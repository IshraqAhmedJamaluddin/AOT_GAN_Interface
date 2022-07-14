import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.utils import spectral_norm

from .common import BaseNetwork
import hiddenlayer as hl
from torchsummary import summary

#BaseNetwork inherits from nn.Module in file common
class InpaintGenerator(BaseNetwork):
    def __init__(self, args):  # 1046
        # super is for using the initilization of the parent class
        super(InpaintGenerator, self).__init__()
        # print(self)
        # A sequential container is used to create a small model to be passed to a constarcator 
        # starts by padding then 3 conv layers and applies relu on the three conv2d layers
        self.encoder = nn.Sequential(
            #This layer is for padding by 3
            nn.ReflectionPad2d(3),
            #conv layer
            # kernal was 7
            nn.Conv2d(4, 64, 7),
            nn.ReLU(True),
            #conv layer
            # Kernal was 4
            nn.Conv2d(64, 128, 4, stride=2, padding=1),
            nn.ReLU(True),
            #conv layer
            #kernal was 4
            nn.Conv2d(128, 256, 4, stride=2, padding=1),
            nn.ReLU(True)
            # the output of RELU is from 0 if the value is negative to the input value if it is possitive
        )
        # print("encoder " , self.encoder)
        # 
        self.middle = nn.Sequential(*[AOTBlock(256, args.rates) for _ in range(args.block_num)])
        
        # The decoder consists of three conv layers with RELU applied on the first two layers 
        self.decoder = nn.Sequential(
          #r input channels 256 output 128 
            UpConv(256, 128),
            # applies RELU activation function on layer 1
            nn.ReLU(True),
             # downsamples inside a conv layer input 256 output 128 
            UpConv(128, 64),
            # applies RELU activation function on layer 1
            nn.ReLU(True),
            # conv2d layer where 64 is the number of channels inputted
            nn.Conv2d(64, 3, 3, stride=1, padding=1)
        )

        self.init_weights()
        # print("Generator" , self)
        # summary(self, (1, 3, 512, 512))

        first_parameter = next(self.parameters())
        input_shape = first_parameter.size()
        # print(f"input_shape {input_shape}")

        

    #for calling the layers that we have defined to build the generator model 
    def forward(self, x, mask):
       #This line is for concatinating x(clear images ??) and masks 
        x = torch.cat([x, mask], dim=1)
        x = self.encoder(x)
        x = self.middle(x)
        x = self.decoder(x)
        # the output of the generator have to be between -1 and 1 and its input and output are tensors 
        x = torch.tanh(x)
        return x


class UpConv(nn.Module):
    def __init__(self, inc, outc, scale=2):
        super(UpConv, self).__init__()
        #for determining our scale factor 
        self.scale = scale
        self.conv = nn.Conv2d(inc, outc, 3, stride=1, padding=1)
    
    #for calling our inilized layer
    def forward(self, x):
        # interpolate function is for upsamplying or downsamplying based on the given scale factor (here it upsamples by 2)
        # print(f"input shape of x {x.shape}")
        return self.conv(F.interpolate(x, scale_factor=2, mode='bilinear', align_corners=True))

#############################################################################################################################################################
class AOTBlock(nn.Module):
    def __init__(self, dim, rates):
        super(AOTBlock, self).__init__()
        self.rates = rates
        for i, rate in enumerate(rates):
            self.__setattr__(
                'block{}'.format(str(i).zfill(2)), 
                nn.Sequential(
                    #padding
                    nn.ReflectionPad2d(rate),
                    #Conv layer where the channels are divided over 4 and dilation in applied
                    nn.Conv2d(dim, dim//4, 3, padding=0, dilation=rate),
                    #conv layer is applied on the conv layer
                    nn.ReLU(True)))
        self.fuse = nn.Sequential(
            nn.ReflectionPad2d(1),
            # paddin then conv layer which takes input channels equal to the original number of channels
            nn.Conv2d(dim, dim, 3, padding=0, dilation=1))
        self.gate = nn.Sequential(
            nn.ReflectionPad2d(1),
            nn.Conv2d(dim, dim, 3, padding=0, dilation=1))

    def forward(self, x):
        out = [self.__getattr__(f'block{str(i).zfill(2)}')(x) for i in range(len(self.rates))]
        out = torch.cat(out, 1)
        out = self.fuse(out)

        mask = my_layer_norm(self.gate(x))
        mask = torch.sigmoid(mask)

        #returning the resutlt after applying equation 
        # x*(1-g)+ x*g
        # where g is the result after applying sigmoid activation function
        return x * (1 - mask) + out * mask


def my_layer_norm(feat):
  # Returns the mean value of all elements in the input tensor.
  # keepdim (bool) – whether the output tensor has dim retained or not.
    mean = feat.mean((2, 3), keepdim=True)
  
  # Calculates the standard deviation of all elements in the input tensor
    std = feat.std((2, 3), keepdim=True) + 1e-9
    feat = 2 * (feat - mean) / std - 1
    feat = 5 * feat
    return feat



################################################################################################################################################
# ----- discriminator -----
#Leaky ReLU is a modification of the ReLU activation function. It has the same form as the ReLU, 
#but it will leak some positive values to 0 if they are close enough to zero. 
#it is a variant of the ReLU activation function

class Discriminator(BaseNetwork):
    def __init__(self, ):
        super(Discriminator, self).__init__()
        inc = 3
        self.conv = nn.Sequential(
          # Spectral normalization stabilizes the training of discriminators 
          #  It controls the Lipschitz constant of the discriminator to mitigate the exploding gradient problem and the mode collapse problem.
            spectral_norm(nn.Conv2d(inc, 64, 4, stride=2, padding=1, bias=False)),
            nn.LeakyReLU(0.2, inplace=True),
            spectral_norm(nn.Conv2d(64, 128, 4, stride=2, padding=1, bias=False)),
            nn.LeakyReLU(0.2, inplace=True),
            spectral_norm(nn.Conv2d(128, 256, 4, stride=2, padding=1, bias=False)),
            nn.LeakyReLU(0.2, inplace=True),
            spectral_norm(nn.Conv2d(256, 512, 4, stride=1, padding=1, bias=False)),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(512, 1, 4, stride=1, padding=1)
        )

        self.init_weights()

    def forward(self, x):
        feat = self.conv(x)
        # print(f'feat {feat}')
        return feat


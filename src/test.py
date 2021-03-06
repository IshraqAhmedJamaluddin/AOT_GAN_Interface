import os
import argparse
import importlib
import numpy as np
from PIL import Image
from glob import glob

import torch
import torch.nn as nn
from torchvision.transforms import ToTensor

from utils.option import args 
import natsort



def postprocess(image):
    image = torch.clamp(image, -1., 1.)
    image = (image + 1) / 2.0 * 255.0
    image = image.permute(1, 2, 0)
    image = image.cpu().numpy().astype(np.uint8)
    return Image.fromarray(image)


def main_worker(args, use_gpu=False): 

    device = torch.device('cuda') if use_gpu else torch.device('cpu')
    
    # Model and version
    net = importlib.import_module('model.'+args.model)
    model = net.InpaintGenerator(args)
    model.load_state_dict(torch.load(args.pre_train))
    model.eval()

    # prepare dataset
    image_paths = []
    for ext in ['.jpg', '.png']: 
        image_paths.extend(glob(os.path.join(args.dir_image, '*'+ext)))
    # image_paths = natsort.natsorted(image_paths,reverse=False)
    image_paths.sort()
    print("image_paths ",image_paths )



    mask_paths = []
    for ext in ['.jpg', '.png']: 
        mask_paths.extend(glob(os.path.join(args.dir_mask, '*'+ext)))
    mask_paths.sort()
    print("mask_paths ", mask_paths)
    os.makedirs(args.outputs, exist_ok=True)
    
    # iteration through datasets
    for ipath, mpath in zip(image_paths, mask_paths): 
        image = ToTensor()(Image.open(ipath).convert('RGB').resize((512,512)))
        image = (image * 2.0 - 1.0).unsqueeze(0)
        mask = ToTensor()(Image.open(mpath).convert('L').resize((512,512)))
        mask = mask.unsqueeze(0)
        # image, mask = image.cuda(), mask.cuda()
        image_masked = image * (1 - mask.float()) + mask
        
        with torch.no_grad():
            pred_img = model(image_masked, mask)

        comp_imgs = (1 - mask) * image + mask * pred_img
        image_name = os.path.basename(ipath).split('.')[0]
        postprocess(image_masked[0]).save(os.path.join(args.outputs, f'{image_name}_masked.png'))

        # os.makedirs(/content/drive/MyDrive/AOTGAN-for-Inpainting3/src/outputs/predicted2, exist_ok=True)
        postprocess(pred_img[0]).save(os.path.join('../src/outputs/predicted', f'{image_name}.png'))
        postprocess(comp_imgs[0]).save(os.path.join(args.outputs, f'{image_name}_comp.png'))
        print(f'saving to {os.path.join(args.outputs, image_name)}')

if __name__ == '__main__':
    main_worker(args)








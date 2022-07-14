# AOT-GAN Interface


## Prerequisites

- [Python](https://www.python.org/downloads/)
- [Flask](https://flask.palletsprojects.com/en/2.1.x/)

## How to run

- First, download the pretrained model and put it in /src/experiments/aotgan_clear_pconv512

- Download the checkpoints and put them in src/outputs/Facades2/checkpoints

- update the model name in /backend/flaskr/__init__.py if needed (~ line 42)

- Create a virtual environment

- Make sure all the requirements are installed

    `pip install -r requirements.txt`

- Then add the location to your environment variable:

    Mac OS/Linux: `export FLASK_APP=flaskr`

    Windows: `$env:FLASK_APP="flaskr"`

- Then use:

    `flask run --host=0.0.0.0 --port=5000`
        
    to run the api

- Open frontend/index.html and Voila!
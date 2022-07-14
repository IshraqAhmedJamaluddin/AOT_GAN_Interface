# AOT-GAN Interface


## Prerequisites

- [Python](https://www.python.org/downloads/)
- [Flask](https://flask.palletsprojects.com/en/2.1.x/)

## How to run

- First, download the pretrained model and put it in /src/experiments/aotgan_clear_pconv512

- update the model name in /backend/flaskr/__init__.py if needed (~ line 42)

- Make sure all the requirements are installed

- Then add the location to your environment variable:

    Mac OS/Linux: `export FLASK_APP=flaskr`

    Windows: `$env:FLASK_APP="flaskr"`

- Then use:

    `flask run --host=0.0.0.0 --port=5000`
        
    to run the api

- Open frontend/index.html and Voila!
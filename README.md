# Arabic OCR: API

This project is a part of a Graduation Project by: Omar Farid, Ishraq Ahmed, Mazen Mohamed, Hossam Gomaa

## Prerequisites

- [Python](https://www.python.org/downloads/)

## How to run

- First, download the easyOCR zip from [here](https://drive.google.com/file/d/1dPQh64ZbqnFD0e7J-blm5DkM0ggDjIK0/view?usp=sharing)

- Extract it so it's under the big folder.

- Then install the virtualenv package:

    `pip install virtualenv`

- Then create your new environment:

    `virtualenv GP`

- Then activate the virtual environment

    Mac OS/Linux: `source GP/bin/activate`

    Windows: `GP\Scripts\activate`

- Then install the requirements:

    `pip install -r requirements.txt`

- Then add the location to your environment variable:

    Mac OS/Linux: `export FLASK_APP=flaskr`

    Windows: `$env:FLASK_APP="flaskr"`

- Then use:

    `flask run --host=0.0.0.0 --port=5000`
        
    to run the application

## API Endpoints

There's only one end point:

- `/predict`:
    
    Input: file with the key `image`

    ```
    {"image": someKindOfAnImageFile}
    ```
    
    Output:

    ```
    {"status": "success", "text": "predictedText"}
    ```
    or

    ```
    {"status": "error"}
    ```

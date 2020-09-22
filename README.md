# Wifi-fingerprint-classifier-api 


This repo contains the full back-end code for the "maskon" project. 
Project submission page here: https://hclbetterhealth-platform.bemyapp.com/#/projects/5f05cf8b980296001bf00b56

UPDATE: The API is currently offline.


The API was built with FastAPI.

The API is capable of taking in data collected from a client Android phone,
processing it, and returning a classification for the given data
within about 3 seconds.

files:

api_demo.py : The running api. 

api_working.py  : Basically identical to api_demo, but less printouts, and more key protection. 

model_rebuid.py :
    The model_rebuild code showcases the model build steps, however
    we cannot release the source data at this time.
    Balanced accuracy (taking into account the imbalance in label groups)
    is currently at 75%, while f1 score is currently at 95% (due to the imbalance).

trained_io_model.model :
    The production model.

data_proc.py :
    data processing module for user data.

json_logger.py : 
    simple logger for user data, which is active only for debugging (currently active)

test_request.py : 
    tests a post to the api. Sends the conrtents of 'json_test.json' to the
    api.


### using the api remotely

Server URL:
`ec2-18-219-8-226.us-east-2.compute.amazonaws.com:5000`

main endpoint:
`/data_in` (protected by API key - ask authors for access)

docs:
`/docs` (unprotected for the duration of judging period,
normally protected by API key as well)

#### playing around in-browser (If total authentication enabled)


Note: as mentioned above, the doc endpoint is currently unprotected.


You can play around with it in-browser by going to:

`ec2-18-219-8-226.us-east-2.compute.amazonaws.com:5000/set_auth?key=API_KEY`

Which will drop a cookie in your browser to keep you authenticated for 30
minutes.(credit to
https://medium.com/data-rebels/fastapi-authentication-revisited-enabling-api-key-authentication-122dc5975680
for the bulk of this slick API-Key code)


You can then go to `/docs`
to test the endpoints in-browser.

To test data_in:
```
click 'data_in', 
click 'try it out', 
paste into the 'Request Body' field the json found in the json_test.json file.
```
It should return "True"


When you're done with your session, go to `/logout` to delete the authentication cookie.

#### testing a python-triggered api call

from within this repo folder, run:

```
python test_request.py
```
It will send the contents of json_test.json, as well as the pre-defined auth
header, and you should see {predicted_indoor_state: true} as a response.


### running the api locally


Using the first steps from the fastapi tutorial: https://fastapi.tiangolo.com/tutorial/first-steps/

in terminal:
  ```
  pip install fastapi
  pip install uvicorn

  uvicorn api_working:app --reload
  ```
  

Thanks for checking this out!

Please let us know if you have any questions, or would like an API key
to test it yourself.

# wifi-fingerprint-classification


### using the api remotely

The server is now running and widely accessible - go to api_dev branch for
files.

accessing the pages requires an API key, which for now is stored in plaintext
in api_working.py. The URL is also there, and here:
ec2-18-219-8-226.us-east-2.compute.amazonaws.com

#### playing around in-browser

You can play around with it in-browser by going to:

ec2-18-219-8-226.us-east-2.compute.amazonaws.com/set_auth?key=[[the key from the python file]]

and then going to ec2-18-219-8-226.us-east-2.compute.amazonaws.com/docs

The api endpoints should work within the docs, you should be authenticated (I
haven't tested it)

When you're done with your session, go to /logout to delete the authentication
cookie.

#### testing a python-triggered api call

from within this repo folder, run:

```
python test_request.py
```
It will send the contents of json_test.json, as well as the pre-defined auth
header, and you should see {predicted_indoor_state: true} as a response.


### running the api locally

To use:

checkout branch api_dev

There are a lot of jupyter notebook files in here that you can ignore to run the API.

Using the first steps from the fastapi tutorial: https://fastapi.tiangolo.com/tutorial/first-steps/
in terminal:
  ```
  pip install fastapi
  pip install uvicorn

  uvicorn api_working:app --reload
  ```

(if on ec2 instance):
```
uvicorn api_working:app --host 0.0.0.0 --port 5000 --reload
```
  
To test with manual input:

go to the docs page, which should be http://127.0.0.1:8000/docs

click 'data_in', click 'try it out', paste into the 'Request Body' field the json found in the json_test text file.

It should return "True"





TODO

#### test with our own data
stub

#### sidenote: detecting when user is at home

As a side note, we can deal with the problem of not alerting people to mask up when they walk into their homes by having them register the name of the wifi AP (the colloqial SSID, not the BSSIC mac address). When this is detected, the alert system will shut off, and the pinging system will go into stasis mode for power saving (polling the wifi once every 5 minutes or so, until the ssid is not detected, perhaps twice in a row).



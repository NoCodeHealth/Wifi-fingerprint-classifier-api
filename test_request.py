import requests as re
import json
from pprint import pprint
from key_biz import KEY, URL

send_endpoint = "data_in"
HEADERS = {"key":
        KEY}

def run():
    with open('json_test.json','r') as f:
        test_payload = json.load(f)

    test_payload = json.dumps(test_payload)
    response = re.post(URL + send_endpoint,headers=HEADERS,data=test_payload)
    print(response.headers)
    pprint(response.json())

if __name__=="__main__":
    run()

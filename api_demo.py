'''fastapi general imports'''
from fastapi import Depends, FastAPI
from pydantic import BaseModel
'''python core library imports'''
from typing import Optional
import pickle
import secrets
import json
'''custom imports'''
import data_proc
from json_logger import logger
from key_biz import KEY, URL
'''security imports'''
from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse
from starlette.requests import Request


"""base code"""
DEBUG = True
LIVE_DISPLAY = True

API_KEY = KEY
API_KEY_NAME = "key"
COOKIE_DOMAIN = URL 

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

print('hello')

"""working code"""


with open('trained_io_model.model', 'rb') as f:
    trained_model = pickle.load(f)


class Data(BaseModel):
    user_id: int
    received_array: list

async def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie),
):

    if api_key_query and secrets.compare_digest(api_key_query,API_KEY):
        return api_key_query
    elif api_key_header and secrets.compare_digest(api_key_header,API_KEY):
        return api_key_header
    elif api_key_cookie and secrets.compare_digest(api_key_cookie,API_KEY):
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

@app.get("/")
async def read_root(api_key: APIKey = Depends(get_api_key)):
    return {"Hello, you are authenticated": "go hit the docs at /docs"}

'''----------------------main function-----------'''

@app.post("/data_in")
async def predict(request: Request, data: Data,api_key: APIKey = Depends(get_api_key)):
    input_array = data.received_array
    processed_data = data_proc.process_input(input_array)
    pred = trained_model.predict(processed_data)
    output_pred = str(pred[0])
    if DEBUG:
        await logger(data.received_array, output_pred, request.client.host)
    if LIVE_DISPLAY:
        print('----------------------------------------')
        print('showcase output')
        print('example input (truncated to first ten input rows):')
        pprint(input_array[:10])
        print('processed input data - ready for classification')
        pprint(processed_data)
        print('the below array is returned to the client:')
        print(ret)
    return {"predicted_indoor_state": output_pred}

'''thats all folks'''


'''api key code
lightly adapted from: 
https://medium.com/data-rebels/fastapi-authentication-revisited-enabling-api-key-authentication-122dc5975680
'''


@app.get("/openapi.json", tags=["documentation"])
async def get_open_api_endpoint():
    response = JSONResponse(
        get_openapi(title="NCH docs", version=1, routes=app.routes)
    )
    return response

@app.get("/docs", tags=["documentation"])
async def get_documentation():
    response = get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
    response.set_cookie(
        API_KEY_NAME,
        value=api_key,
        domain=COOKIE_DOMAIN,
        httponly=True,
        max_age=1800,
        expires=1800,
    )
    return response

@app.get("/set_auth")
async def route_login_and_set_cookie(api_key: APIKey = Depends(get_api_key)):
    response = JSONResponse(
    {"you are authenticated": "yes you are"})
    response.set_cookie(
        API_KEY_NAME,
        value=api_key,
        domain=COOKIE_DOMAIN,
        httponly=True,
        max_age=1800,
        expires=1800,
    )
    return response

@app.get("/logout")
async def route_logout_and_remove_cookie():
    response = JSONResponse(
    {"are you authenticated?": "not any more"})
    response.delete_cookie(API_KEY_NAME, domain=COOKIE_DOMAIN)
    return response

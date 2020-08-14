import json
import os
from datetime import datetime
from pathlib import Path
'''quick n dirty json logger for inputs'''

def log_new(fp: str, ip:str, new_data:dict):
    if not Path(fp).exists():
        old_data = {}
    else:
        with open(fp, 'r') as f:
            old_data = json.load(f)

    if old_data.get(ip,None):
        old_data[ip].append(new_data)
    else:
        old_data[ip] = [new_data]

    with open(fp, 'w') as f:
        json.dump(old_data, f)

async def logger(new_data,pred,ip):
    today = datetime.strftime(datetime.now(),'%Y-%m-%d')
    fp = './logging/{}.json'.format(today) 
    data_dict = {
        'recieved_array': new_data,
        'output_pred': pred
        }
    log_new(fp, ip, data_dict)
    return True
    

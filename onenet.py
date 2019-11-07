#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ==============================
# @File   onenet.py
# @Date   Created on 2019/07/09
# @Author Hehesheng
# ==============================
import requests
import json
import logging

logging.basicConfig(level=logging.INFO,
                    format="[%(filename)s:%(lineno)s]-%(funcName)20s()]:%(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# headers = {
#     "api-key": "k=0=wkvq=gqPAJL8apDMjU=8l8o=",
# }
info = [{"id": "528233832", "head": {"api-key": "k=0=wkvq=gqPAJL8apDMjU=8l8o="}},
        {"id": "541342082", "head": {"api-key": "2g4FG7C=feNvz=pwhicfDz0m8OQ="}}]


def get_onenet_stream(id, device=info[0]["id"]):
    url = 'http://api.heclouds.com/devices/' + \
        device + '/datastreams/' + id
    for headers in info:
        if headers["id"] == device:
            res = requests.request("GET", url, headers=headers["head"], timeout=5)
    return res.text


def get_current_value(res):
    j = json.loads(res)
    if j["errno"] != 0:
        logger.debug(j["error"])
        return None
    return j["data"]["current_value"]

def get_current_onenet(id, device=info[0]["id"]):
    return get_current_value(get_onenet_stream(id, device))

if __name__ == "__main__":
    datastream_id = 'data_pack'
    _res = get_onenet_stream(datastream_id)

    # print(_res.text)

    j = json.loads(_res.text)
    print(j['data']['current_value'])

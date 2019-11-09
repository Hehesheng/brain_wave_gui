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


class onenet(object):
    def __init__(self, id, stream):
        super().__init__()
        self.id = id
        self.stream = stream

    def get_onenet_stream(self):
        url = 'http://api.heclouds.com/devices/' + \
            self.id + '/datastreams/' + self.stream
        for headers in info:
            if headers["id"] == self.id:
                res = requests.request(
                    "GET", url, headers=headers["head"], timeout=5)
                return res.text
        return None

    def get_current_value(self, res):
        j = json.loads(res)
        if j["errno"] != 0:
            logger.debug(j["error"])
            return None
        return j["data"]["current_value"]

    def get_current_onenet(self):
        try:
            j = self.get_current_value(self.get_onenet_stream())
            pack = json.loads(j)
        except Exception as e:
            print(e)
            return None
        return pack


if __name__ == "__main__":
    datastream_id = 'tgam_pack'
    dev_id = "528233832"
    net = onenet(dev_id, datastream_id)
    _res = net.get_current_onenet()

    print(_res)

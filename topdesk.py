# !/usr/bin/python3
# coding: UTF-8

# https://developers.topdesk.com/documentation/index.html

import requests
import json
from utils import join_url_items, make_request

class TOPdesk():
    PAGE_SIZE = 30
    TIMEOUT = 60
    WEBMETHODS = {
        "search_ticket": "incidents",
        "update_ticket": "incidents/id"
    }


    def __init__(self, address, login, token, operator):
        self.api = "https://{}/tas/api".format(address)
        self.address = address
        self.login = login
        self.token = token
        self.operator = operator


    def retrieve_tickets(self):
        request = {
            "url": join_url_items([self.api, self.WEBMETHODS["search_ticket"]]),
            "data": {},
            "headers": {"Content-Type": "application/json", "Accept-Encoding": None},
            "auth": requests.auth.HTTPBasicAuth(self.login, self.token),
            "params": {
                "query": "operatorGroup.name=={};completed==false;closed==false".format(self.operator),
                "pageSize": self.PAGE_SIZE
            },
            "verify": True,
            "timeout": self.TIMEOUT,
            "method": requests.get
        }

        return make_request(request)


    def update_recovery_time(self, incident_id, date):
        request = {
            "url": join_url_items([self.api, self.WEBMETHODS["update_ticket"], incident_id]),
            "data": json.dumps({
                "optionalFields1" : {
                    "date2" : date
                }
            }),
            "headers": {"Content-Type": "application/json", "Accept-Encoding": None},
            "auth": requests.auth.HTTPBasicAuth(self.login, self.token),
            "params": {},
            "verify": True,
            "timeout": self.TIMEOUT,
            "method": requests.put
        }

        return make_request(request)


    def add_note(self, incident_id, message):
        request = {
            "url": join_url_items([self.api, self.WEBMETHODS["update_ticket"], incident_id]),
            "data": json.dumps({
                "action": message
            }),
            "headers": {"Content-Type": "application/json", "Accept-Encoding": None},
            "auth": requests.auth.HTTPBasicAuth(self.login, self.token),
            "params": {},
            "verify": True,
            "timeout": self.TIMEOUT,
            "method": requests.put
        }

        return make_request(request)

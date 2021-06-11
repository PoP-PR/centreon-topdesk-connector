# !/usr/bin/python3
# coding: UTF-8

# https://docs.centreon.com/api/centreon-web/

import requests
import json
import urllib
from utils import join_url_items, make_request

class Centreon():
    TIMEOUT = 60

    def __init__(self, name, address, login, password):
        self.name = name
        self.api = "https://{}/centreon/api/beta".format(address)
        self.address = address
        self.login = login
        self.password = password
        self.token = None


    def get_token(self):
        if not self.token:
            request = {
                "url": join_url_items([self.api, "login"]),
                "data": json.dumps({
                    "security": {
                        "credentials": {
                            "login": self.login,
                            "password": self.password
                        }
                    }
                }),
                "headers": {"Content-type": "application/json"},
                "auth": {},
                "params": {},
                "verify": True,
                "timeout": self.TIMEOUT,
                "method": requests.post
            }
            req = make_request(request)
            token = req["security"]["token"]
            
            self.token = token

        return self.token


    def get_auth_header(self):
        auth = {"X-AUTH-TOKEN": self.get_token()}
        return auth

    
    # retrieve host and service ids
    def get_ids(self, brief_desc):
        request = {
            "url": join_url_items([self.api, "monitoring/services"]),
            "data": {},
            "headers": self.get_auth_header(),
            "auth": {},
            "params": {
                "search": {
                    "service.display_name": {
                        "$eq": brief_desc
                    }
                }
            },
            "verify": True,
            "timeout": self.TIMEOUT,
            "method": requests.get
        }
        request["params"] = urllib.parse.urlencode(request["params"]).replace("%27", "%22") # replace ' with "

        req = make_request(request)
        result = req["result"]

        host_id = str(result[0]["host"]["id"])
        service_id = str(result[0]["id"])

        return host_id, service_id


    def get_recovery_time(self, brief_desc, date):
        host_id, service_id = self.get_ids(brief_desc)
        request = {
            "url": join_url_items([self.api, "monitoring/hosts", host_id, "services", service_id, "timeline"]),
            "data": {},
            "headers": self.get_auth_header(),
            "auth": {},
            "params": {
                "search": {
                    "date": {"$gt": date},
                    "content": {"$lk": "OK%"}
                },
                "sort_by": {
                    "date": "ASC"
                }
            },
            "verify": True,
            "timeout": self.TIMEOUT,
            "method": requests.get
        }
        request["params"] = urllib.parse.urlencode(request["params"]).replace("%27", "%22") # replace ' with "

        req = make_request(request)
        result = req["result"]

        try:
            recovery = result[0]['date']
            return recovery, host_id, service_id
        except:
            return None

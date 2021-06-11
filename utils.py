# !/usr/bin/python3
# coding: UTF-8

import urllib
import dateutil.parser
import requests
from pytz import timezone
from datetime import datetime

def join_url_items(items):
    return "/".join(items)


# date is an utc datetime string
def localize(date):
    brasil = timezone("America/Sao_Paulo")
    date = dateutil.parser.parse(date)
    date = date.astimezone(brasil)
    date = datetime.timestamp(date)

    return date


def build_msg(name, address, host_id, service_id):
    centreon_url = "https://{}/centreon/monitoring/resources?".format(address)
    params = {
        "details" : {
            "id": service_id,
            "parentId": host_id,
            "type":"service",
            "parentType":"host",
            "tab":"timeline"
        }
    }
    params = urllib.parse.urlencode(params).replace("%27", "%22") # replace ' with "
    msg =   """
            Horário de normalização atualizado automaticamente por {}, disponível em {}
            """.format(
                name,
                "<a href='{}'>Centreon</a>".format(centreon_url + params)
            )

    return msg


def make_request(request):        
    result = request["method"](request["url"], data=request["data"], headers=request["headers"],  verify=request["verify"],
            auth=request["auth"], params=request["params"], timeout=request["timeout"])
    
    data = {}
    try:
        data = result.json()
    except:
        pass
    
    return data
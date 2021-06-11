# !/usr/bin/python3
# coding: UTF-8

from centreon import Centreon
from topdesk import TOPdesk
from config import TOPDESK_API, CENTREON_API
from utils import localize, build_msg

import logging
logging.basicConfig(filename="topdesk.log", level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")

if __name__ == '__main__':
    topdesk_user = TOPdesk(**TOPDESK_API)
    centreon_user = Centreon(**CENTREON_API)

    # Recupera os tickets
    tickets = topdesk_user.retrieve_tickets()

    for t in tickets:
        incident_id = t["id"]
        number = t["number"]
        desc = t["briefDescription"]
        failure = t["optionalFields1"]["date1"]

        if failure: # some tickets dont have this field setted
            failure = localize(failure)

            # Recupera o horário de normalização
            recovery, host_id, service_id = centreon_user.get_recovery_time(desc, failure)

            # Se não houver
            if not recovery:
                logging.info("{}: ainda não há horário de normalização.".format(desc))
            else:
                result = topdesk_user.update_recovery_time(incident_id, recovery)
                try:
                    # Caso bem sucedido irá retornar o ticket atualizado
                    logging.info("{} - {}: atualizado.".format(result["number"], result["briefDescription"]))
                    msg = build_msg(centreon_user.name, centreon_user.address, host_id, service_id)
                    topdesk_user.add_note(incident_id, msg)
                except:
                    logging.info("{} - {}: nenhum campo atualizado.".format(number, desc))

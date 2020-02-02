import json
import logging

import requests

from nia_sauron_spoofing_controller.util.response_error import raise_error


class RequestUtil:

    __header_json = {'content-type': 'application/json'}

    def __init__(self, payload, url, header='json'):
        self.__payload = payload
        self.__url = url
        self.__header = self.__get_headers(header)

    def __get_headers(self, header):
        h = None
        if header == 'json':
            h = self.__header_json
        return h

    def post(self, verify=False, timeout=20):
        response = None
        try:
            url = self.__url
            header = self.__header
            payload = self.__payload
            response = requests.post(
                url=url,
                data=json.dumps(payload),
                headers=header,
                verify=verify,
                timeout=timeout
            )
        except requests.exceptions.RequestException as e:
            logging.getLogger('spoofing.request').info(e)
            raise_error(405)
        return response

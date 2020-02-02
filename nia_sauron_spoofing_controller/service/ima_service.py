import json
import logging
import os

from nia_sauron_spoofing_controller.util.config_util import ConfigUtil
from nia_sauron_spoofing_controller.util.request_util import RequestUtil
from nia_sauron_spoofing_controller.util.response_error import raise_error


class ImaService:

    __b64_image = None

    def __init__(self, user_key, protocol, type_interface):
        self.__endpoints = None
        self.config = ConfigUtil()  # Read config file util
        # Init Request
        self.requests = RequestUtil(self.__payload(
            user_key, protocol, type_interface
        ), self.__url())

    def __url(self):
        url = None
        try:
            url = os.environ['IMA_CURIO_URL'] + self.config.get('IMA', 'e1')
        except KeyError:
            logging.getLogger('spoofing.api').info('IMA_CURIO_URL > not found')
        return url

    @staticmethod
    def __payload(user_key, protocol, type_interface):
        payload = {
            "chave_usuario": user_key,
            "protocolo_imagem": protocol,
            "tipo_imagem": [type_interface]
        }
        return payload

    def get_ima_b64(self):
        ima_response = json.loads(self.requests.post().text)
        if not isinstance(ima_response, list):
            raise_error(412)
        return ima_response[0]['imagemBinario']

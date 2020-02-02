import asyncio
import json
import logging
import os
import time

from aiohttp import ClientSession

from nia_sauron_spoofing_controller.util.api_util import ApiUtil
from nia_sauron_spoofing_controller.util.config_util import ConfigUtil
from nia_sauron_spoofing_controller.util.response_error import raise_error


class SpoofingService:

    __b64_image = None
    __header = {'content-type': 'application/json'}

    def __init__(self):
        self.__endpoints = []
        self.api_response = []
        self.util = ApiUtil()
        self.config = ConfigUtil()

    def get_endpoint(self):
        # Antispoofing
        self.__url_antispoofing()
        # Antispoofing-Deep
        self.__url_antispoofing_deep()

    def is_spoofing(self, loop):
        if len(self.__endpoints) > 0:
            loop.create_task(self.__fetch(loop, self.__endpoints))
            loop.run_forever()

        return self.__get_vote()

    def __url_antispoofing(self):
        try:
            url = os.environ['ANTI_SPOOFING_URL']
            payload = {'image': self.__b64_image}
            self.__endpoints.append(
                [url + self.config.get('ANTISPOOFING', 'e1'), payload])
            self.__endpoints.append(
                [url + self.config.get('ANTISPOOFING', 'e2'), payload])
            self.__endpoints.append(
                [url + self.config.get('ANTISPOOFING', 'e3'), payload])
        except KeyError:
            logging.getLogger('spoofing.api').info(
                'ANTI_SPOOFING_URL > not found')

    def __url_antispoofing_deep(self):
        try:
            url = os.environ['ANTI_SPOOFING_DEEP_URL']
            payload = {'b64_image': self.__b64_image}
            self.__endpoints.append(
                [url + self.config.get('ANTISPOOFING_DEEP', 'e1'), payload])
            self.__endpoints.append(
                [url + self.config.get('ANTISPOOFING_DEEP', 'e2'), payload])
        except KeyError:
            logging.getLogger('spoofing.api').info(
                'ANTI_SPOOFING_DEEP_URL > not found')

    async def __set_requests(self, session, enp):
        start_time = time.time()
        async with session.post(
                url=enp[0], data=json.dumps(enp[1])) as response:

            if response.status == 200:
                logging.getLogger('spoofing.endpoint').info(
                    enp[0] + " --> %s seconds" % (time.time() - start_time))
                self.api_response.append([response.status,
                                          await response.json()])
            else:
                logging.getLogger('spoofing.endpoint').error(
                    enp[0] + " --> " + str(response.status))
                self.api_response.append([response.status])

    async def __fetch(self, loop, endpoints):
        async with ClientSession(headers=self.__header, loop=loop) as session:
            tasks = (self.__set_requests(session, enp) for enp in endpoints)
            await asyncio.gather(*tasks, return_exceptions=True)
            loop.stop()

    def __get_vote(self):
        trust = 0
        count = 0
        c_400 = 0  # Errors 4xx
        c_500 = 0  # Errors 500
        score_p = 0  # Score positive
        score_n = 0  # Score negative
        for response in self.api_response:
            if response[0] == 200:
                count += 1
                if not response[1]['is_spoofed']:
                    trust += 1
                    score_p += response[1]['trust']  # Get score when is False.
                    score_n += 100 - response[1]['trust']
                else:
                    score_p += 100 - response[1]['trust']
                    score_n += response[1]['trust']  # Get score when is True.
            # Get error code.
            elif 400 <= response[0] < 500:
                c_400 += 1
            else:
                c_500 += 1
        logging.getLogger('spoofing.service').info({
            'endpoint': len(self.api_response),
            '200': count,
            '400': c_400,
            '500': c_500
        })
        return self.__get_trust(trust, count, score_p, score_n, c_400, c_500)

    def __get_trust(self, trust, count, score_p, score_n, c_400, c_500):
        spoofed = True
        score = score_n
        logging.getLogger('spoofing.service').info({
            'False': trust, 'True': count - trust})
        try:
            if trust > (count - trust):
                spoofed = False
                score = score_p
        except ZeroDivisionError:
            logging.getLogger('spoofing.service').info(
                'Error, endpoint not found')
            raise_error(405)
        return spoofed, round(
            float(score / (len(self.__endpoints) - (c_400 + c_500))), 2)

    def is_request_valid(self, request):
        if not request.is_json:  # Is json.
            raise_error(400)
        result = request.get_json()
        # Contains the key.
        if not all(key in result for key in ['b64_image']):
            raise_error(403)
        b64_image = result['b64_image']
        # Is a base 64?
        try:
            self.util.is_base64(b64_image)
        except ValueError:
            raise_error(401)
        # Get image.
        self.__b64_image = b64_image

    @staticmethod
    def is_ima_request_valid(request):
        if not request.is_json:  # Is json.
            raise_error(400)
        result = request.get_json()
        # Contains the key.
        if not all(key in result for key in
                   ['chave_usuario', 'protocolo_imagem', 'tipo_imagem']):
            raise_error(403)
        # image type is a list?
        if not isinstance(result['tipo_imagem'], int):
            raise_error(400)
        # --.
        user_key = result['chave_usuario']
        protocol = result['protocolo_imagem']
        type_interface = result['tipo_imagem']
        return user_key, protocol, type_interface

    def set_base_64(self, base_64):
        self.__b64_image = base_64

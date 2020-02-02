import asyncio
import logging

from flask import Blueprint, jsonify, request

from nia_sauron_spoofing_controller.service.ima_service import ImaService
from nia_sauron_spoofing_controller.service.spoofing_service import \
    SpoofingService

loop = asyncio.get_event_loop()
ima = Blueprint('ima', __name__)


@ima.route('/spoofing/ima/protocol', methods=['POST'])
def spoofing_ima_b64():
    """Check endpoint handler.
    Args:
        (dict): user key, protocol number and type.
    Returns:
        dict: .
    """
    service = SpoofingService()
    user_key, protocol, type_interface = service.is_ima_request_valid(request)
    ima_service = ImaService(user_key, protocol, type_interface)
    # --.
    service.set_base_64(ima_service.get_ima_b64())
    service.get_endpoint()
    spoofed, score = service.is_spoofing(loop)
    # Response
    output_response = {
        'is_spoofed': spoofed,
        'trust': score
    }
    logging.getLogger('spoofing.controller').info(output_response)
    return jsonify(output_response), 200

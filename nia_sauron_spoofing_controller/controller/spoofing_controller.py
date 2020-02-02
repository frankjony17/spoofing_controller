import asyncio
import logging

from flask import Blueprint, jsonify, request

from nia_sauron_spoofing_controller.service.spoofing_service import \
    SpoofingService

loop = asyncio.get_event_loop()
spoofing = Blueprint('spoofing', __name__)


@spoofing.route('/spoofing/image/b64', methods=['POST'])
def spoofing_image_b64():
    """Check endpoint handler.
    Args:
        (dict): Base64 encoded image.
    Returns:
        dict: .
    """
    service = SpoofingService()
    service.is_request_valid(request)
    service.get_endpoint()
    spoofed, score = service.is_spoofing(loop)
    # Response
    output_response = {
        'is_spoofed': spoofed,
        'trust': score
    }
    logging.getLogger('spoofing.controller').info(output_response)
    return jsonify(output_response), 200

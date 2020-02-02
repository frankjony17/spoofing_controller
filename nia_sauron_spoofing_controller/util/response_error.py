
from flask import Blueprint, abort, jsonify

error_handler = Blueprint('error_handler', __name__)


error_dict = {
    400: {'detail': 'Bad Request, wrong syntax. '
                    'The request could not be understood by the server.'},
    401: {'detail': 'Bad Request, wrong base64. Wrong base64 format.'},
    404: {'detail': 'Bad Request, required parameters missing,'
                    ' parameters wasn\'t found.'},
    403: {'detail': 'Bad Request, bad image. Error in base64 input,'
                    ' no image was found.'},
    405: {'detail': 'Server not Found, '
                    'Error connecting to remote APIs, no connection.'},
    412: {'detail': 'Invalid value, '
                    'IMA does not recognize one of the parameters.'}
}


def raise_error(code):
    if code > 200:
        abort(code)


def response(code):
    """Return response message according to request type of error.
    Args:
        code (int): Code of error.
    Returns:
        dict or None: Message and reason from request type of error.
    """
    return error_dict.get(code, None)


@error_handler.app_errorhandler(400)
def wrong_syntax(error):
    return jsonify(response(400)), 400


@error_handler.app_errorhandler(401)
def wrong_base64(error):
    return jsonify(response(401)), 400


@error_handler.app_errorhandler(404)
def bad_image(error):
    return jsonify(response(404)), 400


@error_handler.app_errorhandler(403)
def miss_parameters(error):
    return jsonify(response(403)), 400


@error_handler.app_errorhandler(405)
def no_face(error):
    return jsonify(response(405)), 400


@error_handler.app_errorhandler(412)
def precondition_failed(error):
    return jsonify(response(412)), 400


__version__ = '0.1.1'

import logging.config
import os
from pathlib import Path

import yaml
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint


def get_scheme(swagger_yml):
    try:
        swagger_yml['schemes'] = [os.environ['SCHEMES']]
        logging.getLogger('spoofing.api').info("SCHEMES > OK")
    except KeyError:
        logging.getLogger('spoofing.api').info('SCHEMES > not found')


def create_app():
    root_path, path = Path(__file__).parents[0], ''
    app = Flask(__name__)

    if os.path.exists(root_path / 'config'):
        root_path = root_path / 'config'
        # logging configs
        if os.environ.get('MODE') == 'prod':
            print('-----STARTING PRODUCTION APPLICATION-----')
            path = root_path / 'logging_cloud.yaml'
        elif os.environ.get('MODE') == 'dev':
            print('----- STARTING DEVELOPMENT APPLICATION -----')

            if not os.path.exists('/var/log/sauron/'):
                print('WARNING: Logging will not work since /var/log/sauron/ '
                      'do not exist.')
            else:
                path = root_path / 'logging.yaml'
        print(f'----- PID {os.getpid()} -----')

        if path:
            with open(str(path), 'rt') as f:
                config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)

        # creates API docs endpoint from swagger file
        doc_path = str(root_path / 'swagger.yaml')
        swagger_yml = yaml.safe_load(open(doc_path, 'r'))
        # get scheme
        get_scheme(swagger_yml)

        app.register_blueprint(
            get_swaggerui_blueprint('/docs', doc_path,
                                    config={'spec': swagger_yml}),
            url_prefix='/docs')
    else:
        print('-----STARTING TESTING APPLICATION-----')

    # error handler
    from nia_sauron_spoofing_controller.util.response_error \
        import error_handler
    app.register_blueprint(error_handler)

    # Start controller
    from nia_sauron_spoofing_controller.controller.start_controller \
        import start
    app.register_blueprint(start)

    # helpers controller
    from nia_sauron_spoofing_controller.util.helpers_controller import helpers
    app.register_blueprint(helpers)

    # spoofing controller
    from nia_sauron_spoofing_controller.controller.spoofing_controller \
        import spoofing
    app.register_blueprint(spoofing)

    # ima controller
    from nia_sauron_spoofing_controller.controller.ima_controller \
        import ima
    app.register_blueprint(ima)

    logging.getLogger('spoofing.init').info(
        'Application created, ready to up.')

    return app

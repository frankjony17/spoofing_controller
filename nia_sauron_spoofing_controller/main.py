import logging
import os

from nia_sauron_spoofing_controller import create_app
from nia_sauron_spoofing_controller.util.middleware_controller import \
    setup_metrics

app = create_app()
setup_metrics(app)


def start_server():
    port = int(os.environ.get('PORT', 9000))
    logging.getLogger('spoofing.main').info(f'Starting in port {port}.')
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('MODE') != 'prod',
            use_reloader=os.environ.get('MODE') != 'prod')


if __name__ == '__main__':
    start_server()

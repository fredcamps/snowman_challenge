#!/usr/bin/env python
"""Script that runs app.
"""

from snowman_challenge.app import create_app

application = create_app(config_filename='config')

if __name__ == '__main__':
    application.run(
        host=application.config['HOST'],
        port=application.config['PORT'],
        debug=application.config['DEBUG'],
    )

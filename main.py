""" Main entry point for this application """
import threading
import time
import os

from flask_application import flask_application


if __name__ == "__main__":
    # Get environment parameters for starting the Flask application
    ip = os.getenv('IP', '127.0.0.1')  # <- We should really check if this is a valid ip-address
    port = int(os.getenv('PORT', '5000'))  # <- We should really check if this is an integer!

    # Initialize the Flask application
    flask_application = flask_application.APIServer(ip=ip, port=port)

    # Start the Flask application
    thread = threading.Thread(target=flask_application.run)
    thread.start()

    try:
        while True:
            # Flask runs in its own thread. Reason: If docker (assumption is that the application is run inside a
            # docker container) a sigterm is captured as a KeyboardInterrupt. By catching this interrupt we can
            # quickly terminate the Flask application by calling its stop method.
            time.sleep(0.1)  # 0.1 seconds is an eternity for an android...
    except KeyboardInterrupt:
        flask_application.stop()

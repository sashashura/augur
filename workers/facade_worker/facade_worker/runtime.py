from flask import Flask, jsonify, request, Response
import click, os, json, requests, logging
from workers.facade_worker.facade_worker.facade00mainprogram import FacadeWorker
from workers.util import create_server, WorkerGunicornApplication

def main():
    """ Declares singular worker and creates the server and flask app that it will be running on
    """
    app = Flask(__name__)
    app.worker = FacadeWorker()

    create_server(app)
    WorkerGunicornApplication(app).run()

    if app.worker._child is not None:
        app.worker._child.terminate()
    try:
        requests.post('http://{}:{}/api/unstable/workers/remove'.format(broker_host, broker_port), json={"id": config['id']})
    except:
        pass

    os.kill(os.getpid(), 9)


    # config = { 
    #         'id': 'com.augurlabs.core.facade_worker.{}'.format(worker_port),
    #         'location': 'http://{}:{}'.format(read_config('Server', 'host', 'AUGUR_HOST', 'localhost'),worker_port),
    #         'password': read_config('Database', 'password', 'AUGUR_DB_PASSWORD', 'password'),
    #         'port': read_config('Database', 'port', 'AUGUR_DB_PORT', 'port'),
    #         'user': read_config('Database', 'user', 'AUGUR_DB_USER', 'user'),
    #         'database': read_config('Database', 'name', 'AUGUR_DB_NAME', 'database'),
    #         'host': read_config('Database', 'host', 'AUGUR_DB_HOST', 'host')
    #     }


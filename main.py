import sys
import logging
import time
import threading
from connector import node
from apscheduler.schedulers.background import BackgroundScheduler
from connector.synchronizer import synchronizer
import kubernetes
from kubernetes import config
from connector import client
import gevent
from gevent import Greenlet


CONTAINER_UUID = "65c7c310-1410-4d5c-9560-d6cd03d514d5"
logger_name = "openstack-k8s-connector"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def sync_node_status():
    logger.warning('Start syncing Node states.')
    #node.node_update_status(node.NODE_NAME)

#class check_capsule_status(threading.Thread):
#    def run(self):

def sync_capsule_status():
    config.load_kube_config()

    configuration = kubernetes.client.Configuration()
    configuration.api_key['authorization'] = 'YOUR_API_KEY'

    api_instance = kubernetes.client.CoreV1Api()

    openstack_client = client.Client()

    sync = synchronizer(openstack_client, api_instance)
    sync.sync_capsule_k8s()


def main(argv):
    #node.update()
    #sched = BackgroundScheduler()
    #sched.add_job(sync_node_status, 'interval', seconds=5)
    #sched.add_job(sync_capsule_status, 'interval', seconds=3)
    #sched.start()

    sync_capsule_status()

    #try:
    #    # This is here to simulate application activity (which keeps the main thread alive).
    #    while True:
    #        time.sleep(2)
    #except (KeyboardInterrupt, SystemExit):
    #    # Not strictly necessary if daemonic mode is enabled but should be done if possible
    #    sched.shutdown()


if __name__ == '__main__':
    main(sys.argv)


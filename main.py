import sys
import logging
import time
from connector import node
from apscheduler.schedulers.background import BackgroundScheduler


logger_name = "openstack-k8s-connector"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.WARN)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def sync_node_status():
    logger.warning('Start syncing Node states.')

    node.node_update_status(node.NODE_NAME)

def main(argv):
    node.update()
    sched = BackgroundScheduler()
    sched.add_job(sync_node_status, 'interval', seconds=5)
    sched.start()
    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        sched.shutdown()

if __name__ == '__main__':
    main(sys.argv)

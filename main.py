import sys
import logging
from connector import node
from threading import Timer


logger_name = "openstack-k8s-connector"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.WARN)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def sync_node_status():
    logger.info('Start syncing Node states.')

    node.node_update_status(node.NODE_NAME)

def main(argv):
    logger.info('Process begin')
    node.update()
    #node.node_update_status(node.NODE_NAME, node.get_time())
    Timer(5, sync_node_status()).start()


if __name__ == '__main__':
    main(sys.argv)

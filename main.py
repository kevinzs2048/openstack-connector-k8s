import sys
from openstack_connector_k8s.cmd.eventlet import controller


def main(argv):
    controller.start(argv)


if __name__ == '__main__':
    main(sys.argv)

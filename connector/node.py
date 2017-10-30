from __future__ import print_function
import kubernetes
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from kubernetes.client.models import v1_node_condition as node_condition
from kubernetes.client.models import v1_node_status
from pprint import pprint
import datetime
from dateutil.tz import tzlocal
import logging

logger_name = "openstack-k8s-connector"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)
NODE_NAME = "openstack-k8s-connector"
KUBELET_VERSION = "v1.8.1"

def update():
    try:
        logger.info("Node Update")
        config.load_kube_config()

        configuration = kubernetes.client.Configuration()
        configuration.api_key['authorization'] = 'YOUR_API_KEY'

        api_instance = kubernetes.client.CoreV1Api()

        try:
            result = api_instance.list_node()
        except ApiException as e:
            logger.error("Exception when calling CoreV1Api->list_node: %s\n" % e)

        found = False
        for item in result.items:
            if item.metadata.name == NODE_NAME:
                found = True
                break

        if found:
            logger.info("found node openstack-k8s-connector")
        else:
            time_last = get_time()
            status = v1_node_status.V1NodeStatus(
                node_info={'kubeletVersion': KUBELET_VERSION},
                conditions=_node_get_condition(time_last)
            )
            body = kubernetes.client.V1Node(api_version="v1",
                                            kind="Node",
                                            metadata={"name": NODE_NAME},
                                            spec={"taints": [{"key": "openstack/zun",
                                                              "effect": "NoSchedule"}]},
                                            status=status)
            try:
                api_response = api_instance.create_node(body)
                pprint(api_response)
            except ApiException as e:
                logger.error("Exception when calling CoreV1Api->create_node: %s\n" % e)
    except Exception as e:
        logger.error("Error: %s", e)


def get_time():
    time = datetime.datetime.now(tzlocal())
    return time


def _node_get_condition(time_last):
    provider_registered = False
    conditions = [node_condition.V1NodeCondition(last_heartbeat_time=get_time(),
                                                 last_transition_time=time_last,
                                                 message='kubelet is posting ready',
                                                 reason='KubeletReady',
                                                 status='True',
                                                 type='Ready')]


    message = 'kubelet has sufficient disk space available'
    reason = 'KubeletHasSufficientDisk'
    status = 'False'
    type = 'OutOfDisk'
    condition_outofdisk = node_condition.V1NodeCondition(last_heartbeat_time=get_time(),
                                                         last_transition_time=time_last,
                                                         message=message,
                                                         reason=reason,
                                                         status=status,
                                                         type=type)
    conditions.append(condition_outofdisk)

    if not provider_registered:
        # TODO(kevinz): get the provider information here:
        provider_ready = True
        if provider_ready:
            provider_registered = True
        else:
            time = get_time()
            message = 'OpenStack Zun service not registered'
            reason = 'ProviderRegistered'
            status = 'False'
            type = 'ProviderStatus'
            condition_not_registered = node_condition(time, time_last, message, reason, status, type)
            conditions.append(condition_not_registered)

    return conditions


def node_update_status(node_name):
    config.load_kube_config()
    configuration = kubernetes.client.Configuration()
    configuration.api_key['authorization'] = 'YOUR_API_KEY'
    api_instance = kubernetes.client.CoreV1Api()
    try:
        node = api_instance.read_node(node_name)
        logger.warning(node.status)
    except ApiException as e:
        logger.error("Exception when calling CoreV1Api->read_node: %s\n" % e)
        return
    if node:
        time_last = get_time()
        conditions = _node_get_condition(time_last)
        node.status = v1_node_status.V1NodeStatus(
            node_info={'kubeletVersion': KUBELET_VERSION, 'architecture': "amd64"},
            allocatable={"cpu": "8", "memory": "100Gi", "pods": "20"},
            conditions=conditions
        )
        #TODO(kevinz): calculate quota here
        node.status.capacity = node.status.allocatable

        try:
            api_instance.replace_node(node.metadata.name, node)
        except ApiException as e:
            logger.error("Exception when calling CoreV1Api->replace_node: %s\n" % e)
    else:
        logger.warning("No available nodes")

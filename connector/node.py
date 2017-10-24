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


NODE_NAME = "openstack-k8s-connector"

def update():
    try:
        config.load_kube_config()

        configuration = kubernetes.client.Configuration()
        configuration.api_key['authorization'] = 'YOUR_API_KEY'

        api_instance = kubernetes.client.CoreV1Api()

        thread = api_instance.list_node(async=True)

        result = thread.get()
        for item in result.items:
            if item.metadata.name == NODE_NAME:
                found = True
                break

        if found:
            logging.info("found openstack-k8s-connector")
        else:
            time_last = get_time()
            status = v1_node_status.V1NodeStatus(
                node_info={'kubeletVersion': 'v1.6.6'},
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
                logging.error("Exception when calling CoreV1Api->create_node: %s\n" % e)
    except Exception as e:
        logging.error("Error: %s", e)


def get_time():
    time = datetime.datetime.now(tzlocal()).strftime('%a, %d %b %Y %X %z')
    return time


def _node_get_condition(time_last):
    provider_registered = False
    conditions = [node_condition.V1NodeCondition(get_time(),
                                                time_last,
                                                'kubelet is posting ready',
                                                'KubeletReady',
                                                'True',
                                                'Ready')]


    time = get_time()
    message = 'kubelet has sufficient disk space available'
    reason = 'KubeletHasSufficientDisk'
    status = 'False'
    type = 'OutOfDisk'
    condition_outofdisk = node_condition.V1NodeCondition(get_time(),
                                                         time_last,
                                                         message,
                                                         reason,
                                                         status,
                                                         type)
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
    except ApiException as e:
        logging.error("Exception when calling CoreV1Api->read_node: %s\n" % e)
    time_last = get_time()
    conditions = _node_get_condition(time_last)
    node.status = v1_node_status.V1NodeStatus(
        node_info={'kubeletVersion': 'v1.6.6', 'architecture': "amd64"},
        allocatable={"cpu": "8", "memory": "100Gi", "pods": "20"},
        conditions=conditions
    )
    #TODO(kevinz): calculate quota here
    node.status.capacity = node.status.allocatable

    try:
        api_instance.replace_node(node.metadata.name, node)
    except ApiException as e:
        logging.error("Exception when calling CoreV1Api->replace_node: %s\n" % e)


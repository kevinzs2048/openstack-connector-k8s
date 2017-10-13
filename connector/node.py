from __future__ import print_function
import time
import kubernetes
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from pprint import pprint


config.load_kube_config()

configuration = kubernetes.client.Configuration()
configuration.api_key['authorization'] = 'YOUR_API_KEY'

api_instance = kubernetes.client.CoreV1Api()

ret = api_instance.list_pod_for_all_namespaces(watch=False)
for i in ret.items:
    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

body = kubernetes.client.V1Node(api_version="v1", kind="Node", metadata={"name": "openstack1-k8s-connector"}, 
       spec={"taints": [{"key": "openstack/zun", "effect": "NoSchedule"}]})

try: 
    api_response = api_instance.create_node(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CoreV1Api->create_node: %s\n" % e)

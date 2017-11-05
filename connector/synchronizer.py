# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import kubernetes
from kubernetes import client as k8s_client
from connector.client import Client
import datetime
import logging


logger_name = "openstack-k8s-connector"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)
NODE_NAME = "openstack-k8s-connector"
KUBELET_VERSION = "v1.8.1"

class synchronizer(Client):
    def __init__(self, openstackclient=None, k8sclient=None):
        self.openstackclient = openstackclient
        self.k8sclient = k8sclient

    def _get_capsule_info(self):
        capsules = self.openstackclient.cs.capsules.list()
        capsules_for_connector = {}
        for capsule in capsules:
            if capsule.meta_label.get('orchestrator', default=None) != 'kubernetes':
                continue
            #TODO(kevinz): Make the capsule meta_name as the identification.
            capsules_for_connector[capsule.meta_name] = capsule
        return capsules_for_connector


    def _get_pods_info(self):
        thread = self.k8sclient.list_namespace_pod(namespace="default",
                                                   async=True)
        pods = thread.get()
        pod_in_connector = []
        for pod in pods.items:
            if pod.spec.node_name != NODE_NAME:
                continue
            pod_in_connector.append(pod)

        return pod_in_connector

    def sync_capsule_k8s(self):
        capsules = self._get_capsule_info()
        pods = self._get_pods_info()
        for pod in pods:
            if capsules[pod.spec.node_name] is None:
                continue
            ##TODO(kevinz): Add transfermation from obj to json
            ##and tweak the parameters



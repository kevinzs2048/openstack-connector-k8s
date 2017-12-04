#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import openstack_connector_k8s.conf
from oslo_log import log as logging
from openstack_connector_k8s.clients import k8s_client
from openstack_connector_k8s.clients import zun_client

CONF = openstack_connector_k8s.conf.CONF
_clients = {}
_ZUN_CLIENT = 'zun-client'
_KUBERNETES_CLIENT = 'kubernetes-client'
LOG = logging.getLogger(__name__)


def get_zun_client():
    return _clients[_ZUN_CLIENT]


def get_kubernetes_client():
    return _clients[_KUBERNETES_CLIENT]


def setup_clients():
    try:
        setup_zun_client()
    except RuntimeError as e:
        LOG.error("Runtime Error: %s, if authorized error, you need to "
                  "setup the env parameters for OpenStack", e)
        raise e
    try:
        setup_kubernetes_client()
    except Exception as e:
        LOG.error("setup Kubernetes client failed: %s", e)
        raise e


def setup_zun_client():
    _clients[_ZUN_CLIENT] = zun_client.Client()
    LOG.info("Connected to OpenStack Zun")


def setup_kubernetes_client():
    _clients[_KUBERNETES_CLIENT] = k8s_client.K8sClient(
        CONF.kubernetes.api_root)

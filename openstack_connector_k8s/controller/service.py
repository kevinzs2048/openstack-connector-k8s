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

import sys

from oslo_log import log as logging
from oslo_service import service

from openstack_connector_k8s.clients import clients
from openstack_connector_k8s import conf
from openstack_connector_k8s.controller.handlers import pipeline as h_pipeline
from openstack_connector_k8s import watcher
#from kuryr_kubernetes import constants
#from kuryr_kubernetes.controller.handlers import lbaas as h_lbaas
#from kuryr_kubernetes.controller.handlers import vif as h_vif
#from kuryr_kubernetes import objects
#from kuryr_kubernetes import watcher

LOG = logging.getLogger(__name__)
CONF = conf.CONF


class ConnectorService(service.Service):
    """OpenStack-connector-K8S controller Service."""

    def __init__(self):
        super(ConnectorService, self).__init__()

        #TODO(kevinz): Add the DB Object and Operation.
        pipeline = h_pipeline.ControllerPipeline(self.tg)
        self.watcher = watcher.Watcher(pipeline, self.tg)
        # TODO(kevinz): pluggable resource/handler registration
        for resource in ["pods", "services", "endpoints"]:
            self.watcher.add("%s/%s" % (constants.K8S_API_BASE, resource))
        pipeline.register(h_vif.VIFHandler())
        pipeline.register(h_lbaas.LBaaSSpecHandler())
        pipeline.register(h_lbaas.LoadBalancerHandler())

    def start(self):
        LOG.info("Service '%s' starting", self.__class__.__name__)
        super(ConnectorService, self).start()
        self.watcher.start()
        LOG.info("Service '%s' started", self.__class__.__name__)

    def wait(self):
        super(ConnectorService, self).wait()
        LOG.info("Service '%s' stopped", self.__class__.__name__)

    def stop(self, graceful=False):
        LOG.info("Service '%s' stopping", self.__class__.__name__)
        self.watcher.stop()
        super(ConnectorService, self).stop(graceful)


def start():
    conf.base.init(sys.argv[1:])
    conf.base.setup_logging()
    clients.setup_clients()
    #os_vif.initialize()
    kuryrk8s_launcher = service.launch(CONF, ConnectorService())
    kuryrk8s_launcher.wait()

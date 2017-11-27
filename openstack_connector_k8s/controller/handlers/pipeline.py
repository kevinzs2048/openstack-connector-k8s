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

from openstack_connector_k8s import exceptions
from openstack_connector_k8s.handlers import asynchronous as h_async
from openstack_connector_k8s.handlers import dispatch as h_dis
from openstack_connector_k8s.handlers import k8s_base as h_k8s
from openstack_connector_k8s.handlers import logging as h_log
from openstack_connector_k8s.handlers import retry as h_retry


class ControllerPipeline(h_dis.EventPipeline):
    """Serves as an entry point for controller Kubernetes events.

    `ControllerPipeline` is an entry point handler for the
    OpenStack-connector-K8S controller. `ControllerPipeline` allows registering
    :class:`openstack_connector_k8s.handlers.k8s_base.ResourceEventHandler`s and
    ensures the proper handler is called for each event that is passed to the
    `ControllerPipeline`. Also it ensures the following behavior:

      - multiple `ResourceEventHandler`s can be registered for the same
        resource type (`OBJECT_KIND`)

      - failing handlers (i.e. ones that raise `Exception`s) are retried
        until either the handler succeeds or a finite amount of time passes,
        in which case the most recent exception is logged

      - in case there are multiple handlers registered for the same resource
        type, all such handlers are considered independent (i.e. if one
        handler fails, other handlers will still be called regardless; and the
        order in which such handlers are called is not determined)

      - events for different Kubernetes objects can be handled concurrently

      - events for the same Kubernetes object are handled sequentially in
        the order of arrival
    """

    def __init__(self, thread_group):
        self._tg = thread_group
        super(ControllerPipeline, self).__init__()

    def _wrap_consumer(self, consumer):
        # TODO(ivc): tune retry interval/timeout
        return h_log.LogExceptions(h_retry.Retry(
            consumer, exceptions=exceptions.ResourceNotReady))

    def _wrap_dispatcher(self, dispatcher):
        return h_log.LogExceptions(h_async.Async(dispatcher, self._tg,
                                                 h_k8s.object_link))

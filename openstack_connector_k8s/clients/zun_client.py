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

from zunclient.experimental import client
from zunclient import api_versions
import openstack_connector_k8s.conf

DEFAULT_API_VERSION = api_versions.DEFAULT_API_VERSION
EXPERIENTAL_SERVICE_TYPE = 'container-experimental'
CONF = openstack_connector_k8s.conf.CONF


class Client(object):
    def __init__(self, api_version=DEFAULT_API_VERSION, **kwargs):
        self.version = api_version
        self.username = CONF.zun_client.os_username
        self.password = CONF.zun_client.os_password
        self.project_id = CONF.zun_client.os_project_id
        self.project_name = CONF.zun_client.os_project_name
        self.user_domain_id = CONF.zun_client.os_user_domain_id
        self.user_domain_name = CONF.zun_client.os_user_domain_name
        self.project_domain_id = CONF.zun_client.os_project_domain_id
        self.project_domain_name = CONF.zun_client.os_project_domain_name
        self.auth_url = CONF.zun_client.os_auth_url
        self.service_type = EXPERIENTAL_SERVICE_TYPE
        self.region_name = CONF.zun_client.os_region_name
        self.endpoint_override = CONF.zun_client.endpoint_override
        self.interface = CONF.zun_client.os_endpoint_type
        self.insecure = CONF.zun_client.zunclient_insecure
        self.cs = client.Client(version=self.version,
                                username=self.username,
                                password=self.password,
                                project_id=self.project_id,
                                project_name=self.project_name,
                                user_domain_id=self.user_domain_id,
                                user_domain_name=self.user_domain_name,
                                project_domain_id=self.project_domain_id,
                                project_domain_name=self.project_domain_name,
                                auth_url=self.auth_url,
                                service_type=self.service_type,
                                region_name=self.region_name,
                                endpoint_override=self.endpoint_override,
                                interface=self.interface,
                                insecure=self.insecure,
                                **kwargs)

    def list(self):
        return self.cs.capsules.list()

#
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

import os
from zunclient.experimental import client
from zunclient import api_versions

DEFAULT_API_VERSION = api_versions.DEFAULT_API_VERSION
EXPERIENTAL_SERVICE_TYPE = 'container-experimental'
DEFAULT_ENDPOINT_TYPE = 'publicURL'


def env(*args, **kwargs):
    """Returns the first environment variable set.

    If all are empty, defaults to '' or keyword arg `default`.
    """
    for arg in args:
        value = os.environ.get(arg)
        if value:
            return value
    return kwargs.get('default', '')


class Client(object):
    def __init__(self, api_version=DEFAULT_API_VERSION, **kwargs):
        self.version = api_version
        self.username = env('OS_USERNAME', default=None)
        self.password = env('OS_PASSWORD', default=None)
        self.project_id = env('OS_PROJECT_ID', default=None)
        self.project_name = env('OS_PROJECT_NAME', default=None)
        self.user_domain_id = env('OS_USER_DOMAIN_ID')
        self.user_domain_name = env('OS_USER_DOMAIN_NAME')
        self.project_domain_id = env('OS_PROJECT_DOMAIN_ID')
        self.project_domain_name = env('OS_PROJECT_DOMAIN_NAME')
        self.auth_url = env('OS_AUTH_URL')
        self.service_type = EXPERIENTAL_SERVICE_TYPE
        self.region_name = env('OS_REGION_NAME')
        self.endpoint_override = env('BYPASS_URL', default=None)
        self.interface = env('OS_ENDPOINT_TYPE', default=DEFAULT_ENDPOINT_TYPE)
        self.insecure = env('ZUNCLIENT_INSECURE', default=False)
        import pdb;pdb.set_trace()
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

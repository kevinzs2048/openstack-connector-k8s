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

import json
import six
import datetime

def pod_to_capsule(pod):
    pod.kind = "capsule"
    pod.api_version = "beta"
    pod_json = pod.to_dict()
    containers = pod_json.get('spec').get('containers')

    for container in containers:
        container['environment'] = container.get('env')
        container['workdir'] = container.get('working_dir')
        container['stdin_open'] = container.get('stdin')
        ##NOTE(kevinz): Here we map the limits to zun "allocation"
        if container.get('resources').get('limits') is not None:
            container.get('resources')['allocation'] = \
                container.get('resources').get('limits')
        else:
            container.pop('resources')
        container.pop('env')
        container.pop('working_dir')
        container.pop('stdin')
    creation_time = pod_json.get('metadata').get('creation_timestamp')
    deletion_time = pod_json.get('metadata').get('deletion_timestamp')
    if creation_time is not None:
        pod_json.get('metadata')['creation_timestamp'] = \
            creation_time.strftime("%Y-%m-%d %H:%M:%S%z")
    if deletion_time is not None:
        pod_json.get('metadata')['deletion_timestamp'] = \
            deletion_time.strftime("%Y-%m-%d %H:%M:%S%z")
    import pdb;pdb.set_trace()
    return pod_json

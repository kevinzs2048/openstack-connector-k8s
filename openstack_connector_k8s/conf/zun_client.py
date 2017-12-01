#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import os

from oslo_config import cfg
from openstack_connector_k8s.common import utils
from openstack_connector_k8s.common.i18n import _

EXPERIENTAL_SERVICE_TYPE = 'container-experimental'
DEFAULT_ENDPOINT_TYPE = 'publicURL'

zun_client_opts = [
    cfg.StrOpt('os_username',
               help=_("OS username"),
               default=utils.env('OS_USERNAME', default=None)),
    cfg.StrOpt('os_password',
               help=_("OS password"),
               default=utils.env('OS_PASSWORD', default=None)),
    cfg.StrOpt('os_project_id',
               help=_("OS project id"),
               default=utils.env('OS_PROJECT_ID', default=None)),
    cfg.StrOpt('os_project_name',
               help=_("OS project name"),
               default=utils.env('OS_PROJECT_NAME', default=None)),
    cfg.StrOpt('os_user_domain_id',
               help=_("OS user domain id"),
               default=utils.env('OS_USER_DOMAIN_ID', default=None)),
    cfg.StrOpt('os_user_domain_name',
               help=_("OS user domain name"),
               default=utils.env('OS_USER_DOMAIN_NAME', default=None)),
    cfg.StrOpt('os_project_domain_id',
               help=_("OS project domain id"),
               default=utils.env('OS_PROJECT_DOMAIN_ID', default=None)),
    cfg.StrOpt('os_project_domain_name',
               help=_("OS project domain name"),
               default=utils.env('OS_PROJECT_DOMAIN_NAME', default=None)),
    cfg.StrOpt('os_region_name',
               help=_("OS region name"),
               default=utils.env('OS_REGION_NAME')),
    cfg.StrOpt('os_auth_url',
               help=_("OS auth url"),
               default=utils.env('OS_AUTH_URL')),
    cfg.StrOpt('endpoint_override',
               help=_("Endpoint override"),
               default=utils.env('BYPASS_URL', default=None)),
    cfg.StrOpt('os_endpoint_type',
               help=_("OS endpoint type"),
               default=utils.env('OS_ENDPOINT_TYPE', default=None)),
    cfg.StrOpt('zunclient_insecure',
               help=_("zun client insecure"),
               default=utils.env('ZUNCLIENT_INSECURE', default=None)),
]


zun_group = cfg.OptGroup(name='zun_client',
                         title='Options for zun client')


ALL_OPTS = (zun_client_opts)


def register_opts(conf):
    conf.register_group(zun_group)
    conf.register_opts(ALL_OPTS, zun_group)


def list_opts():
    return {
        zun_group: ALL_OPTS
    }

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from glanceclient.exc import ClientException
from glanceclient.v2 import client as glance_client
from keystoneclient.auth.identity import v2 as keystone_v2
from keystoneclient.auth.identity import v3 as keystone_v3
from keystoneclient import client as keystoneclient
from keystoneclient import session


class GlanceHealth(object):

    def __init__(self, creds):
        cacert = creds['cacert']
        del creds['cacert']
        auth = keystone_v3.Password(**creds)
        sess = session.Session(auth=auth, verify=cacert)
        self.glanceclient = glance_client.Client('1', session=sess)

    def glance_image_list(self):
        try:
            image_list = self.glanceclient.images.list()
            # The above api doens't generate appropriate exception
            # so we are walking through the generator to raise exception
            for image in image_list:
                pass
        except (ClientException, Exception) as e:
            return (404, "ClientException:" + str(e), [])
        return (200, "success", image_list)

    def glance_image_create(self, image_url,
                            image_name, cont_format, disk_format):
        try:
            ret = self.glanceclient.images.create(location=image_url,
                                                  name=image_name,
                                                  container_format=cont_format,
                                                  disk_format=disk_format)
        except (ClientException, Exception) as e:
            return (404, e.message, [])
        return (200, "success", ret)

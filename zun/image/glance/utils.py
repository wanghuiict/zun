# Copyright 2016 Intel.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from oslo_utils import uuidutils

from zun.common import clients
from zun.common import exception
from zun.common.i18n import _LE


def create_glanceclient(context):
    """Creates glance client object.

        :param context: context to create client object
        :returns: Glance client object
    """
    osc = clients.OpenStackClients(context)
    return osc.glance()


def find_image(context, image_ident):
    glance = create_glanceclient(context)
    if uuidutils.is_uuid_like(image_ident):
        image_meta = glance.images.get(image_ident)
    else:
        filters = {'name': image_ident}
        matches = list(glance.images.list(filters=filters))
        if len(matches) == 0:
            raise exception.ImageNotFound(image=image_ident)
        if len(matches) > 1:
            msg = _LE("Multiple images exist with same name "
                      "%(image_ident)s. Please use the image id "
                      "instead.") % {'image_ident': image_ident}
            raise exception.Conflict(msg)
        image_meta = matches[0]
    return image_meta
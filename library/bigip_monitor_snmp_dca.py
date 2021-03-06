#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2017 F5 Networks Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {
    'status': ['preview'],
    'supported_by': 'community',
    'metadata_version': '1.1'
}

DOCUMENTATION = '''
---
module: bigip_monitor_snmp_dca
short_description: Manages BIG-IP SNMP data collecting agent (DCA) monitors.
description:
  - The BIG-IP has an SNMP data collecting agent (DCA) that can query remote
    SNMP agents of various types, including the UC Davis agent (UCD) and the
    Windows 2000 Server agent (WIN2000).
version_added: "2.5"
options:
  name:
    description:
      - Monitor name.
    required: True
    aliases:
      - monitor
  description:
    description:
      - Specifies descriptive text that identifies the monitor.
  parent:
    description:
      - The parent template of this monitor template. Once this value has
        been set, it cannot be changed. By default, this value is the C(snmp_dca)
        parent on the C(Common) partition.
    default: "/Common/snmp_dca"
  interval:
    description:
      - Specifies, in seconds, the frequency at which the system issues the
        monitor check when either the resource is down or the status of the
        resource is unknown. When creating a new monitor, the default is C(10).
  timeout:
    description:
      - Specifies the number of seconds the target has in which to respond to
        the monitor request. When creating a new monitor, the default is C(30)
        seconds. If the target responds within the set time period, it is
        considered 'up'. If the target does not respond within the set time
        period, it is considered 'down'. When this value is set to 0 (zero),
        the system uses the interval from the parent monitor. Note that
        C(timeout) and C(time_until_up) combine to control when a resource is
        set to up.
  time_until_up:
    description:
      - Specifies the number of seconds to wait after a resource first responds
        correctly to the monitor before setting the resource to 'up'. During the
        interval, all responses from the resource must be correct. When the
        interval expires, the resource is marked 'up'. A value of 0, means
        that the resource is marked up immediately upon receipt of the first
        correct response. When creating a new monitor, the default is C(0).
  community:
    description:
      - Specifies the community name that the system must use to authenticate
        with the host server through SNMP. When creating a new monitor, the
        default value is C(public). Note that this value is case sensitive.
  version:
    description:
      - Specifies the version of SNMP that the host server uses. When creating
        a new monitor, the default is C(v1). When C(v1), specifies that the
        host server uses SNMP version 1. When C(v2c), specifies that the host
        server uses SNMP version 2c.
    choices:
      - v1
      - v2c
  agent_type:
    description:
      - Specifies the SNMP agent running on the monitored server. When creating
        a new monitor, the default is C(UCD) (UC-Davis).
    choices:
      - UCD
      - WIN2000
      - GENERIC
  cpu_coefficient:
    description:
      - Specifies the coefficient that the system uses to calculate the weight
        of the CPU threshold in the dynamic ratio load balancing algorithm.
        When creating a new monitor, the default is C(1.5).
  cpu_threshold:
    description:
      - Specifies the maximum acceptable CPU usage on the target server. When
        creating a new monitor, the default is C(80) percent.
  memory_coefficient:
    description:
      - Specifies the coefficient that the system uses to calculate the weight
        of the memory threshold in the dynamic ratio load balancing algorithm.
        When creating a new monitor, the default is C(1.0).
  memory_threshold:
    description:
      - Specifies the maximum acceptable memory usage on the target server.
        When creating a new monitor, the default is C(70) percent.
  disk_coefficient:
    description:
      - Specifies the coefficient that the system uses to calculate the weight
        of the disk threshold in the dynamic ratio load balancing algorithm.
        When creating a new monitor, the default is C(2.0).
  disk_threshold:
    description:
      - Specifies the maximum acceptable disk usage on the target server. When
        creating a new monitor, the default is C(90) percent.
  partition:
    description:
      - Device partition to manage resources on.
    required: False
    default: 'Common'
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk.
  - Requires BIG-IP software version >= 12
  - This module does not support the C(variables) option because this option
    is broken in the REST API and does not function correctly in C(tmsh); for
    example you cannot remove user-defined params. Therefore, there is no way
    to automatically configure it.
requirements:
  - f5-sdk >= 2.2.3
extends_documentation_fragment: f5
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Create SNMP DCS monitor
  bigip_monitor_snmp_dca:
      state: "present"
      server: "lb.mydomain.com"
      user: "admin"
      password: "secret"
      name: "my_monitor"
  delegate_to: localhost

- name: Remove TCP Echo Monitor
  bigip_monitor_snmp_dca:
      state: "absent"
      server: "lb.mydomain.com"
      user: "admin"
      password: "secret"
      name: "my_monitor"
  delegate_to: localhost
'''

RETURN = '''
parent:
    description: New parent template of the monitor.
    returned: changed
    type: string
    sample: "snmp_dca"
interval:
    description: The new interval in which to run the monitor check.
    returned: changed
    type: int
    sample: 2
timeout:
    description: The new timeout in which the remote system must respond to the monitor.
    returned: changed
    type: int
    sample: 10
time_until_up:
    description: The new time in which to mark a system as up after first successful response.
    returned: changed
    type: int
    sample: 2
community:
    description: The new community for the monitor.
    returned: changed
    type: string
    sample: foobar
version:
    description: The new new SNMP version to be used by the monitor.
    returned: changed
    type: string
    sample: v2c
agent_type:
    description: The new agent type to be used by the monitor.
    returned: changed
    type: string
    sample: UCD
cpu_coefficient:
    description: The new CPU coefficient.
    returned: changed
    type: float
    sample: 2.4
cpu_threshold:
    description: The new CPU threshold.
    returned: changed
    type: int
    sample: 85
memory_coefficient:
    description: The new memory coefficient.
    returned: changed
    type: float
    sample: 6.4
memory_threshold:
    description: The new memory threshold.
    returned: changed
    type: int
    sample: 50
disk_coefficient:
    description: The new disk coefficient.
    returned: changed
    type: float
    sample: 10.2
disk_threshold:
    description: The new disk threshold.
    returned: changed
    type: int
    sample: 34
'''

import os

from ansible.module_utils.f5_utils import AnsibleF5Client
from ansible.module_utils.f5_utils import AnsibleF5Parameters
from ansible.module_utils.f5_utils import HAS_F5SDK
from ansible.module_utils.f5_utils import F5ModuleError
from ansible.module_utils.f5_utils import iteritems
from ansible.module_utils.f5_utils import defaultdict

try:
    from ansible.module_utils.f5_utils import iControlUnexpectedHTTPError
except ImportError:
    HAS_F5SDK = False


class Parameters(AnsibleF5Parameters):
    api_map = {
        'timeUntilUp': 'time_until_up',
        'defaultsFrom': 'parent',
        'agentType': 'agent_type',
        'cpuCoefficient': 'cpu_coefficient',
        'cpuThreshold': 'cpu_threshold',
        'memoryCoefficient': 'memory_coefficient',
        'memoryThreshold': 'memory_threshold',
        'diskCoefficient': 'disk_coefficient',
        'diskThreshold': 'disk_threshold'
    }

    api_attributes = [
        'timeUntilUp', 'defaultsFrom', 'interval', 'timeout', 'destination', 'community',
        'version', 'agentType', 'cpuCoefficient', 'cpuThreshold', 'memoryCoefficient',
        'memoryThreshold', 'diskCoefficient', 'diskThreshold'
    ]

    returnables = [
        'parent', 'ip', 'interval', 'timeout', 'time_until_up', 'description', 'community',
        'version', 'agent_type', 'cpu_coefficient', 'cpu_threshold', 'memory_coefficient',
        'memory_threshold', 'disk_coefficient', 'disk_threshold'
    ]

    updatables = [
        'ip', 'interval', 'timeout', 'time_until_up', 'description', 'community',
        'version', 'agent_type', 'cpu_coefficient', 'cpu_threshold', 'memory_coefficient',
        'memory_threshold', 'disk_coefficient', 'disk_threshold'
    ]

    def __init__(self, params=None):
        self._values = defaultdict(lambda: None)
        self._values['__warnings'] = []
        if params:
            self.update(params=params)

    def update(self, params=None):
        if params:
            for k, v in iteritems(params):
                if self.api_map is not None and k in self.api_map:
                    map_key = self.api_map[k]
                else:
                    map_key = k

                # Handle weird API parameters like `dns.proxy.__iter__` by
                # using a map provided by the module developer
                class_attr = getattr(type(self), map_key, None)
                if isinstance(class_attr, property):
                    # There is a mapped value for the api_map key
                    if class_attr.fset is None:
                        # If the mapped value does not have
                        # an associated setter
                        self._values[map_key] = v
                    else:
                        # The mapped value has a setter
                        setattr(self, map_key, v)
                else:
                    # If the mapped value is not a @property
                    self._values[map_key] = v

    def to_return(self):
        result = {}
        try:
            for returnable in self.returnables:
                result[returnable] = getattr(self, returnable)
            result = self._filter_params(result)
            return result
        except Exception:
            return result

    def api_params(self):
        result = {}
        for api_attribute in self.api_attributes:
            if self.api_map is not None and api_attribute in self.api_map:
                result[api_attribute] = getattr(self, self.api_map[api_attribute])
            else:
                result[api_attribute] = getattr(self, api_attribute)
        result = self._filter_params(result)
        return result

    @property
    def interval(self):
        if self._values['interval'] is None:
            return None
        if 1 > int(self._values['interval']) > 86400:
            raise F5ModuleError(
                "Interval value must be between 1 and 86400"
            )
        return int(self._values['interval'])

    @property
    def timeout(self):
        if self._values['timeout'] is None:
            return None
        return int(self._values['timeout'])

    @property
    def time_until_up(self):
        if self._values['time_until_up'] is None:
            return None
        return int(self._values['time_until_up'])

    @property
    def parent(self):
        if self._values['parent'] is None:
            return None
        if self._values['parent'].startswith('/'):
            parent = os.path.basename(self._values['parent'])
            result = '/{0}/{1}'.format(self.partition, parent)
        else:
            result = '/{0}/{1}'.format(self.partition, self._values['parent'])
        return result

    @property
    def cpu_coefficient(self):
        result = self._get_numeric_property('cpu_coefficient')
        return result

    @property
    def cpu_threshold(self):
        result = self._get_numeric_property('cpu_threshold')
        return result

    @property
    def memory_coefficient(self):
        result = self._get_numeric_property('memory_coefficient')
        return result

    @property
    def memory_threshold(self):
        result = self._get_numeric_property('memory_threshold')
        return result

    @property
    def disk_coefficient(self):
        result = self._get_numeric_property('disk_coefficient')
        return result

    @property
    def disk_threshold(self):
        result = self._get_numeric_property('disk_threshold')
        return result

    def _get_numeric_property(self, property):
        if self._values[property] is None:
            return None
        try:
            fvar = float(self._values[property])
        except ValueError:
            raise F5ModuleError(
                "Provided {0} must be a valid number".format(property)
            )
        return fvar

    @property
    def type(self):
        return 'snmp_dca'


class Difference(object):
    def __init__(self, want, have=None):
        self.want = want
        self.have = have

    def compare(self, param):
        try:
            result = getattr(self, param)
            return result
        except AttributeError:
            result = self.__default(param)
            return result

    @property
    def parent(self):
        if self.want.parent != self.want.parent:
            raise F5ModuleError(
                "The parent monitor cannot be changed"
            )

    @property
    def destination(self):
        if self.want.ip is None:
            return None
        if self.want.destination != self.have.destination:
            return self.want.destination

    @property
    def interval(self):
        if self.want.timeout is not None and self.want.interval is not None:
            if self.want.interval >= self.want.timeout:
                raise F5ModuleError(
                    "Parameter 'interval' must be less than 'timeout'."
                )
        elif self.want.timeout is not None:
            if self.have.interval >= self.want.timeout:
                raise F5ModuleError(
                    "Parameter 'interval' must be less than 'timeout'."
                )
        elif self.want.interval is not None:
            if self.want.interval >= self.have.timeout:
                raise F5ModuleError(
                    "Parameter 'interval' must be less than 'timeout'."
                )
        if self.want.interval != self.have.interval:
            return self.want.interval

    def __default(self, param):
        attr1 = getattr(self.want, param)
        try:
            attr2 = getattr(self.have, param)
            if attr1 != attr2:
                return attr1
        except AttributeError:
            return attr1


class ModuleManager(object):
    def __init__(self, client):
        self.client = client
        self.have = None
        self.want = Parameters(self.client.module.params)
        self.changes = Parameters()

    def _set_changed_options(self):
        changed = {}
        for key in Parameters.returnables:
            if getattr(self.want, key) is not None:
                changed[key] = getattr(self.want, key)
        if changed:
            self.changes = Parameters(changed)

    def _update_changed_options(self):
        diff = Difference(self.want, self.have)
        updatables = Parameters.updatables
        changed = dict()
        for k in updatables:
            change = diff.compare(k)
            if change is None:
                continue
            else:
                changed[k] = change
        if changed:
            self.changes = Parameters(changed)
            return True
        return False

    def _announce_deprecations(self):
        warnings = []
        if self.want:
            warnings += self.want._values.get('__warnings', [])
        if self.have:
            warnings += self.have._values.get('__warnings', [])
        for warning in warnings:
            self.client.module.deprecate(
                msg=warning['msg'],
                version=warning['version']
            )

    def exec_module(self):
        changed = False
        result = dict()
        state = self.want.state

        try:
            if state == "present":
                changed = self.present()
            elif state == "absent":
                changed = self.absent()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        changes = self.changes.to_return()
        result.update(**changes)
        result.update(dict(changed=changed))
        self._announce_deprecations()
        return result

    def present(self):
        if self.exists():
            return self.update()
        else:
            return self.create()

    def create(self):
        self._set_changed_options()

        if self.want.timeout is None:
            self.want.update({'timeout': 30})
        if self.want.interval is None:
            self.want.update({'interval': 10})
        if self.want.time_until_up is None:
            self.want.update({'time_until_up': 0})
        if self.want.community is None:
            self.want.update({'community': 'public'})
        if self.want.version is None:
            self.want.update({'version': 'v1'})
        if self.want.agent_type is None:
            self.want.update({'agent_type': 'UCD'})
        if self.want.cpu_coefficient is None:
            self.want.update({'cpu_coefficient': '1.5'})
        if self.want.cpu_threshold is None:
            self.want.update({'cpu_threshold': '80'})
        if self.want.memory_coefficient is None:
            self.want.update({'memory_coefficient': '1.0'})
        if self.want.memory_threshold is None:
            self.want.update({'memory_threshold': '70'})
        if self.want.disk_coefficient is None:
            self.want.update({'disk_coefficient': '2.0'})
        if self.want.disk_threshold is None:
            self.want.update({'disk_threshold': '90'})

        if self.client.check_mode:
            return True
        self.create_on_device()
        return True

    def should_update(self):
        result = self._update_changed_options()
        if result:
            return True
        return False

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.client.check_mode:
            return True
        self.update_on_device()
        return True

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def remove(self):
        if self.client.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the monitor.")
        return True

    def read_current_from_device(self):
        resource = self.client.api.tm.ltm.monitor.snmp_dcas.snmp_dca.load(
            name=self.want.name,
            partition=self.want.partition
        )
        result = resource.attrs
        return Parameters(result)

    def exists(self):
        result = self.client.api.tm.ltm.monitor.snmp_dcas.snmp_dca.exists(
            name=self.want.name,
            partition=self.want.partition
        )
        return result

    def update_on_device(self):
        params = self.want.api_params()
        result = self.client.api.tm.ltm.monitor.snmp_dcas.snmp_dca.load(
            name=self.want.name,
            partition=self.want.partition
        )
        result.modify(**params)

    def create_on_device(self):
        params = self.want.api_params()
        self.client.api.tm.ltm.monitor.snmp_dcas.snmp_dca.create(
            name=self.want.name,
            partition=self.want.partition,
            **params
        )

    def remove_from_device(self):
        result = self.client.api.tm.ltm.monitor.snmp_dcas.snmp_dca.load(
            name=self.want.name,
            partition=self.want.partition
        )
        if result:
            result.delete()


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = dict(
            name=dict(required=True),
            description=dict(),
            parent=dict(),
            ip=dict(),
            interval=dict(type='int'),
            timeout=dict(type='int'),
            time_until_up=dict(type='int'),
            community=dict(),
            version=dict(),
            agent_type=dict(
                choices=['UCD', 'WIN2000', 'GENERIC']
            ),
            cpu_coefficient=dict(),
            cpu_threshold=dict(type='int'),
            memory_coefficient=dict(),
            memory_threshold=dict(type='int'),
            disk_coefficient=dict(),
            disk_threshold=dict(type='int')
        )
        self.f5_product_name = 'bigip'


def main():
    try:
        spec = ArgumentSpec()

        client = AnsibleF5Client(
            argument_spec=spec.argument_spec,
            supports_check_mode=spec.supports_check_mode,
            f5_product_name=spec.f5_product_name
        )

        if not HAS_F5SDK:
            raise F5ModuleError("The python f5-sdk module is required")

        mm = ModuleManager(client)
        results = mm.exec_module()
        client.module.exit_json(**results)
    except F5ModuleError as e:
        client.module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()

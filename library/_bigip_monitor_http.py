#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# Copyright (c) 2013 Serge van Ginderachter <serge@vanginderachter.be>
# Copyright (c) 2013 Matt Hite <mhite@hotmail.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: _bigip_monitor_http
short_description: Manages F5 BIG-IP LTM http monitors
deprecated: Deprecated in 2.5. Use C(bigip_monitor_http) instead.
description:
  - Manages F5 BIG-IP LTM monitors via iControl SOAP API
version_added: "1.4"
author:
  - Serge van Ginderachter (@srvg)
  - Tim Rupp (@caphrim007)
notes:
  - "Requires BIG-IP software version >= 11"
  - "F5 developed module 'bigsuds' required (see http://devcentral.f5.com)"
  - "Best run as a local_action in your playbook"
  - "Monitor API documentation: https://devcentral.f5.com/wiki/iControl.LocalLB__Monitor.ashx"
requirements:
  - bigsuds
options:
  state:
    description:
      - Monitor state
    required: false
    default: 'present'
    choices:
      - present
      - absent
  name:
    description:
      - Monitor name
    required: true
    default: null
    aliases:
      - monitor
  partition:
    description:
      - Partition for the monitor
    required: false
    default: 'Common'
  parent:
    description:
      - The parent template of this monitor template
    required: false
    default: 'http'
  parent_partition:
    description:
      - Partition for the parent monitor
    required: false
    default: 'Common'
  send:
    description:
      - The send string for the monitor call
    required: true
    default: none
  receive:
    description:
      - The receive string for the monitor call
    required: true
    default: none
  receive_disable:
    description:
      - The receive disable string for the monitor call
    required: true
    default: none
  ip:
    description:
      - IP address part of the ipport definition. The default API setting
        is "0.0.0.0".
    required: false
    default: none
  port:
    description:
      - Port address part of the ip/port definition. The default API
        setting is 0.
    required: false
    default: none
  interval:
    description:
      - The interval specifying how frequently the monitor instance
        of this template will run. By default, this interval is used for up and
        down states. The default API setting is 5.
    required: false
    default: none
  timeout:
    description:
      - The number of seconds in which the node or service must respond to
        the monitor request. If the target responds within the set time
        period, it is considered up. If the target does not respond within
        the set time period, it is considered down. You can change this
        number to any number you want, however, it should be 3 times the
        interval number of seconds plus 1 second. The default API setting
        is 16.
    required: false
    default: none
  time_until_up:
    description:
      - Specifies the amount of time in seconds after the first successful
        response before a node will be marked up. A value of 0 will cause a
        node to be marked up immediately after a valid response is received
        from the node. The default API setting is 0.
    required: false
    default: none
extends_documentation_fragment: f5
'''

EXAMPLES = r'''
- name: BIGIP F5 | Create HTTP Monitor
  bigip_monitor_http:
    state: present
    server: lb.mydomain.com
    user: admin
    password: secret
    name: my_http_monitor
    send: http string to send
    receive: http string to receive
  delegate_to: localhost

- name: BIGIP F5 | Remove HTTP Monitor
  bigip_monitor_http:
    state: absent
    server: lb.mydomain.com
    user: admin
    password: secret
    name: my_http_monitor
  delegate_to: localhost
'''

TEMPLATE_TYPE = 'TTYPE_HTTP'
DEFAULT_PARENT_TYPE = 'http'


def check_monitor_exists(module, api, monitor, parent):
    # hack to determine if monitor exists
    result = False
    try:
        ttype = api.LocalLB.Monitor.get_template_type(template_names=[monitor])[0]
        parent2 = api.LocalLB.Monitor.get_parent_template(template_names=[monitor])[0]
        if ttype == TEMPLATE_TYPE and parent == parent2:
            result = True
        else:
            module.fail_json(msg='Monitor already exists, but has a different type (%s) or parent(%s)' % (ttype, parent))
    except bigsuds.OperationFailed as e:
        if "was not found" in str(e):
            result = False
        else:
            # genuine exception
            raise
    return result


def create_monitor(api, monitor, template_attributes):
    try:
        api.LocalLB.Monitor.create_template(
            templates=[{
                'template_name': monitor,
                'template_type': TEMPLATE_TYPE
            }],
            template_attributes=[template_attributes]
        )
    except bigsuds.OperationFailed as e:
        if "already exists" in str(e):
            return False
        else:
            # genuine exception
            raise
    return True


def delete_monitor(api, monitor):
    try:
        api.LocalLB.Monitor.delete_template(template_names=[monitor])
    except bigsuds.OperationFailed as e:
        # maybe it was deleted since we checked
        if "was not found" in str(e):
            return False
        else:
            # genuine exception
            raise
    return True


def check_string_property(api, monitor, str_property):
    try:
        template_prop = api.LocalLB.Monitor.get_template_string_property(
            [monitor], [str_property['type']]
        )[0]
        return str_property == template_prop
    except bigsuds.OperationFailed as e:
        # happens in check mode if not created yet
        if "was not found" in str(e):
            return True
        else:
            # genuine exception
            raise


def set_string_property(api, monitor, str_property):
    api.LocalLB.Monitor.set_template_string_property(
        template_names=[monitor],
        values=[str_property]
    )


def check_integer_property(api, monitor, int_property):
    try:
        template_prop = api.LocalLB.Monitor.get_template_integer_property(
            [monitor], [int_property['type']]
        )[0]
        return int_property == template_prop
    except bigsuds.OperationFailed as e:
        # happens in check mode if not created yet
        if "was not found" in str(e):
            return True
        else:
            # genuine exception
            raise


def set_integer_property(api, monitor, int_property):
    api.LocalLB.Monitor.set_template_integer_property(
        template_names=[monitor],
        values=[int_property]
    )


def update_monitor_properties(api, module, monitor, template_string_properties, template_integer_properties):
    changed = False
    for str_property in template_string_properties:
        if str_property['value'] is not None and not check_string_property(api, monitor, str_property):
            if not module.check_mode:
                set_string_property(api, monitor, str_property)
            changed = True
    for int_property in template_integer_properties:
        if int_property['value'] is not None and not check_integer_property(api, monitor, int_property):
            if not module.check_mode:
                set_integer_property(api, monitor, int_property)
            changed = True

    return changed


def get_ipport(api, monitor):
    return api.LocalLB.Monitor.get_template_destination(template_names=[monitor])[0]


def set_ipport(api, monitor, ipport):
    try:
        api.LocalLB.Monitor.set_template_destination(
            template_names=[monitor], destinations=[ipport]
        )
        return True, ""
    except bigsuds.OperationFailed as e:
        if "Cannot modify the address type of monitor" in str(e):
            return False, "Cannot modify the address type of monitor if already assigned to a pool."
        else:
            # genuine exception
            raise


def main():
    argument_spec = f5_argument_spec()

    meta_args = dict(
        name=dict(required=True),
        parent=dict(default=DEFAULT_PARENT_TYPE),
        parent_partition=dict(default='Common'),
        send=dict(required=False),
        receive=dict(required=False),
        receive_disable=dict(required=False),
        ip=dict(required=False),
        port=dict(required=False, type='int'),
        interval=dict(required=False, type='int'),
        timeout=dict(required=False, type='int'),
        time_until_up=dict(required=False, type='int', default=0)
    )
    argument_spec.update(meta_args)

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    server = module.params['server']
    server_port = module.params['server_port']
    user = module.params['user']
    password = module.params['password']
    state = module.params['state']
    partition = module.params['partition']
    validate_certs = module.params['validate_certs']

    parent_partition = module.params['parent_partition']
    name = module.params['name']
    parent = fq_name(parent_partition, module.params['parent'])
    monitor = fq_name(partition, name)
    send = module.params['send']
    receive = module.params['receive']
    receive_disable = module.params['receive_disable']
    ip = module.params['ip']
    port = module.params['port']
    interval = module.params['interval']
    timeout = module.params['timeout']
    time_until_up = module.params['time_until_up']

    # end monitor specific stuff

    api = bigip_api(server, user, password, validate_certs, port=server_port)
    monitor_exists = check_monitor_exists(module, api, monitor, parent)

    # ipport is a special setting
    if monitor_exists:
        cur_ipport = get_ipport(api, monitor)
        if ip is None:
            ip = cur_ipport['ipport']['address']
        if port is None:
            port = cur_ipport['ipport']['port']
    else:
        if interval is None:
            interval = 5
        if timeout is None:
            timeout = 16
        if ip is None:
            ip = '0.0.0.0'
        if port is None:
            port = 0
        if send is None:
            send = ''
        if receive is None:
            receive = ''
        if receive_disable is None:
            receive_disable = ''

    # define and set address type
    if ip == '0.0.0.0' and port == 0:
        address_type = 'ATYPE_STAR_ADDRESS_STAR_PORT'
    elif ip == '0.0.0.0' and port != 0:
        address_type = 'ATYPE_STAR_ADDRESS_EXPLICIT_PORT'
    elif ip != '0.0.0.0' and port != 0:
        address_type = 'ATYPE_EXPLICIT_ADDRESS_EXPLICIT_PORT'
    else:
        address_type = 'ATYPE_UNSET'

    ipport = {'address_type': address_type,
              'ipport': {'address': ip,
                         'port': port}}

    template_attributes = {'parent_template': parent,
                           'interval': interval,
                           'timeout': timeout,
                           'dest_ipport': ipport,
                           'is_read_only': False,
                           'is_directly_usable': True}

    # monitor specific stuff
    template_string_properties = [{'type': 'STYPE_SEND',
                                   'value': send},
                                  {'type': 'STYPE_RECEIVE',
                                   'value': receive},
                                  {'type': 'STYPE_RECEIVE_DRAIN',
                                   'value': receive_disable}]

    template_integer_properties = [
        {
            'type': 'ITYPE_INTERVAL',
            'value': interval
        },
        {
            'type': 'ITYPE_TIMEOUT',
            'value': timeout
        },
        {
            'type': 'ITYPE_TIME_UNTIL_UP',
            'value': time_until_up
        }
    ]

    # main logic, monitor generic

    try:
        result = {'changed': False}  # default

        if state == 'absent':
            if monitor_exists:
                if not module.check_mode:
                    # possible race condition if same task
                    # on other node deleted it first
                    result['changed'] |= delete_monitor(api, monitor)
                else:
                    result['changed'] |= True
        else:
            # check for monitor itself
            if not monitor_exists:
                if not module.check_mode:
                    # again, check changed status here b/c race conditions
                    # if other task already created it
                    result['changed'] |= create_monitor(api, monitor, template_attributes)
                else:
                    result['changed'] |= True

            # check for monitor parameters
            # whether it already existed, or was just created, now update
            # the update functions need to check for check mode but
            # cannot update settings if it doesn't exist which happens in check mode
            result['changed'] |= update_monitor_properties(api, module, monitor,
                                                           template_string_properties,
                                                           template_integer_properties)

            # we just have to update the ipport if monitor already exists and it's different
            if monitor_exists and cur_ipport != ipport:
                set_ipport(api, monitor, ipport)
                result['changed'] |= True
            # else: monitor doesn't exist (check mode) or ipport is already ok
    except Exception as e:
        module.fail_json(msg="received exception: %s" % e)

    module.exit_json(**result)

# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.f5_utils import *

if __name__ == '__main__':
    main()

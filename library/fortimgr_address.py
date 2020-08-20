#!/usr/bin/python
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
#

ANSIBLE_METADATA = {
    "metadata_version": "1.0",
    "status": ["preview"],
    "supported_by": "community"
}

DOCUMENTATION = '''
---
module: fortimgr_address
version_added: "2.3"
short_description: Manages Address resources and attributes
description:
  - Manages FortiManager Address configurations using jsonrpc API
author: Jacob McGill (@jmcgill298)
options:
  adom:
    description:
      - The ADOM the configuration should belong to.
    required: true
    type: str
  host:
    description:
      - The FortiManager's Address.
    required: true
    type: str
  lock:
    description:
      - True locks the ADOM, makes necessary configuration updates, saves the config, and unlocks the ADOM
    required: false
    default: True
    type: bool
  password:
    description:
      - The password associated with the username account.
    required: false
    type: str
  port:
    description:
      - The TCP port used to connect to the FortiManager if other than the default used by the transport
        method(http=80, https=443).
    required: false
    type: int
  provider:
    description:
      - Dictionary which acts as a collection of arguments used to define the characteristics
        of how to connect to the device.
      - Arguments hostname, username, and password must be specified in either provider or local param.
      - Local params take precedence, e.g. hostname is preferred to provider["hostname"] when both are specified.
    required: false
    type: dict
  session_id:
    description:
      - The session_id of an established and active session
    required: false
    type: str
  state:
    description:
      - The desired state of the specified object.
      - absent will delete resource if it exists.
      - param_absent will remove passed params from the object config if necessary and possible.
      - present will update the configuration if needed.
    required: false
    default: present
    type: str
    choices: ["absent", "param_absent", "present"]
  use_ssl:
    description:
      - Determines whether to use HTTPS(True) or HTTP(False).
    required: false
    default: True
    type: bool
  username:
    description:
      - The username used to authenticate with the FortiManager.
    required: false
    type: str
  validate_certs:
    description:
      - Determines whether to validate certs against a trusted certificate file (True), or accept all certs (False)
    required: false
    default: False
    type: bool
  address_name:
    description:
      - The name of the Address object.
    required: true
    type: str
  address_type:
    description:
      - The type of address the Address object is.
    required: false
    type: str
    choices: ["ipmask", "iprange", "fqdn", "wildcard", "wildcard-fqdn"]
  allow_routing:
    description:
      - Determines if the address can be used in static routing configuration.
    required: false
    type: str
    options: ["enable", "disable"]
  associated_intfc:
    description:
      - The interface associated with the Address.
    required: false
    type: list
  color:
    description:
      - A tag that can be used to group objects
    required: false
    type: int
  comment:
    description:
      - A comment to add to the Address
    required: false
    type: str
  end_ip:
    description:
      - The last IP associated with an Address when the type is iprange.
    required: false
    type: str
  fqdn:
    description:
      - The fully qualified domain name associated with an Address when the type is fqdn.
    required: false
    type: str
  network_address: 
    description:
      - The network address to use when address_type is ipmask.
      - The network_mask param must be used in conjuction with network_address.
      - Alternatively, the subnet param can be used for cidr notation.
    required: false
    type: str
  network_mask: 
    description:
      - The netmask to use when address_type is ipmask.
      - The network_address param must be used in conjuction with network_mask.
      - Alternatively, the subnet param can be used for cidr notation.
    required: false
    type: str
  start_ip:
    description:
      - The first IP associated with an Address when the type is iprange.
    required: false
    type: str
  subnet:
    description:
      - The subnet associated with an Address when the type is ipmask.
      - This supports sending a string as cidr notation or a two element list that
        would be returned from getting existing address objects.
      - Alternatively, the network_address and network_mask params can be used.
    required: false
    type: list
  wildcard:
    description:
      - The wildcard associated with an Address when the type is wildcard.
      - This supports sending a string as cidr notation or a two element list that
        would be returned from getting existing address objects.
      - Alternatively, the wildcard_address and wildcard_mask params can be used.
    required: false
    type: list
  wildcard_address:
    description:
      - The wildcard address to use when address_type is wildcard.
      - The wildcard_mask param must be used in conjunction with the wildcard_address.
      - Alternatively, the wildcard param can be used for cidr notation.
    required: false
    type: str
  wildcard_fqdn:
    description:
      - The wildcard FQDN associated with an Address when the type is wildcard-fqdn.
    required: false
    type: str
  wildcard_mask:
    description:
      - The wildcard mask to use when address_type is wildcard.
      - The wildcard_address param must be used in conjuction with the wildcard_mask
      - Alternatively, the wildcard param can be used for cidr notation.
    required: false
    type: str
'''

EXAMPLES = '''
- name: Add iprange Address
  fortimanager_address:
    host: "{{ ansible_host }}"
    username: "{{ ansible_user }}"
    password: "{{ ansible_password }}"
    adom: "lab"
    address_name: "server01"
    address_type: "iprange"
    associated_intfc: "any"
    comment: "App01 Server"
    start_ip: "10.10.10.21"
    end_ip: "10.10.10.26"
- name: Modify iprange Address range
  fortimanager_address:
    host: "{{ ansible_host }}"
    username: "{{ ansible_user }}"
    password: "{{ ansible_password }}"
    adom: "lab"
    address_name: "server01"
    address_type: "iprange"
    associated_intfc: "any"
    comment: "App01 Server"
    start_ip: "10.10.10.21"
    end_ip: "10.10.10.32"
- name: Add ipmask Address
  fortimanager_address:
    host: "{{ ansible_host }}"
    username: "{{ ansible_user }}"
    password: "{{ ansible_password }}"
    adom: "lab"
    port: 8443
    validate_certs: True
    state: "present"
    address_name: "server02"
    address_type: "iprange"
    subnet: "10.20.30.0/24"
- name: Add ipmask Address
  fortimanager_address:
    host: "{{ ansible_host }}"
    username: "{{ ansible_user }}"
    password: "{{ ansible_password }}"
    adom: "lab"
    port: 8443
    validate_certs: True
    state: "present"
    address_name: "server02"
    address_type: "iprange"
    network_address: "10.20.31.0"
    mask: "255.255.255.0"
- name: Delete Address
  fortimanager_address:
    host: "{{ ansible_host }}"
    username: "{{ ansible_user }}"
    password: "{{ ansible_password }}"
    use_ssl: False
    adom: "lab"
    address_name: "server02"
    state: "absent"
'''

RETURN = '''
existing:
    description: The existing configuration for the Address (uses address_name) before the task executed.
    returned: always
    type: dict
    sample: {"allow-routing": "disable", "associated-interface": ["any"], "color": 0,
             "comment": "App01 Server", "end-ip": "10.10.10.26", "name": "Server01", "start-ip": "10.10.10.21",
             "type": "iprange", "uuid": "353259f6-3caf-51e7-ad56-13759b17ff46", "visibility": "enable"}
config:
    description: The configuration that was pushed to the FortiManager.
    returned: always
    type: dict
    sample: {"end-ip": "10.10.10.32", "name": "Server01"}
locked:
    description: The status of the ADOM lock command
    returned: When lock set to True
    type: bool
    sample: True
saved:
    description: The status of the ADOM save command
    returned: When lock set to True
    type: bool
    sample: True
unlocked:
    description: The status of the ADOM unlock command
    returned: When lock set to True
    type: bool
    sample: True
'''

import time

import requests
from ansible import __version__ as ansible_version
if float(ansible_version[:3]) < 2.4:
    raise ImportError("Ansible versions below 2.4 are not supported")
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.six import string_types
from ansible.module_utils.fortimgr_fortimanager import FortiManager
from ansible.module_utils.fortimgr_fmaddress import FMAddress


requests.packages.urllib3.disable_warnings()


def main():
    base_argument_spec = dict(
        adom=dict(required=False, type="str"),
        host=dict(required=False, type="str"),
        lock=dict(required=False, type="bool"),
        password=dict(fallback=(env_fallback, ["ANSIBLE_NET_PASSWORD"]), no_log=True),
        port=dict(required=False, type="int"),
        session_id=dict(required=False, type="str"),
        state=dict(choices=["absent", "param_absent", "present"], type="str"),
        use_ssl=dict(required=False, type="bool"),
        username=dict(fallback=(env_fallback, ["ANSIBLE_NET_USERNAME"])),
        validate_certs=dict(required=False, type="bool"),
        address_name=dict(required=False, type="str"),
        address_type=dict(choices=["ipmask", "iprange", "fqdn", "wildcard", "wildcard-fqdn"],
                          required=False, type="str"),
        allow_routing=dict(choices=["enable", "disable"], required=False, type="str"),
        associated_intfc=dict(required=False, type="list"),
        color=dict(required=False, type="int"),
        comment=dict(required=False, type="str"),
        end_ip=dict(required=False, type="str"),
        fqdn=dict(required=False, type="str"),
        network_address=dict(required=False, type="str"),
        network_mask=dict(required=False, type="str"),
        start_ip=dict(required=False, type="str"),
        subnet=dict(required=False, type="list"),
        wildcard=dict(required=False, type="list"),
        wildcard_address=dict(required=False, type="str"),
        wildcard_fqdn=dict(required=False, type="str"),
        wildcard_mask=dict(required=False, type="str")
    )
    argument_spec = base_argument_spec
    argument_spec["provider"] = dict(required=False, type="dict", options=base_argument_spec)

    module = AnsibleModule(argument_spec, supports_check_mode=True,
                           required_together=[["network_address", "network_mask"], ["wildcard_address", "wildcard_mask"]],
                           mutually_exclusive=[["network_address", "subnet"], ["wildcard", "wildcard_address"]])

    provider = module.params["provider"] or {}

    # allow local params to override provider
    for param, pvalue in provider.items():
        if module.params.get(param) is None:
            module.params[param] = pvalue

    # handle params passed via provider and insure they are represented as the data type expected by fortimanager
    adom = module.params["adom"]
    host = module.params["host"]
    lock = module.params["lock"]
    if lock is None:
        module.params["lock"] = True
    password = module.params["password"]
    port = module.params["port"]
    session_id = module.params["session_id"]
    state = module.params["state"]
    if state is None:
        state = "present"
    use_ssl = module.params["use_ssl"]
    if use_ssl is None:
        use_ssl = True
    username = module.params["username"]
    validate_certs = module.params["validate_certs"]
    if validate_certs is None:
        validate_certs = False
    address_name = module.params["address_name"]
    associated_intfc = module.params["associated_intfc"]
    if isinstance(associated_intfc, str):
        associated_intfc = [associated_intfc]
    color = module.params["color"]
    if isinstance(color, str):
        color = int(color)
    network_address = module.params["network_address"]
    network_mask = module.params["network_mask"]
    subnet = module.params["subnet"]
    if isinstance(subnet, str):
        subnet = [subnet]
    wildcard = module.params["wildcard"]
    if isinstance(wildcard, str):
        wildcard = [wildcard]
    wildcard_address = module.params["wildcard_address"]
    wildcard_mask = module.params["wildcard_mask"]

    # validate required arguments are passed; not used in argument_spec to allow params to be called from provider
    argument_check = dict(adom=adom, host=host, address_name=address_name)
    for key, val in argument_check.items():
        if not val:
            module.fail_json(msg="{} is required".format(key))

    # validate address parameters are passed correctly
    if subnet and (network_address or network_mask):
        module.fail_json(msg="The subnet parameter cannot be used with the network_address and network_mask parameters")
    elif wildcard and (wildcard_address or wildcard_mask):
        module.fail_json(msg="The wildcard parameter cannot be used with the wildcard_address and wildcard_mask parameters")
    elif network_address and not network_mask:
        module.fail_json(msg="The network_address and network_mask parameters must be provided together; missing network_mask.")
    elif network_mask and not network_address:
        module.fail_json(msg="The network_address and network_mask parameters must be provided together; missing network_address.")
    elif wildcard_address and not wildcard_mask:
        module.fail_json(msg="The wildcard_address and wildcard_mask parameters must be provided together; missing wildcard_mask.")
    elif wildcard_mask and not wildcard_address:
        module.fail_json(msg="The wildcard_address and wildcard_mask parameters must be provided together; missing wildcard_address.")

    # use subnet variables to normalize the subnet into a list that fortimanager expects
    if subnet and len(subnet) == 1 and "/" in subnet[0]:
        subnet = FortiManager.cidr_to_network(subnet[0])
        if not subnet:
            module.fail_json(msg="The prefix must be a value between 0 and 32")
    elif subnet and len(subnet) == 1:
        subnet.append("255.255.255.255")
    elif network_address and network_mask:
        subnet = [network_address, network_mask]

    # use wildcard variables to normalize the wildcard into a list that fortimanager expects
    if wildcard and "/" in wildcard[0]:
        wildcard = FortiManager.cidr_to_wildcard(wildcard[0])
        if not wildcard:
            module.fail_json(msg="The prefix must be a value between 0 and 32")
    elif wildcard_address and wildcard_mask:
        wildcard = [wildcard_address, wildcard_mask]

    args = {
        "allow-routing": module.params["allow_routing"],
        "associated-interface": associated_intfc,
        "color": color,
        "comment": module.params["comment"],
        "end-ip": module.params["end_ip"],
        "fqdn": module.params["fqdn"],
        "name": address_name,
        "start-ip": module.params["start_ip"],
        "subnet": subnet,
        "type": module.params["address_type"],
        "wildcard": wildcard,
        "wildcard-fqdn": module.params["wildcard_fqdn"]
    }

    # "if isinstance(v, bool) or v" should be used if a bool variable is added to args
    proposed = dict((k, v) for k, v in args.items() if v)

    kwargs = dict()
    if port:
        kwargs["port"] = port

    # validate successful login or use established session id
    session = FMAddress(host, username, password, use_ssl, validate_certs, adom, **kwargs)
    if not session_id:
        session_login = session.login()
        if not session_login.json()["result"][0]["status"]["code"] == 0:
            module.fail_json(msg="Unable to login", fortimanager_response=session_login.json())
    else:
        session.session = session_id

    # get existing configuration from fortimanager and make necessary changes
    existing = session.get_item(proposed["name"])
    if state == "present":
        results = session.config_present(module, proposed, existing)
    elif state == "absent":
        results = session.config_absent(module, proposed, existing)
    else:
        results = session.config_param_absent(module, proposed, existing)

    # if module has made it this far and lock set, then all related return values are true
    if module.params["lock"] and results["changed"]:
        locked = dict(locked=True, saved=True, unlocked=True)
        results.update(locked)

    # logout, build in check for future logging capabilities
    if not session_id:
        session_logout = session.logout()
        # if not session_logout.json()["result"][0]["status"]["code"] == 0:
        #     results["msg"] = "Completed tasks, but unable to logout of FortiManager"
        #     module.fail_json(**results)

    return module.exit_json(**results)


if __name__ == "__main__":
    main()


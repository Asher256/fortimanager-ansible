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
module: fortimgr_address_group
version_added: "2.3"
short_description: Manages Address Group resources and attributes
description:
  - Manages FortiManager Address Group configurations using jsonrpc API
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
      - absent will delete the object if it exists.
      - param_absent will remove passed params from the object config if necessary and possible.
      - present will create the configuration if needed.
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
  address_group_name:
    description:
      - The name of the Address Group object.
    required: true
    type: str
  allow_routing:
    description:
      - Determines if the address can be used in static routing configuration.
    required: false
    type: str
    options: ["enable", "disable"]
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
  members:
    description:
      - A list of members associated with the Address Group object.
    required: false
    type: str
'''

EXAMPLES = '''
- name: Add Address Group
  fortimgr_address_group:
    host: "{{ ansible_host }}"
    username: "{{ ansible_user }}"
    password: "{{ ansible_password }}"
    adom: "lab"
    address_group_name: "App01_Servers"
    comment: "App01 Servers"
    members:
      - "Server01"
      - "Server02"
      - "Server03"
- name: Add Address to Address Group
  fortimgr_address_group:
    host: "{{ ansible_host }}"
    username: "{{ ansible_user }}"
    password: "{{ ansible_password }}"
    adom: "lab"
    address_group_name: "App01_Servers"
    members: "Server04"
- name: Remove Address from Address Group
  fortimgr_address_group:
    host: "{{ ansible_host }}"
    username: "{{ ansible_user }}"
    password: "{{ ansible_password }}"
    adom: "lab"
    port: 8443
    validate_certs: True
    address_group_name: "App01_Servers"
    state: "param_absent"
    members:
      - "Server01"
      - "Server02"
- name: Delete Address Group
  fortimgr_address_group:
    host: "{{ ansible_host }}"
    username: "{{ ansible_user }}"
    password: "{{ ansible_password }}"
    use_ssl: False
    adom: "lab"
    address_group_name: "App01_Servers"
    state: "absent"
'''

RETURN = '''
existing:
    description: The existing configuration for the Address Group (uses address_group_name) before the task executed.
    returned: always
    type: dict
    sample: {"allow-routing": "disable", "color": 0, "comment": "", "member": ["Server01"],
             "name": "App01_Servers", "uuid": "1bb2fc36-4d4b-51e7-64b5-911230d8301f", "visibility": "enable"}
config:
    description: The configuration that was pushed to the FortiManager.
    returned: always
    type: dict
    sample: {"method": "update", "params": [{"data": [{"member": ["Server02"], "name": "App01_Servers"}],
             "url": "/pm/config/adom/lab/obj/firewall/addrgrp"}]}
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


requests.packages.urllib3.disable_warnings()


class FMAddressGroup(FortiManager):
    """
    This is the class used for interacting with the "address group" API Endpoint. In addition to address group specific
    methods, the api endpoint default value is set to "addrgrp."
    """

    def __init__(self, host, user, passw, use_ssl=True, verify=False, adom="", package="", api_endpoint="addrgrp",
                 **kwargs):
        super(FMAddressGroup, self).__init__(host, user, passw, use_ssl, verify, adom, package, api_endpoint, **kwargs)


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
        address_group_name=dict(required=False, type="str"),
        allow_routing=dict(choices=["enable", "disable"], required=False, type="str"),
        color=dict(required=False, type="int"),
        comment=dict(required=False, type="str"),
        members=dict(required=False, type="list")
    )
    argument_spec = base_argument_spec
    argument_spec["provider"] = dict(required=False, type="dict", options=base_argument_spec)

    module = AnsibleModule(argument_spec, supports_check_mode=True)
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
    address_group_name = module.params["address_group_name"]
    color = module.params["color"]
    if isinstance(color, str):
        color = int(color)
    members = module.params["members"]
    if isinstance(members, str):
        members = [members]

    # validate required arguments are passed; not used in argument_spec to allow params to be called from provider
    argument_check = dict(adom=adom, host=host, address_group_name=address_group_name)
    for key, val in argument_check.items():
        if not val:
            module.fail_json(msg="{} is required".format(key))

    args = {
        "allow-routing": module.params["allow_routing"],
        "color": color,
        "comment": module.params["comment"],
        "member": members,
        "name": address_group_name
    }

    # "if isinstance(v, bool) or v" should be used if a bool variable is added to args
    proposed = dict((k, v) for k, v in args.items() if v)

    kwargs = dict()
    if port:
        kwargs["port"] = port

    # validate successful login or use established session id
    session = FMAddressGroup(host, username, password, use_ssl, validate_certs, adom, **kwargs)
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


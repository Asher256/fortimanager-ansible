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
module: fortimgr_ip_pool_map
version_added: "2.3"
short_description: Manages IP Pool mapped resources and attributes
description:
  - Manages FortiManager IP Pool dynamic_mapping configurations using jsonrpc API
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
      - absent will delete the mapping from the object if it exists.
      - param_absent will remove passed params from the object config if necessary and possible.
      - present will create configuration for the mapping correlating to the fortigate specified if needed.
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
  arp_intfc:
    description:
      - Sets the interface which should reply for ARP if arp_reply is enabled.
    required: false
    type: str
  arp_reply:
    description:
      - Allows the fortigate to reply to ARP requests.
    required: false
    type: str
    choices: ["enable", "disable"]
  comment:
    description:
      - A comment to add to the IP Pool.
    required: false
    type: str
  end_ip:
    description:
      - The last address in the range of external addresses used to NAT internal addresses to.
    required: false
    type: str
  fortigate:
    description:
      - The name of the fortigate to map the configuration to.
    required: false
    type: str
  permit_any_host:
    description:
      - Allows for the use fo full cone NAT.
    required: false
    type: str
    choices: ["enable", "disable"]
  pool_name:
    description:
      - The name of the IP Pool.
    required: true
    type: str
  source_end_ip:
    description:
      - The last address in the range of internal addresses which will be NAT'ed to an address in the external range.
    required: false
    type: str
  source_start_ip:
    description:
      - The first address in the range of internal addresses which will be NAT'ed to an address in the external range.
    required: false
    type: str
  start_ip:
    description:
      - The first address in the range of external addresses used to NAT internal addresses to.
    required: false
    type: str
  type:
    description:
      - The type of NAT the IP Pool will perform
    required: false
    type: str
    choices: ["overload", "one-to-one", "fixed-port-range", "port-block-allocation"]
  vdom:
    description:
      - The vdom on the fortigate that the config should be associated to.
    required: true
    type: str
'''

EXAMPLES = '''
- name: Add IP Pool Map
  fortimgr_ip_pool_map:
    host: "{{ ansible_host }}"
    username: "{{ ansible_user }}"
    password: "{{ ansible_password }}"
    adom: "lab"
    fortigate: "{{ item.fg }}"
    vdom: "root"
    pool_name: "App01_Pool"
    type: "overload"
    start_ip: "{{ item.start }}"
    end_ip: "{{ item.end }}"
    comment: "App01 Pool"
  with_items:
    - fg: "lab01_fortigate"
      start: "100.10.10.10"
      end: "100.10.10.10"
    - fg: "lab02_fortigate"
      start: "100.10.12.10"
      end: "100.10.12.10"
- name: Modify IP Pool Map
  fortimgr_ip_pool_map:
    host: "{{ ansible_host }}"
    username: "{{ ansible_user }}"
    password: "{{ ansible_password }}"
    adom: "lab"
    fortigate: "{{ item.fg }}"
    vdom: root
    pool_name: "App01_Pool"
    validate_certs: True
    port: 8443
    end_ip: "{{ item.end }}"
  with_items:
    - fg: "lab01_fortigate"
      end: "100.10.10.11"
    - fg: "lab02_fortigate"
      end: "100.10.12.11"
- name: Add Mapping to IP Pool
  fortimgr_ip_pool_map:
    host: "{{ ansible_host }}"
    username: "{{ ansible_user }}"
    password: "{{ ansible_password }}"
    adom: "lab"
    fortigate: "lab03_fortigate"
    vdom: "root"
    pool_name: "App01_Pool"
    start_ip: "100.10.14.10"
    end_ip: "100.10.14.11"
- name: Remove Mapping from IP Pool
  fortimgr_ip_pool_map:
    host: "{{ ansible_host }}"
    username: "{{ ansible_user }}"
    password: "{{ ansible_password }}"
    adom: "lab"
    fortigate: "lab01_fortigate"
    vdom: "root"
    pool_name: "App01_Pool"
'''

RETURN = '''
existing:
    description: The existing dynamic_mapping configuration for the IP Pool (uses pool_name) before the task executed.
    returned: always
    type: dict
    sample: {"dynamic_mapping": [{"_scope": [{"name": "Prod", "vdom": "root"}], "arp-reply": "enable",
             "block-size": 128, "comments": "", "endip": "10.20.20.10", "num-blocks-per-user": 8, "permit-any-host":
             "disable", "source-endip": "0.0.0.0", "source-startip": "0.0.0.0", "startip": "10.20.20.10",
             "type": "overload"}], "name": "ippool-10.20.20.10"}
config:
    description: The configuration that was pushed to the FortiManager.
    returned: always
    type: dict
    sample: {"method": "update", "params": [{"data": {"dynamic_mapping": [{"_scope": [{"name": "DR", "vdom": "root"}],
             "startip": "10.10.10.10", "endip": "10.10.10.10", "type": "overload"}, {"_scope": [{"name":
             "Prod", "vdom": "root"}]}], "name": "App01_Pool"},
             "url": "/pm/config/adom/lab/obj/firewall/ippool"}]}
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


class FMPool(FortiManager):
    """
    This is the class used for interacting with the "ip pool" API Endpoint. In addition to service specific
    methods, the api endpoint default value is set to "ippool."
    """

    def __init__(self, host, user, passw, use_ssl=True, verify=False, adom="", package="",
                 api_endpoint="ippool", **kwargs):
        super(FMPool, self).__init__(host, user, passw, use_ssl, verify, adom, package, api_endpoint, **kwargs)

    @staticmethod
    def get_diff_add(proposed, existing):
        """
        This method is used to get the difference between two configurations when the "proposed" configuration is a dict
        of configuration items that should exist in the configuration for the object in the FortiManager. Either the
        get_item or get_item_fields methods should be used to obtain the "existing" variable; if either of those methods
        return an empty dict, then you should use the add_config method to add the new object.

        :param proposed: Type dict.
                         The configuration that should not exist for the object on the FortiManager.
        :param existing: Type dict.
                         The current configuration for the object that potentially needs configuration removed.
        :return: A dict corresponding to the "data" portion of an "update" request. This can be used to call the
                 update_config method.
        """
        config = {}
        replace = ["arp-intf"]
        for field in proposed.keys():
            proposed_field = proposed[field]
            existing_field = existing.get(field)
            if existing_field and proposed_field != existing_field:
                if field in replace:
                    config[field] = proposed_field
                elif isinstance(existing_field, list):
                    proposed_field = set(proposed_field)
                    if not proposed_field.issubset(existing_field):
                        config[field] = list(proposed_field.union(existing_field))
                elif isinstance(existing_field, dict):
                    config[field] = dict(set(proposed_field.items()).union(existing_field.items()))
                elif isinstance(existing_field, int) or isinstance(existing_field, string_types):
                    config[field] = proposed_field
            elif field not in existing:
                config[field] = proposed_field

        if config:
            config["name"] = proposed["name"]

        return config


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
        arp_intfc=dict(required=False, type="str"),
        arp_reply=dict(choices=["enable", "disable"], required=False, type="str"),
        comment=dict(required=False, type="str"),
        end_ip=dict(required=False, type="str"),
        fortigate=dict(required=False, type="str"),
        permit_any_host=dict(choices=["enable", "disable"], required=False, type="str"),
        pool_name=dict(required=False, type="str"),
        source_end_ip=dict(required=False, type="str"),
        source_start_ip=dict(required=False, type="str"),
        start_ip=dict(required=False, type="str"),
        type=dict(choices=["overload", "one-to-one", "fixed-port-range", "port-block-allocation"],
                  required=False, type="str"),
        vdom=dict(required=False, type="str")
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
    fortigate = module.params["fortigate"]
    pool_name = module.params["pool_name"]
    vdom = module.params["vdom"]

    # validate required arguments are passed; not used in argument_spec to allow params to be called from provider
    argument_check = dict(adom=adom, fortigate=fortigate, host=host, pool_name=pool_name, vdom=vdom)
    for key, val in argument_check.items():
        if not val:
            module.fail_json(msg="{} is required".format(key))

    args = {
        "arp-intf": module.params["arp_intfc"],
        "arp-reply": module.params["arp_reply"],
        "comments": module.params["comment"],
        "name": pool_name,
        "endip": module.params["end_ip"],
        "fortigate": fortigate,
        "permit-any-host": module.params["permit_any_host"],
        "source-endip": module.params["source_end_ip"],
        "source-startip": module.params["source_start_ip"],
        "startip": module.params["start_ip"],
        "type": module.params["type"],
        "vdom": vdom
    }

    # "if isinstance(v, bool) or v" should be used if a bool variable is added to args
    proposed_args = dict((k, v) for k, v in args.items() if v)

    proposed = dict(
        name=proposed_args.pop("name"),
        dynamic_mapping=[{
            "_scope": [{
                "name": proposed_args.pop("fortigate"),
                "vdom": proposed_args.pop("vdom")
            }],
        }]
    )

    for k, v in proposed_args.items():
        proposed["dynamic_mapping"][0][k] = v

    kwargs = dict()
    if port:
        kwargs["port"] = port

    # validate successful login or use established session id
    session = FMPool(host, username, password, use_ssl, validate_certs, adom, **kwargs)
    if not session_id:
        session_login = session.login()
        if not session_login.json()["result"][0]["status"]["code"] == 0:
            module.fail_json(msg="Unable to login", fortimanager_response=session_login())
    else:
        session.session = session_id

    # get existing configuration from fortimanager and make necessary changes
    existing = session.get_item_fields(proposed["name"], ["name", "dynamic_mapping"])
    if state == "present":
        # If no pre-existing ip pool entry, we need to set _if_no_default to 1
        # (GUI option "configure default value" = off)
        # to be able to create a IP Pool with only dynamimc mappings and no default nat range.
        # This behavior changed somewhere around FMG version 6.0.5.
        if not existing:
            proposed[ "_if_no_default"] = 1
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


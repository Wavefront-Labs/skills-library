---
id: computing-software.systems-network-administration.cisco-networking.netconf-with-ncclient
name: netconf-with-ncclient
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ios-xe, netconf, ncclient, yang, yang-model, netconf-yang, edit-config, get-config, candidate-datastore, xml-filter, python, network-programmability, port-830]
level: practitioner
status: draft
description: "Automate IOS XE over NETCONF with Python ncclient: enable netconf-yang, connect on 830, subtree filters, edit-config merge/replace, candidate datastore with confirmed commit."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/prog/configuration/1712/b_1712_programmability_cg/m_1712_prog_yang_netconf.html
  - https://ncclient.readthedocs.io/en/latest/
  - https://datatracker.ietf.org/doc/html/rfc6241
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NETCONF with ncclient

NETCONF (RFC 6241) runs over SSH (TCP 830) with XML RPCs: get, get-config, edit-config,
lock, commit. Unlike RESTCONF it supports **transactions** (candidate datastore, confirmed
commit) on platforms that enable them.

## Enable on IOS XE
```
netconf-yang
netconf-yang feature candidate-datastore     ! optional; changes require commit
username api privilege 15 secret <API_SECRET>
aaa authorization exec default local
```

## Connect and read
```python
from ncclient import manager
with manager.connect(host="10.0.0.5", port=830, username="api", password=SECRET,
                     hostkey_verify=False, device_params={"name": "iosxe"}, timeout=60) as m:
    print([c for c in m.server_capabilities if "Cisco-IOS-XE-native" in c][:1])
    flt = """<filter><native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
               <hostname/></native></filter>"""
    print(m.get_config(source="running", filter=flt).data_xml)
```
Use subtree filters always: an unfiltered get-config returns the full config as XML and is slow.

## Change config
```python
cfg = """<config><native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
  <interface><Loopback><name>101</name><description>netconf</description>
  <ip><address><primary><address>10.101.0.1</address><mask>255.255.255.255</mask></primary></address></ip>
  </Loopback></interface></native></config>"""
m.edit_config(target="running", config=cfg)        # default-operation merge
```
`operation="replace"` or `"delete"` attributes on an element (`xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete"`) target that subtree only.

## Candidate datastore and confirmed commit
```python
with m.locked("candidate"):
    m.edit_config(target="candidate", config=cfg)
    m.commit(confirmed=True, timeout="120")    # auto-rollback in 120 s unless confirmed
    # ... verify reachability ...
    m.commit()                                 # confirm
```
`m.discard_changes()` drops candidate edits.

## Gotchas
- Errors come back as `RPCError` with `rpc-error` XML: read `error-path` and `error-message`.
- Namespace must match the module exactly; get it from capabilities or YANG Suite.
- NETCONF changes are not saved to startup-config automatically: call the
  `<cisco-ia:save-config xmlns:cisco-ia="http://cisco.com/yang/cisco-ia"/>` RPC via
  `m.dispatch(...)`, or `copy run start`.
- The datastore sync can lag after CLI changes; `show netconf-yang datastores` shows sync state.

## Verify
- [ ] `ssh -s api@10.0.0.5 -p 830 netconf` prints a hello with capabilities.
- [ ] Script edit appears in `show run`; confirmed commit rolls back if not confirmed.

---
id: computing-software.systems-network-administration.cisco-networking.netconf-subtree-and-xpath-filters
name: netconf-subtree-and-xpath-filters
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, netconf, subtree-filter, xpath-filter, ncclient, yang, get-config, ios-xe, model-driven-programmability]
level: practitioner
status: draft
description: "Retrieve only what you need over NETCONF with subtree and XPath filters: syntax, namespaces, ncclient examples and IOS XE support details."
sources:
  - https://datatracker.ietf.org/doc/html/rfc6241#section-6
  - https://ncclient.readthedocs.io/en/latest/manager.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/prog/configuration/1712/b_1712_programmability_cg/m_1712_prog_yang_netconf.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NETCONF subtree and XPath filters

## Why filter
A `<get-config>` without a filter returns the whole running config as XML (MBs on big boxes);
`<get>` without a filter returns all operational data too, which can take minutes.

## Subtree filter (RFC 6241 section 6, mandatory for servers)
Selection by example XML: containment nodes, selection nodes (empty element) and content-match nodes (with value).
```xml
<filter type="subtree">
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name>GigabitEthernet1</name>   <!-- content match: only this interface -->
      <enabled/>                      <!-- selection: only this leaf -->
    </interface>
  </interfaces>
</filter>
```

## XPath filter (capability `:xpath`)
```xml
<filter type="xpath"
  xmlns:if="urn:ietf:params:xml:ns:yang:ietf-interfaces"
  select="/if:interfaces/if:interface[if:name='GigabitEthernet1']/if:enabled"/>
```
IOS XE advertises `urn:ietf:params:netconf:capability:xpath:1.0` (check the hello). XPath support is
a subset: predicates on keys work; complex functions may not.

## ncclient
```python
from ncclient import manager
with manager.connect(host="<DEVICE>", port=830, username="<USER>", password="<PW>",
                     hostkey_verify=False, device_params={"name": "iosxe"}) as m:
    sub = """<interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
               <interface><name>GigabitEthernet1</name></interface></interfaces>"""
    r = m.get_config(source="running", filter=("subtree", sub))
    x = m.get(filter=("xpath", ("/if:interfaces-state", {"if": "urn:ietf:params:xml:ns:yang:ietf-interfaces"})))
    print(r.data_xml)
```
For XPath with prefixes, pass a `(namespaces_dict, xpath)` tuple per ncclient docs or declare the
prefix in the filter element.

## Gotchas
- Wrong namespace = empty `<data/>` reply, not an error. Copy the namespace from the module.
- Native model root: `<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">`.
- Filters on non-key leaves (content match) can be slow on large lists.

## Verify
- [ ] The reply contains only the selected subtree; size small enough for the automation loop.

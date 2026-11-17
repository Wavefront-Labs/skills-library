---
id: computing-software.systems-network-administration.cisco-networking.restconf-requests-on-ios-xe
name: restconf-requests-on-ios-xe
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ios-xe, restconf, restconf-api, rest-api, yang, yang-model, json-encoding, network-json, curl, python-requests, cisco-ios-xe-native, ietf-interfaces, http-methods, network-programmability]
level: practitioner
status: draft
description: "Read and change IOS XE config over RESTCONF: enabling it, URL structure, JSON payloads with native and IETF YANG models, GET/PATCH/PUT/DELETE semantics, curl and Python examples."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/prog/configuration/1712/b_1712_programmability_cg/m_1712_prog_restconf.html
  - https://datatracker.ietf.org/doc/html/rfc8040
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RESTCONF on IOS XE

RESTCONF (RFC 8040) exposes YANG-modelled config and state over HTTPS with JSON or XML.

## Enable
```
username api privilege 15 secret <API_SECRET>
aaa new-model
aaa authentication login default local
aaa authorization exec default local
ip http secure-server
restconf
```
Check `show platform software yang-management process` (confd, nesd, syncfd running).

## URL structure
`https://<DEVICE>/restconf/data/<module>:<container>/<list>=<key>`
Headers: `Accept: application/yang-data+json`, `Content-Type: application/yang-data+json`.
```
# Read hostname (native model)
curl -sk -u api:<API_SECRET> -H 'Accept: application/yang-data+json' \
  https://10.0.0.5/restconf/data/Cisco-IOS-XE-native:native/hostname
# Interfaces, IETF model (interface names URL-encoded: / -> %2F)
curl -sk -u api:<API_SECRET> -H 'Accept: application/yang-data+json' \
  'https://10.0.0.5/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet1%2F0%2F10'
```

## Change config
```
curl -sk -u api:<API_SECRET> -X PATCH \
  -H 'Content-Type: application/yang-data+json' -H 'Accept: application/yang-data+json' \
  https://10.0.0.5/restconf/data/ietf-interfaces:interfaces \
  -d '{"ietf-interfaces:interfaces":{"interface":[{"name":"Loopback100","type":"iana-if-type:softwareLoopback","enabled":true,
       "ietf-ip:ipv4":{"address":[{"ip":"10.100.0.1","netmask":"255.255.255.255"}]}}]}}'
```
| Method | Semantics |
|---|---|
| GET | read |
| POST | create a child that must not exist (409 if it does) |
| PUT | create or **replace** the target entirely (dangerous at high levels) |
| PATCH | merge into the target |
| DELETE | remove the target |
A PUT on `Cisco-IOS-XE-native:native` replaces the whole running config. Use PATCH or target the
narrowest resource.

## Python
```python
import requests
r = requests.get(url, auth=("api", secret), verify=False,   # use a CA bundle in production
                 headers={"Accept": "application/yang-data+json"})
r.raise_for_status(); print(r.json())
```
Responses: 200/201/204 success, 400 bad payload (read the error-message), 404 path not
found (wrong module prefix or key), 409 exists.

## Discover paths
GET `/restconf/data/ietf-yang-library:modules-state` lists supported modules; use YANG Suite
or `pyang -f tree` on Cisco's model repo (github.com/YangModels/yang/vendor/cisco/xe/<release>).
Or configure via CLI and GET the native subtree to see the JSON shape.

## Verify
- [ ] GET on hostname returns JSON; PATCH creates the loopback; `show run int Lo100` agrees.
- [ ] Changes are in running-config only: save with `copy run start` or the `cisco-ia:save-config` RPC.

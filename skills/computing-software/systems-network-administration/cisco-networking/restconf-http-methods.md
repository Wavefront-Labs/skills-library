---
id: computing-software.systems-network-administration.cisco-networking.restconf-http-methods
name: restconf-http-methods
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ios-xe, restconf, restconf-methods, patch, put, yang, rest-api]
level: practitioner
status: draft
description: "Use RESTCONF methods correctly on IOS XE: GET with depth and fields, POST to create, PUT to replace, PATCH to merge, DELETE, and the status codes and pitfalls of each."
sources:
  - https://www.rfc-editor.org/rfc/rfc8040#section-4
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RESTCONF HTTP methods

Base URL on IOS XE: `https://<device>/restconf/data/`, headers
`Accept: application/yang-data+json` and `Content-Type: application/yang-data+json`.

## GET (read)
```
curl -sk -u admin:pw -H 'Accept: application/yang-data+json' \
  'https://10.0.0.1/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet=1'
curl ... 'https://10.0.0.1/restconf/data/ietf-interfaces:interfaces?depth=2'
curl ... 'https://10.0.0.1/restconf/data/Cisco-IOS-XE-native:native/hostname'
curl ... 'https://10.0.0.1/restconf/data/ietf-interfaces:interfaces-state/interface=GigabitEthernet1?fields=statistics(in-octets;out-octets)'
```
List keys go in the path after `=`; slashes in keys are URL-encoded (`GigabitEthernet=1%2F0%2F1`
for Gi1/0/1 in the native model).

## POST (create a child; fails if it exists)
```
curl -sk -u admin:pw -X POST -H 'Content-Type: application/yang-data+json' \
  https://10.0.0.1/restconf/data/Cisco-IOS-XE-native:native/interface \
  -d '{"Cisco-IOS-XE-native:Loopback":{"name":10,"ip":{"address":{"primary":{"address":"10.10.10.1","mask":"255.255.255.255"}}}}}'
```
201 Created; 409 Conflict if it already exists.

## PATCH (merge)
Changes only the supplied leaves; everything else stays. Safest for incremental changes.
```
curl ... -X PATCH .../native/interface/Loopback=10 -d '{"Cisco-IOS-XE-native:Loopback":{"name":10,"description":"mgmt"}}'
```
204 No Content on success.

## PUT (replace)
Replaces the target resource entirely with the body: leaves you omit are deleted. A PUT on
`/native/interface/GigabitEthernet=1` without the IP address removes the IP address. A PUT on
`/native` replaces the whole configuration. Use PUT only when you send the full desired state.

## DELETE
```
curl ... -X DELETE .../native/interface/Loopback=10
```
204 on success, 404 if missing.

## Status codes
200 OK (GET), 201 Created, 204 No Content, 400 malformed/invalid value, 401 auth, 404 resource
missing, 409 exists (POST) or locked datastore, 412/428 precondition issues.

## Gotchas
- RESTCONF changes the running config; `write memory` is still needed (POST to
  `/restconf/operations/cisco-ia:save-config`).
- Large GETs on `native` are slow; use specific paths, `depth`, `fields`.

## Verify
- [ ] After PATCH, a GET of the resource shows the change and other leaves untouched.

---
id: computing-software.systems-network-administration.dns-dhcp.kea-custom-option-definitions
name: kea-custom-option-definitions
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, kea, kea-dhcp4, option-def, option-data, custom-options, vendor-encapsulated-options, option-43, option-space, csv-format, always-send, option-121, classless-static-routes]
level: advanced
status: verified
description: "Send non-standard DHCP options from Kea: option-def types and arrays, option spaces and vendor option 43, always-send, csv-format vs raw hex, capture checks."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html#custom-dhcpv4-options
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html#dhcpv4-vendor-specific-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kea custom option definitions

Standard options (routers, domain-name-servers, ntp-servers, classless-static-route 121, tftp
server 66, boot-file-name 67, vendor-encapsulated-options 43 ...) are pre-defined: use `option-data`
by name. Define new ones only for codes Kea does not know.

## Define and send a custom option
```json
"option-def": [
  {"name": "provisioning-url", "code": 224, "type": "string", "space": "dhcp4"},
  {"name": "tftp-server-list", "code": 150, "type": "ipv4-address", "array": true, "space": "dhcp4"}
],
"option-data": [
  {"name": "provisioning-url", "data": "https://prov.example.org/cfg"},
  {"name": "tftp-server-list", "data": "10.0.0.69, 10.0.0.70"}
]
```
Types (ARM table): `uint8/16/32`, `int8/16/32`, `boolean`, `ipv4-address`, `ipv6-address`,
`ipv6-prefix`, `psid`, `string`, `fqdn`, `binary`, `empty`, `tuple`, `record` (with `record-types`
for structured options, no nested `record` or `empty`), `array: true` (applies to the last field of
a record). Option 150 is not in Kea's standard DHCPv4 option table, so it needs a definition.
Codes 224-254 are reserved for private use.

## Raw hex
With `"csv-format": false` the `data` is hex, either delimited octets separated by spaces or
colons (`"C0 00 03 01"`, `"ab:cd:ef"`) or a continuous digit string with or without a `0x` prefix
(`"0xabcdef"`, `"abcdef"`).
The ARM warns Kea cannot validate hex content, so check the capture. A binary option can also
be given as a single-quoted string inside the JSON string: `"data": "'some text'"`.
Option 43 is special: the built-in last-resort definition of option 43 is not compatible with a
raw binary value, so for raw 43 the ARM says to define a client class that matches those clients
and carries an option-def for option 43 with type `binary` and no encapsulation.

## Vendor-encapsulated options with an option space
```json
"option-def": [{"name": "controller-list", "code": 241, "space": "acme-ap", "type": "ipv4-address", "array": true},
               {"name": "vendor-encapsulated-options", "code": 43, "type": "empty", "encapsulate": "acme-ap"}],
"client-classes": [{"name": "acme-ap", "test": "substring(option[60].text,0,8) == 'ACME-AP '",
  "option-data": [{"name": "vendor-encapsulated-options"},
                  {"name": "controller-list", "space": "acme-ap", "data": "10.10.10.10, 10.10.10.11"}]}]
```
Scope option 43 to a class: different vendors interpret 43 differently. Option definitions inside
client classes are allowed only for option 43 and codes 224-254 (DHCPv4 only). Option 43 is
unpacked after classification, so clients cannot be classified by 43 sub-options. For output the
class definition wins over the global one, which wins over the built-in last-resort one.

## always-send / never-send
Defined options are added when the client requests them in option 55 (Parameter Request List),
with a few exceptions that are always added. `always-send: true` forces it (needed for devices
that do not request the option, e.g. some phones/APs); `never-send: true` stops the server adding
it, as if the client had removed the code from option 55.

## Verify
- [ ] `kea-dhcp4 -t` accepts the config; packet capture of the OFFER/ACK shows the option bytes as intended.
- [ ] The device acts on the option (it uses the controller address or downloads its config).

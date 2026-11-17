---
id: computing-software.systems-network-administration.dns-dhcp.kea-client-classification
name: kea-client-classification
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, kea, kea-dhcp4, client-classes, client-classification, kea-expressions, vendor-class-identifier, option-60, option-93, pool-client-class, known-unknown, only-if-required, test-expression]
level: advanced
status: verified
description: "Classify DHCP clients in Kea with test expressions (vendor class, arch, MAC prefix, relay info), attach options or pools to classes, use KNOWN/UNKNOWN."
sources:
  - https://kea.readthedocs.io/en/latest/arm/classify.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kea client classification

## Define classes
```json
"client-classes": [
  {"name": "acme-phones",
   "test": "substring(option[60].text,0,10) == 'ACME-PHONE'",
   "option-data": [{"name": "tftp-server-name", "data": "10.0.0.69"}]},
  {"name": "uefi-x64", "test": "option[93].hex == 0x0007"},
  {"name": "printers", "test": "substring(pkt4.mac,0,3) == 0x001b44"},
  {"name": "site-b-relay", "test": "relay4[1].hex == 'sw-b-01'"}
]
```
Expression language: `option[N].hex|text|exists`, `substring(x,start,len)`, `pkt4.mac`,
`pkt4.giaddr`, `relay4[sub].hex` (option 82), `member('class')`, `and/or/not`, `concat`,
`ifelse`, `hexstring`, comparisons with `==`.
Built-in classes: `ALL`, `KNOWN` (client has a reservation), `UNKNOWN`, `VENDOR_CLASS_<value>`
(automatic from option 60, e.g. `VENDOR_CLASS_MSFT 5.0`), plus the prefixes `HA_`, `AFTER_` and
`EXTERNAL_` and the names `SKIP_DDNS` and `DROP`. `known` and `unknown` are shorthand for
`member('KNOWN')` and `not member('KNOWN')`. Any expression that uses `KNOWN` is evaluated after
the host reservation lookup; with `early-global-reservations-lookup` a global match sets `KNOWN`
early but a miss does not set `UNKNOWN` at that stage (ARM, classification section).

## Use classes
- Options per class (above) are merged into responses. Option precedence in the ARM is: host,
  pool, subnet, shared network, options from classes (in the order the classes were assigned;
  the first class that sets an option wins, `ALL` first), options from
  `evaluate-additional-classes` classes, then global options. So class options override global
  options but not subnet-level ones.
- Restrict pools (Kea 3.0+; before 2.7.5 the single-valued `"client-class": "acme-phones"` was used,
  now deprecated):
  ```json
  "pools": [{"pool": "10.20.50.10 - 10.20.50.99", "client-classes": ["acme-phones"]},
            {"pool": "10.20.50.100 - 10.20.50.250"}]
  ```
- Restrict pools, subnets and shared networks the same way: `"client-classes": ["KNOWN"]` gives
  addresses only to registered devices; an `UNKNOWN` pool can serve a remediation network.
- `evaluate-additional-classes` (a list on pool, subnet or shared network; replaced
  `require-client-classes` in Kea 2.7.4) evaluates classes only after subnet selection, e.g.
  per-subnet PXE options. The class flag `only-if-required` became `only-in-additional-list`
  in the same release; such a class is usable for option configuration only.

## Debug
Logger `kea-dhcp4.eval` at severity DEBUG with debuglevel at least 55 shows each expression
evaluated per packet and the result. Message `DHCP4_CLASSES_ASSIGNED` (debug level 40) lists all
classes a packet was assigned.
Test option values first with a capture (`dhcp.option.vendor_class_id`, `dhcp.option.client_system_architecture`).

## Verify
- [ ] Packet log shows the expected classes for a test client of each type.
- [ ] Class-restricted pools only hand addresses to members.

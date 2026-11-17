---
id: computing-software.systems-network-administration.dns-dhcp.isc-dhcp-class-to-kea-expression
name: isc-dhcp-class-to-kea-expression
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, kea, class-expression-conversion, client-classes, isc-dhcp-migration]
level: practitioner
status: verified
description: "Convert ISC dhcpd class and match if statements (vendor class, user class, option 82, PXE arch) into Kea client-classes test expressions."
sources:
  - https://kea.readthedocs.io/en/latest/arm/classify.html
  - https://kb.isc.org/docs/migrating-from-isc-dhcp-to-kea-dhcp-using-the-migration-assistant
  - https://github.com/isc-projects/dhcp/tree/master/keama
  - https://ipxe.org/howto/dhcpd
  - https://www.iana.org/assignments/dhcpv6-parameters/dhcpv6-parameters.xhtml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Converting classes to Kea expressions

keama (ISC's experimental migration tool) emits a comment, with a reference to a Kea GitLab issue, for
every feature it cannot translate; check each class it flags. The table shows hand translations.
dhcpd expression semantics are from dhcp-eval(5) and dhcpd.conf(5), Kea's from the ARM
classification chapter.

## Common translations
| dhcpd | Kea `test` |
|-------|------------|
| `match if substring(option vendor-class-identifier, 0, 9) = "PXEClient";` | `substring(option[60].hex,0,9) == 'PXEClient'` |
| `match if option user-class = "iPXE";` | `option[77].hex == 'iPXE'` |
| `match if option client-architecture = 00:07;` (with `option client-architecture code 93 = unsigned integer 16;`, as in iPXE's dhcpd howto) | `option[93].hex == 0x0007` |
| `match if substring(hardware,1,3) = 00:50:56;` (`hardware` is the type byte then the MAC, hence offset 1) | `substring(pkt4.mac,0,3) == 0x005056` |
| `match if option agent.circuit-id = "Gi1/0/1";` | `relay4[1].hex == 'Gi1/0/1'` |
| `match if exists dhcp-client-identifier;` | `option[61].exists` |
| `match pick-first-value (option dhcp-client-identifier, hardware);` subclasses | host reservations or flex-id hook |
| `allow members of "foo";` in a pool | `"client-classes": ["foo"]` on the pool (Kea 3.0+, introduced in 2.7.5; the single-valued `"client-class"` is deprecated) |
| `deny unknown-clients;` | pool `"client-classes": ["KNOWN"]` |

## Example
```json
"client-classes": [
  { "name": "uefi-x64", "test": "option[93].hex == 0x0007",
    "boot-file-name": "shimx64.efi", "next-server": "10.0.0.20" },
  { "name": "ipxe", "test": "option[77].hex == 'iPXE'", "boot-file-name": "http://10.0.0.20/boot.ipxe" },
  { "name": "legacy-bios", "test": "option[93].hex == 0x0000", "boot-file-name": "pxelinux.0" }
]
```
Order matters: Kea evaluates classes in configuration order, and an expression may only depend on
classes defined earlier (including built-ins): forward dependencies are rejected when the config is
parsed. Use `member('name')` to reference an earlier class.

Architecture codes (IANA "Processor Architecture Types"): 0 = x86 BIOS, 6 = x86 UEFI, 7 = x64 UEFI,
9 = EBC (EFI byte code, not x64), 11 = ARM 64-bit UEFI. Capture a real client to confirm what its
firmware sends.

## Gotchas
- `.hex` compares raw bytes; strings in quotes compare as bytes too. Integers need correct width
  (`0x0007`, two bytes for option 93).
- Options from the client are only available if sent; test with `option[N].exists` when needed.
- Classes are evaluated before subnet selection; to evaluate a class only after the subnet is chosen
  (for example per-subnet boot options) flag it `only-in-additional-list` and name it in an
  `evaluate-additional-classes` list on the pool, subnet or shared network. These replaced
  `only-if-required` and `require-client-classes` in Kea 2.7.4 (so Kea 3.0 stable); the old names are
  deprecated.

## Verify
- [ ] Each client type (UEFI, BIOS, iPXE, phones) gets the expected class in Kea debug logs (`kea-dhcp4.eval` at debug level 55; `DHCP4_CLASSES_ASSIGNED`) and the right boot options.

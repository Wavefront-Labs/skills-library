---
id: computing-software.systems-network-administration.network-design.iana-registry-and-etc-services
name: iana-registry-and-etc-services
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, iana-registry, etc-services, port-numbers, service-names, getent]
level: practitioner
status: docs-checked
description: "Look up and interpret port and protocol assignments correctly: IANA registry ranges, the local services file on Linux/Windows, and why registered does not mean in use."
sources:
  - https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml
  - https://www.rfc-editor.org/rfc/rfc6335
  - https://man7.org/linux/man-pages/man5/services.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IANA port registry and the services file

## Ranges (RFC 6335)
| Range | Name | Assignment |
|---|---|---|
| 0-1023 | system / well-known | assigned by IANA |
| 1024-49151 | user / registered | assigned by IANA |
| 49152-65535 | dynamic / private | never assigned; ephemeral source ports |

Registration documents intent, not reality: malware, games and vendors use unregistered or
squatted ports, and a registered port can carry anything. Identify traffic by inspection, not by
port number alone.

## Looking ports up
- IANA CSV: `https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.csv`
  (search by name or number; includes transport and reference RFC).
- Linux: `/etc/services`, one service per line as `service-name port/protocol [aliases ...]` (services(5)).
- Tools that resolve service names from the same table can show a name where you expect a number.

## Practical rules
- Firewall rule documentation should state the service, not only the number (`tcp/8443 = vendor X
  admin UI`).
- When choosing a port for an internal service, pick an unassigned registered port and record it
  in the CMDB; avoid the dynamic range, which collides with ephemeral sockets.
- Use numeric output in network tools during incidents so names do not hide port numbers.

## Verify
- [ ] Each custom service port is recorded with owner and checked against the IANA list for collisions.

## Checked

- Date: 2026-10-28
- Confirmed: RFC 6335 ranges (system 0-1023 and user 1024-49151 assigned by IANA; dynamic 49152-65535 never assigned); services(5) line format.
- Removed: the IETF-review/IESG/expert-review column, root or capability requirement, getent usage, the Windows services path, the ss-name remark.

Method: documentation only; no commands were run.

---
id: computing-software.networking-hardware-and-wireless.asterisk.migrating-chan-sip-to-pjsip
name: migrating-chan-sip-to-pjsip
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, pjsip, chan-sip, migration, sip-to-pjsip, modules-conf, nat]
level: practitioner
status: docs-checked
description: "Migrate from chan_sip to res_pjsip: the sip_to_pjsip.py conversion script, user and trunk mapping, modules.conf choices, running both drivers, and NAT option equivalents."
sources:
  - https://docs.asterisk.org/Configuration/Channel-Drivers/SIP/Configuring-res_pjsip/Migrating-from-chan_sip-to-res_pjsip/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# migrating from chan_sip to res_pjsip
Conversion helper: `contrib/scripts/sip_to_pjsip/sip_to_pjsip.py` in the source tree; run it from the configuration directory (see `--help`).

The page maps two scenarios from sip.conf to pjsip.conf: phones as users (6001 registering, 6002 with a static host/contact, both with username and password auth), and an ITSP trunk (registration with account name and password, outbound calls to the same address with the same credentials, inbound calls with a user name arriving only from the provider IP).

Choosing a driver: edit `modules.conf` and restart Asterisk. To remove PJSIP entirely, remove PJSIP modules from the modules directory, delete `pjsip.conf`, or rebuild without PJSIP modules. To run chan_pjsip alongside chan_sip, change the port or bind interface of the pjsip transport.

NAT equivalents:
- `rtp_symmetric`: send media to the address and port it is received from, ignoring the SDP.
- `force_rport`: send responses to the source address and port even without `rport`.
- `rewrite_contact`: rewrite the Contact to the request source so later requests go there.

## Checked
2026-11-09: read the cited Migrating from chan_sip to res_pjsip page in full and confirmed the script path and behaviour, the two side-by-side scenarios, the modules.conf and removal options, and the three NAT options. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.

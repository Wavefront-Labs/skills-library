---
id: computing-software.networking-hardware-and-wireless.asterisk.pjsip-troubleshooting
name: pjsip-troubleshooting
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, pjsip, troubleshooting, logger, identify, authentication, cli]
level: practitioner
status: docs-checked
description: "Troubleshoot PJSIP endpoint identification, authentication, missing auth lines and dialplan routing using pjsip show commands, pjsip set logger and module checks."
sources:
  - https://docs.asterisk.org/Configuration/Channel-Drivers/SIP/Configuring-res_pjsip/Asterisk-PJSIP-Troubleshooting-Guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pjsip troubleshooting
Turn on tracing: `core set verbose 4`, `core set debug 4`, `pjsip set logger on`.

Identify by user: run `pjsip show endpoints`. If the endpoint is missing, check startup logs and that the section has `type = endpoint` (otherwise the whole section is ignored).

Identify by IP: confirm `module show like res_pjsip_endpoint_identifier_ip.so`; run `pjsip show endpoint <name>`; check the identify section has `type = identify`, a correctly spelled `endpoint`, and correct `match` lines. With non-file config, identify sections must be listed under the `res_pjsip_endpoint_identifier_ip` module in `sorcery.conf`.

Anonymous identification: check `res_pjsip_endpoint_identifier_anonymous.so` is loaded and the "anonymous" endpoint exists.

Authentication: username and password case must match; set `username` explicitly (it is not taken from the section name); check `realm`; the endpoint needs an `auth` line pointing to an existing `type = auth` section; the device must use Digest authentication.

Routing: check the endpoint `context` spelling and use `dialplan show <context>` to confirm the extension exists.

## Checked

2026-11-09. Confirmed against the Asterisk PJSIP Troubleshooting Guide: logging commands, identify-by-user and identify-by-IP steps including the sorcery.conf note, anonymous identifier module, authentication checks and the dialplan show check. Pages is dated but the cited steps are unchanged. Nothing changed in the skill.
Method: documentation only; no commands were run.

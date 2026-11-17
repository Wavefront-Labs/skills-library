---
id: computing-software.networking-hardware-and-wireless.asterisk.pjsip-configuration-wizard
name: pjsip-configuration-wizard
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, pjsip, pjsip-wizard, wizard, trunk, itsp, registration]
level: practitioner
status: docs-checked
description: "Use the PJSIP configuration wizard (pjsip_wizard.conf) to generate endpoint, aor, auth, registration and identify objects for trunk and user scenarios from one section."
sources:
  - https://docs.asterisk.org/Configuration/Channel-Drivers/SIP/Configuring-res_pjsip/PJSIP-Configuration-Wizard/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pjsip configuration wizard
The wizard (module `res_pjsip_config_wizard`) is defined in `pjsip_wizard.conf` with `type = wizard`. It creates standard objects behind the scenes; transport, system and global sections still belong in `pjsip.conf`, and names must not collide with objects defined there.

Key parameters:
- `sends_auth=yes` creates an outbound auth object named `<wizard_name>-oauth`, configured with the `outbound_auth/` prefix.
- `accepts_auth=yes` creates `<wizard_name>-iauth`, configured with `inbound_auth/`.
- `sends_registrations=yes` creates a registration per remote host named `<wizard_name>-reg-<n>`; do not use a wizard when each registration needs different parameters.
- `remote_hosts` is a comma-separated list; each gets an AoR contact built from `contact_pattern`. `server_uri_pattern` and `client_uri_pattern` use `${REMOTE_HOST}` and `${USERNAME}`.
- `accepts_registrations` requires `remote_hosts` to be unset. Otherwise an identify object `<wizard_name>-identify` is created.
- `has_phoneprov` needs `phoneprov/MAC` and `phoneprov/PROFILE`; `has_hint` uses `hint_context`, `hint_exten`, `hint_application`.
- `<object>/<parameter>` (for example `endpoint/context`, `aor/qualify_frequency`) passes values through to the native object.

An endpoint and AoR are always created, named after the wizard.

## Checked

2026-11-09. Confirmed against the Asterisk PJSIP Configuration Wizard page: pjsip_wizard.conf, generated object names (-oauth, -iauth, -reg-n, -identify), sends/accepts parameters, URI patterns, phoneprov and hint requirements, prefix passthrough, name-collision and pjsip.conf notes. Nothing changed.
Method: documentation only; no commands were run.

---
id: computing-software.networking-hardware-and-wireless.asterisk.pjsip-sections-and-relationships
name: pjsip-sections-and-relationships
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, pjsip, pjsip-conf, endpoint, aor, transport, identify, acl]
level: practitioner
status: docs-checked
description: "Relate PJSIP pjsip.conf section types: endpoint, transport, auth, aor, registration, domain_alias, acl and identify, and how endpoint and AoR names match inbound requests."
sources:
  - https://docs.asterisk.org/Configuration/Channel-Drivers/SIP/Configuring-res_pjsip/PJSIP-Configuration-Sections-and-Relationships/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pjsip sections and relationships
pjsip.conf is a flat file of sections. Each section has a `type` option naming the configuration object. Help for any option: `config show help <res_pjsip module name> <configobject> <configoption>`.

- **endpoint**: profile for a phone or remote server; ties to auth, aor and transport. It cannot be contacted without one or more AoRs (`aors=`).
- **transport**: UDP, TCP, WebSocket or TLS binding. Transports cannot share an IP+port or IP+protocol, and PJSIP does not allow multiple TCP or TLS transports of the same IP version. Transport sections cannot be reloaded at run time unless `allow_reload=yes`.
- **auth**: credentials for inbound or outbound authentication; several endpoints or registrations may share one.
- **aor**: where an endpoint can be contacted, either a static `contact=` SIP URI or dynamic REGISTER contacts. `max_contacts` limits registrations. The name must match the user part of the To header in a REGISTER.
- **registration**: outbound registration (`server_uri`, `client_uri`, `outbound_auth`, `retry_interval`).
- **domain_alias**: maps one domain to another.
- **acl**: applies to all inbound res_pjsip traffic, via `acl=` (acl.conf), `deny`/`permit`, or `contactdeny`/`contactpermit`.
- **identify**: `endpoint=` plus `match=` IP so inbound traffic is matched to an endpoint by IP.

Endpoint and AoR section names must match the user part of the inbound From header, unless an identify section matches the request by IP. If `transport=` is unset, the first valid configured transport is used.

## Checked

2026-11-09. Confirmed against the Asterisk PJSIP Configuration Sections and Relationships page: section types, transport caveats and allow_reload, AoR and endpoint naming, acl and identify options. Nothing changed.
Method: documentation only; no commands were run.

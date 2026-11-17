---
id: computing-software.networking-hardware-and-wireless.asterisk.pjsip-outbound-registrations
name: pjsip-outbound-registrations
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, pjsip, registration, server-uri, client-uri, contact-user, itsp, trunk, identify]
level: practitioner
status: docs-checked
description: "Register Asterisk to a provider with a PJSIP registration section: server_uri, client_uri, contact_user, outbound_auth, plus the endpoint, identify and aor."
sources:
  - https://docs.asterisk.org/Configuration/Channel-Drivers/SIP/Configuring-res_pjsip/Configuring-Outbound-Registrations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pjsip outbound registrations
A `type = registration` section is separate from any endpoint.

- `server_uri`: where the registrar is.
- `client_uri`: address of record used in the To and From headers of the REGISTER.
- `contact_user`: user part of the Contact URI; calls from the provider arrive in this extension in the dialplan.
- `outbound_auth`: points to a `type = auth` section (with `username`, `password`) used when the registrar challenges. Omit it if no authentication is needed.
- `transport`, and `retry_interval`.
- Transport type can be put in the URIs, e.g. `server_uri = sip:registrar@example.com\;transport=tcp`.

To accept calls from the provider, add an endpoint plus an `identify` section (`match = <provider IP>`, `endpoint = <endpoint name>`). To dial out to it, also add an `aor` with a `contact` and list it in the endpoint's `aors`.

The page calls these the bare minimum: a working setup also needs a context, codecs and authentication on the endpoint. Full option list is in the res_pjsip_outbound_registration module configuration reference.

## Checked

2026-11-09. Confirmed against the Asterisk Configuring Outbound Registrations page: server_uri, client_uri, contact_user, outbound_auth, transport tip, endpoint, identify and aor requirements, and the bare-minimum warning. Nothing changed.
Method: documentation only; no commands were run.

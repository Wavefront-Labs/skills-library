---
id: computing-software.cybersecurity-defensive.authentik.provider-radius
name: provider-radius
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, radius-provider, eap-tls, pap, vendor-attributes, outpost]
level: advanced
status: docs-checked
description: "Configure the authentik RADIUS provider: supported stages, PAP and EAP-TLS (Enterprise), MFA code in the password, and custom vendor attributes via property mappings."
sources:
  - https://docs.goauthentik.io/add-secure-apps/providers/radius/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: authenticate network gear and apps that only speak RADIUS. Needs a RADIUS outpost. Only authentication requests are supported.

## Flow
Requests execute a flow in the background. Supported stages: Identification, Password, Authenticator validation (Duo, TOTP, static only), User Logout, User Login, Deny, Mutual TLS. For code-based MFA append the code after a semicolon: `example-password;123456`. SMS authenticators cannot be used because no code can be sent during the request.

## Protocols
Password auth supports only PAP, because other methods need reversible password hashes which authentik does not keep. EAP-TLS is an Enterprise feature.

EAP-TLS setup: build an authentication flow whose first stage is a Mutual TLS stage configured with your CA, select a server certificate on the RADIUS provider, and set the provider to use that flow. Use CA-issued client and server certificates, not self-generated ones. Do not use a globally known CA: anyone holding a certificate it signed could authenticate; use private PKI trusted by the devices and implement custom validation to prevent unauthorized access.

## Custom attributes
Since 2024.8, RADIUS property mappings add attributes to responses; select the mapping in the provider afterwards. Cisco AV-Pair example:
```python
define_attribute(
    vendor_code=9,
    vendor_name="Cisco",
    attribute_name="AV-Pair",
    attribute_code=1,
    attribute_type="string",
)
packet["Cisco-AV-Pair"] = "shell:priv-lvl=15"
return packet
```

## Checked
2026-11-03. Every remaining option, endpoint, value and example was read against the authentik documentation page https://docs.goauthentik.io/add-secure-apps/providers/radius/.
Removed as not confirmed by that page: Cisco AV-Pair example corrected to the documented define_attribute/packet form; auth_method pointer.
Method: documentation only; no commands were run.

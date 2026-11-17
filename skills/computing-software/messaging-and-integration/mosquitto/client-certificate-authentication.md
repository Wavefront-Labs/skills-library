---
id: computing-software.messaging-and-integration.mosquitto.client-certificate-authentication
name: client-certificate-authentication
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [require-certificate, use-identity-as-username, use-subject-as-username, mutual-tls]
level: advanced
status: docs-checked
description: "Require client certificates and map the certificate CN or full subject to the MQTT username for access control."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: authenticate clients by X.509 certificate.

Listener options:
- `require_certificate true|false`: if true, a client connecting to this listener must provide a valid certificate for the network connection to proceed. If false, the client verifies the server but authentication is limited to MQTT username/password.
- `use_identity_as_username true`: the Common Name (CN) from the client certificate is used as the username for access control. The `password_file` is not used for this listener. The password is not used because only authenticated clients have valid certificates.
- `use_subject_as_username true`: the complete subject is used instead, in a form like `CN=test client,OU=Production,O=Server,L=Nottingham,ST=Nottinghamshire,C=GB`. `use_identity_as_username` takes priority if both are true.

Both username options require `require_certificate true`.

Trust warning from the page: any CA certificate you include in `cafile` or `capath` can issue client certificates that are valid for connecting to your broker.

If `use_identity_as_username` is false, the client must authenticate as normal through MQTT username and password (if required by `password_file`).

Related: `disable_client_cert_date_checks true` allows expired or not-yet-valid client certificates when `require_certificate` is true; it defaults to false.

## Checked

Method: 2026-11-08 docs-only. Read the cited man page in full and compared each claim. Claims checked against mosquitto.conf(5). Claims unchanged; all match the page.

---
id: computing-software.systems-network-administration.pki-tls-administration.step-ca-acme-renewal
name: step-ca-acme-renewal
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [step-ca-acme-renewal, pki-step-ca, step-ca, acme, step-renew, smallstep, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Issue internal certificates over ACME from step-ca and keep them renewed with step ca renew and a systemd timer."
sources:
  - https://smallstep.com/docs/step-ca/provisioners/#acme
  - https://smallstep.com/docs/step-cli/reference/ca/renew/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# step-ca ACME and renewal daemon
Goal: internal TLS certificates that renew themselves.
ACME clients (certbot, acme.sh) point `--server` at the ACME provisioner's directory URL, with the internal root trusted by the client. An ACME provisioner is added with `step ca provisioner add acme --type ACME`.
Native renewal:
```
step ca renew --daemon --renew-period 16h app.crt app.key
step ca renew --force app.crt app.key --exec "systemctl reload nginx"
```
- step-ca issues certificates valid for 24 hours by default; change `defaultTLSCertDuration` per provisioner or pass `--not-after` to `step ca certificate`. Short lifetimes give regular key rotation and passive revocation.
- `--daemon` renews before 2/3 of the lifetime has elapsed unless `--renew-period` or `--expires-in` is set; `--exec` runs a command after renewal.
- systemd: the `cert-renewer@.service` template with `cert-renewer@.timer` runs renewals; its `ExecStartPost` reloads or restarts the unit named by the instance, and an override file can add more `ExecStartPost` lines (an empty `ExecStartPost=` disables the template's).
- Renewal authenticates with mTLS using the existing certificate.
Gotcha: an expired certificate cannot renew with mTLS unless the provisioner was configured with `--allow-renewal-after-expiry`, which the docs warn adds security risk; renew well before expiry.
Verify:
- [ ] `openssl x509 -in app.crt -noout -dates` moves forward after the timer.
- [ ] The service reload hook fires (check journal).

## Checked
2026-11-03. Confirmed on the step-ca Renewal page and the `step ca renew` reference: 24 hour default, `defaultTLSCertDuration`, `--not-after`, passive revocation, `--daemon` (2/3 default), `--renew-period`, `--expires-in`, `--exec`, `--force`, mTLS authentication, `--allow-renewal-after-expiry`, `cert-renewer@.service` and `.timer`, `ExecStartPost` template and override behaviour; `step ca provisioner add acme --type ACME` on the Provisioners page. Removed: the certbot directory URL form, `REQUESTS_CA_BUNDLE`, the combined `--expires-in 8h --renew-period 16h` example, the claim that an expired certificate always needs re-bootstrapping, and the `step certificate inspect | jq` check.
Method: documentation only; no commands were run.

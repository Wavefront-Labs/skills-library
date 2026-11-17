---
id: computing-software.cloud-infrastructure-engineering.cert-manager.certificate-resource
name: certificate-resource
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [certificate, duration, renewbefore, rotationpolicy, privatekey, secrettemplate, renewal-windows]
level: practitioner
status: docs-checked
description: "Write cert-manager Certificate resources: required fields, duration and renewal rules, private key rotationPolicy, usages, output formats and Secret contents."
sources:
  - https://cert-manager.io/docs/usage/certificate/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Required: `secretName`, `issuerRef`, and at least one of `commonName`, `dnsNames`, `uris`, `emailAddresses`, `ipAddresses`, `otherNames` (needs 1.14+ and the OtherNames gate). `issuerRef.kind` defaults to `Issuer`; `group` defaults to `cert-manager.io`. Avoid `commonName` for leaves.

Durations: default 90 days, minimum 1 hour. `renewBefore` effective minimum 5 minutes; `duration` must exceed it. Use `s`, `m`, `h`; the `d` suffix is not allowed. Default renewal at two thirds of lifetime; `renewBeforePercentage` is preferred to avoid loops when issuers backdate `notBefore` (Let's Encrypt's one-hour backdating leaves 89d 23h). `status.RenewalTime` shows the schedule. `renewal.policy` is `RenewBefore` or `Disabled`; `renewal.windows` take a 5-field `cron`, `windowDuration` and optional `timezone` (default UTC) and only express a preference: if no window fits, renewal still happens at the calculated time.

Reissue triggers: changes to names, `subject`, `isCA`, `usages`, `duration` or `issuerRef`; or `cmctl renew <name>`. Do not delete the Secret to rotate keys.

`privateKey.rotationPolicy`: `Always` since v1.18.0 (`Never` before). Some issuers (CyberArk) disallow key reuse, so set it explicitly.

Secret: `tls.crt` is the certificate plus chain, roots omitted; `ca.crt` only when the CA is known (never for ACME) and changes on renewal, so do not mount it into trust stores. `additionalOutputFormats`: `CombinedPEM` (`tls-combined.pem`), `DER` (`key.der`). `secretTemplate` labels are enforced.

Default usages: digital signature, key encipherment, server auth. Deleting a Certificate keeps its Secret unless `--enable-certificate-owner-ref` is set. Annotation `cert-manager.io/issue-temporary-certificate: "true"` holds a placeholder until issuance.

## Checked

2026-11-03. Confirmed on the cert-manager Certificate page (usage/certificate): required fields, otherNames gate, duration and renewBefore rules and minimums, no d suffix, Let's Encrypt backdating example, renewal policy and windows, reissue triggers, rotationPolicy and the v1.18.0 default change, Secret contents, output formats, default usages, owner-ref flag, temporary certificate annotation. Nothing removed. Note the page itself still lists Never as default in its rotationPolicy table while its text says Always from v1.18.0; the skill follows the text.
Method: documentation only; no commands were run.

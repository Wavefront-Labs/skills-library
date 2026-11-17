---
id: computing-software.systems-network-administration.pki-tls-administration.ct-monitoring-alerts
name: ct-monitoring-alerts
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [ct-monitoring-alerts, pki-ct, certificate-transparency, crt-sh, certstream, monitoring, pki-tls-administration]
level: practitioner
status: draft
description: "Monitor CT logs for unexpected certificates on your domains using crt.sh queries, Cert Spotter or CertStream and respond to misissuance."
sources:
  - https://crt.sh/
  - https://sslmate.com/certspotter
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CT monitoring and alerting
Goal: learn about rogue or mistaken certificates within minutes.
```
curl -s 'https://crt.sh/?q=%25.example.com&output=json' | jq -r '.[].name_value' | sort -u
```
- Services: Cert Spotter (SSLMate), Facebook CT Monitor, Censys, Google's CT search; or self-hosted `certstream` filter on your domains.
- Alert rules: certificate for your domain issued by a CA not on your allow-list, unexpected wildcard, or hostnames you do not use.
- Reconcile with inventory: every logged cert should map to a known automation job.
- Respond: contact the CA (their problem-reporting address in the CPS), revoke, and review DNS, CAA and validation records.
- Add CAA to restrict issuers (see CAA topic).
Gotcha: crt.sh queries time out under load; rely on a monitoring service API for alerts, not ad hoc scripts.
Verify:
- [ ] Test issuance in staging domain triggers an alert within the expected window.
- [ ] Alert routing reaches a monitored channel.

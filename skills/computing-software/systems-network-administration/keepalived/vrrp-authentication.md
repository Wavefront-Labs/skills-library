---
id: computing-software.systems-network-administration.keepalived.vrrp-authentication
name: vrrp-authentication
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, vrrp, authentication, auth-type, auth-pass, ipsec-ah]
level: practitioner
status: docs-checked
description: "vrrp_instance authentication block: auth_type PASS or AH and auth_pass, with IPSEC-AH MD5-96 protecting advertisements against spoofing and replay."
sources:
  - https://keepalived.readthedocs.io/en/latest/configuration_synopsis.html
  - https://keepalived.readthedocs.io/en/latest/case_study_failover.html
  - https://keepalived.readthedocs.io/en/latest/software_design.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VRRP authentication

```
authentication {
    auth_type AH
    auth_pass <PASSWORD>
}
```
- `auth_type`: PASS or AH.
- `auth_pass`: the password string.

AH uses IPSEC Authentication Header with MD5-96 to protect advertisements from spoofing and replay. The failover case study uses AH with a different password per instance; the healthcheck/failover mixing study uses PASS.

## Checked

2026-11-04: auth_type PASS|AH and auth_pass confirmed in the configuration synopsis; AH purpose in the failover case study; IPSEC-AH with MD5-96 in the software design page; AH per-instance passwords and PASS in the case studies. Removed unsourced advice (distinct password per router id, keep out of version control, must match on both peers) and the Verify line.
Method: documentation only; no commands were run.

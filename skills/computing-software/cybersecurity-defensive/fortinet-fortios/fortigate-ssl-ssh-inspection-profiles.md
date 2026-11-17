---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-ssl-ssh-inspection-profiles
name: fortigate-ssl-ssh-inspection-profiles
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [ssl-inspection, fortios, deep-inspection, certificate-inspection, ssl-ssh-profile, ssl-exempt, ca-certificate]
level: practitioner
status: draft
description: "Configure FortiGate SSL/SSH inspection from certificate to deep inspection, with exemptions and CA distribution."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: inspect encrypted traffic where policy allows, without breaking pinned apps.

```
config firewall ssl-ssh-profile
    edit "deep-inspect"
        config https
            set ports 443
            set status deep-inspection
        end
        set caname "Corp_SSL_CA"
        config ssl-exempt
            edit 1
                set type fortiguard-category
                set fortiguard-category 31
            next
        end
    next
end
config firewall policy
    edit 10
        set ssl-ssh-profile "deep-inspect"
    next
end
```
The factory profile `certificate-inspection` reads only the server certificate and SNI (enough for web filter categories). `deep-inspection` re-signs traffic with the CA named, so clients must trust that CA (GPO or MDM). Prefer an internal enterprise CA over the default Fortinet_CA_SSL certificate, which is the same on many units.

Gotchas
- Exempt categories such as finance and health by FortiGuard category (IDs vary; confirm with `?`) and add exceptions for pinned apps and update services.
- `set untrusted-caname` handles invalid upstream certs: choose block or allow explicitly.
- Deep inspection drops throughput; check NP offload impact and model sizing.
- Proxy-mode inspection supports more protocols; flow mode supports fewer options.

## Verify
```
diagnose firewall ssl-ssh-profile
diagnose sys session list
```
Browse an https site and verify the certificate issuer is your CA; the traffic log shows ssl decrypted flows (confirm field `ssl-action`).

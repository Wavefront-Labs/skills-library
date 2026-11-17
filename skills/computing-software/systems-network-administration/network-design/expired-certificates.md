---
id: computing-software.systems-network-administration.network-design.expired-certificates
name: expired-certificates
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, troubleshooting-services, expired-certificate, tls, certificate-monitoring, pki]
level: practitioner
status: draft
description: "Detect, fix and prevent outages from expired certificates on network services: checking expiry and chains, common victims (VPN, RADIUS, LDAPS, APIs), and automated monitoring."
sources:
  - https://www.openssl.org/docs/manmaster/man1/openssl-x509.html
  - https://letsencrypt.org/docs/
  - https://www.rfc-editor.org/rfc/rfc8555
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/nps/nps-manage-cert-requirements
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Expired certificates

## Symptoms
- Browsers: `NET::ERR_CERT_DATE_INVALID`; curl: `certificate has expired`.
- VPN clients fail all at once; 802.1X Wi-Fi stops authenticating (expired RADIUS/NPS server
  certificate, or expired client certificates); LDAPS binds fail; API integrations break;
  syslog/TLS and SAML signing failures (expired IdP signing cert).
- Also: an expired **intermediate** or **root** in the chain (e.g. Let's Encrypt DST Root CA X3
  expiry in 2021 broke old clients).

## Check
```
echo | openssl s_client -connect vpn.example.com:443 -servername vpn.example.com 2>/dev/null | openssl x509 -noout -dates -subject -issuer
openssl s_client -connect ldap.example.com:636 -showcerts </dev/null        # whole chain
openssl x509 -in cert.pem -noout -checkend 2592000 && echo "valid >30d"
certutil -store My                                                          # Windows
Get-ChildItem Cert:\LocalMachine\My | ? NotAfter -lt (Get-Date).AddDays(30)
```
Device CLIs: `show crypto pki certificates` (Cisco), check the self-signed HTTPS cert on gear.

## Fix
Renew with the CA, install the **full chain** (leaf + intermediates), restart/rebind the service
(IIS binding, NPS policy selecting the new cert, ASA `crypto ca trustpoint`), verify from a client.
For 802.1X, push the new server cert's issuer to clients beforehand if it changed.

## Prevent
- Inventory every certificate (including internal CA, device, IdP signing); owners recorded.
- Automate renewal: ACME (RFC 8555) with certbot/acme.sh/cert-manager; CA auto-enrolment for internal.
- Monitoring: expiry checks at 30/14/7 days (Prometheus blackbox `probe_ssl_earliest_cert_expiry`,
  Zabbix/Nagios check_ssl_cert), certificate transparency watch for public names.
- Public TLS certificate maximum lifetime is shrinking (CA/B Forum schedule to 47 days by 2029):
  manual renewal will not scale.

## Verify
- [ ] Alerting covers every certificate in inventory; no certificate expires without a ticket at least 30 days before.

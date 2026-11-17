---
id: computing-software.cloud-infrastructure-engineering.external-dns.rfc2136-microsoft-dns-gss-tsig
name: rfc2136-microsoft-dns-gss-tsig
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, gss-tsig, microsoft-dns, kerberos-krb5-conf, active-directory-dns, rfc2136-insecure]
level: sme
status: docs-checked
description: "Use the RFC2136 provider with Microsoft DNS: secure updates via GSS-TSIG and a Kerberos ConfigMap, insecure updates, and the realm and principal error fixes."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/tutorials/rfc2136.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RFC2136 against Microsoft DNS

The docs say external-dns was not developed or tested against Microsoft DNS but can be configured for it ("YMMV").

**DNS side (secure):** create a zone, enable secure dynamic updates, enable zone transfers to all servers and/or other domains, and create a user allowed to create, update and delete records. If ExternalDNS cannot fetch existing records, you probably skipped zone transfers.

**Kerberos:** mount a `krb5.conf` ConfigMap at `/etc/krb5.conf` (volume with `subPath: krb5.conf`). Set `default_realm` and `[realms]` with the KDC and admin server, and `[domain_realm]` mappings; the realm usually matches the domain name.

**Flags:**
```text
--provider=rfc2136
--rfc2136-gss-tsig
--rfc2136-host=dns-host.yourdomain.com
--rfc2136-port=53
--rfc2136-zone=your-zone.com
--rfc2136-kerberos-username=your-domain-account
--rfc2136-kerberos-password=your-domain-password
--rfc2136-kerberos-realm=your-domain.com
--rfc2136-axfr
```
`--rfc2136-axfr` is needed for zone transfers, which deletion requires.

**Errors**
- `KRB Error: (68) KDC_ERR_WRONG_REALM`: set `--rfc2136-kerberos-realm` (otherwise optional).
- `KDC_ERR_S_PRINCIPAL_UNKNOWN Server not found in Kerberos database`: `--rfc2136-host` also names the Kerberos principal, so use the DNS server's actual hostname.

**Insecure updates:** enable insecure dynamic updates and zone transfers, and pass `--rfc2136-insecure --rfc2136-axfr`.

`--rfc2136-use-tls` cannot be combined with `--rfc2136-gss-tsig`; startup is refused.

## Checked

2026-11-04. Read the RFC2136 tutorial (Microsoft DNS, GSS-TSIG, Kerberos configuration, Insecure Updates, DNS over TLS). Confirmed the DNS-side steps, the krb5.conf mount, the flags, the two Kerberos error fixes, the insecure-update flags and the TLS plus GSS-TSIG refusal. Removed nothing.

Method: documentation only; no commands were run.

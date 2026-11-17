---
id: computing-software.cloud-infrastructure-engineering.external-dns.rfc2136-bind-tsig-setup
name: rfc2136-bind-tsig-setup
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, rfc2136, bind9, tsig-key, dynamic-dns-update, tsig-keygen]
level: practitioner
status: docs-checked
description: "Point ExternalDNS at BIND with the RFC2136 provider: generate a TSIG key, allow-transfer and update-policy zone config, flags, local dry-run and verification."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/tutorials/rfc2136.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RFC2136 with BIND and TSIG

**Key:** `tsig-keygen -a hmac-sha256 externaldns` (older: `dnssec-keygen -a HMAC-SHA256 -b 256 -n HOST externaldns`). It prints a `key "externaldns-key" { algorithm hmac-sha256; secret "..."; };` block for `named.conf`.

**Zone config:** allow the key to transfer and update.
```text
zone "k8s.example.org" {
    type master;
    file "/etc/bind/pri/k8s/k8s.zone";
    allow-transfer { key "externaldns-key"; };
    update-policy { grant externaldns-key zonesub ANY; };
};
```
Put the zone file in its own directory because `named` runs unprivileged and must create a journal file. Listen on the interface ExternalDNS reaches. Reload named.

**Dry-run from a workstation:**
```sh
external-dns --txt-owner-id k8s --provider rfc2136 \
  --rfc2136-host=192.168.0.1 --rfc2136-port=53 --rfc2136-zone=k8s.example.org \
  --rfc2136-tsig-secret=<secret> --rfc2136-tsig-secret-alg=hmac-sha256 \
  --rfc2136-tsig-keyname=externaldns-key --rfc2136-axfr \
  --source ingress --once --domain-filter=k8s.example.org --dry-run
```

**Deployment args** (docs): `--registry=txt`, `--txt-prefix=external-dns-`, `--txt-owner-id=k8s`, repeated `--rfc2136-zone`, `--source=ingress`, `--policy=upsert-only`, `--domain-filter`.

**TTL:** the default is 0; use the `ttl` annotation, or `--rfc2136-min-ttl=60s` for a default.

**Secrets:** pass them as `EXTERNAL_DNS_RFC2136_TSIG_SECRET` and `EXTERNAL_DNS_RFC2136_TSIG_KEYNAME` from a Secret.

**Verify:** `dig @<server> app.example.local A +short`, and AXFR with `-y hmac-sha256:<keyname>:<secret>`.

## Checked

2026-11-04. Read the RFC2136 tutorial (Using with BIND, Custom TTL, local test, provider configuration, Helm secret section). Confirmed tsig-keygen and dnssec-keygen commands, the zone block with allow-transfer and update-policy, the journal-file reason, the dry-run flags, deployment args, default TTL 0, --rfc2136-min-ttl and the Secret-sourced environment variables. Removed nothing.

Method: documentation only; no commands were run.

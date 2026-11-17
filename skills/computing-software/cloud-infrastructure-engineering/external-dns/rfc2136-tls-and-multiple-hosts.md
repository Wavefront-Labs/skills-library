---
id: computing-software.cloud-infrastructure-engineering.external-dns.rfc2136-tls-and-multiple-hosts
name: rfc2136-tls-and-multiple-hosts
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, rfc2136-use-tls, dns-over-tls, load-balancing-strategy, multiple-dns-hosts]
level: advanced
status: docs-checked
description: "RFC2136 DNS over TLS flags and multi-host failover or load balancing with --rfc2136-load-balancing-strategy (round-robin, random, disabled)."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/tutorials/rfc2136.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RFC2136: TLS and multiple hosts

**DNS over TLS (RFCs 7858 and 9103)**
- `--rfc2136-use-tls`: TLS for both zone transfers and updates. Doing only one over TLS is not supported.
- `--tls-ca=<cert-file>`: certificates to verify the DNS server.
- `--tls-client-cert=<file>` and `--tls-client-cert-key=<file>`: mutual verification.
- `--rfc2136-skip-tls-verify`: skip server certificate verification.
- Cannot be combined with `--rfc2136-gss-tsig`: the GSS-TSIG key exchange does not support TLS, so ExternalDNS refuses to start.

**Multiple hosts.** Repeat `--rfc2136-host`, and pick a strategy:
- `round-robin`: spread updates evenly across hosts.
- `random`: pick a host at random per update.
- `disabled` (default): use the first host and move on only after a failure.

```shell
external-dns \
  --provider=rfc2136 \
  --rfc2136-host="dns-host-1.yourdomain.com" \
  --rfc2136-host="dns-host-2.yourdomain.com" \
  --rfc2136-load-balancing-strategy="round-robin" \
  --rfc2136-port=53 \
  --rfc2136-zone=example.com \
  --rfc2136-tsig-secret-alg=hmac-sha256 \
  --rfc2136-tsig-keyname=example-key \
  --rfc2136-tsig-secret=example-secret
```

Benefits per the docs: spreads update load across data centres and adds a retry across the host list.

**Helm:** put flags in `extraArgs` and source the key name and secret from a Secret through `EXTERNAL_DNS_RFC2136_TSIG_KEYNAME` and `EXTERNAL_DNS_RFC2136_TSIG_SECRET`:
```shell
kubectl create secret generic rfc2136-keys --from-literal=rfc2136-tsig-secret='xxx' --from-literal=rfc2136-tsig-keyname='k8s-external-dns-key' -n external-dns
```

## Checked

2026-11-04. Read the RFC2136 tutorial (DNS Over TLS, Multiple Hosts and Load Balancing, Helm, Secret creation, Benefits). Confirmed every TLS flag, the three strategies with disabled as default, the example command, the Helm environment variables and the Secret command. Removed nothing.

Method: documentation only; no commands were run.

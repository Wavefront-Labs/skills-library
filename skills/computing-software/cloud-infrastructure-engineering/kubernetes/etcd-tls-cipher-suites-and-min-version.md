---
id: computing-software.cloud-infrastructure-engineering.kubernetes.etcd-tls-cipher-suites-and-min-version
name: etcd-tls-cipher-suites-and-min-version
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, etcd-security, etcd-cipher-suites, tls, etcd, hardening]
level: practitioner
status: docs-checked
description: "Restrict etcd client and peer TLS to strong cipher suites and TLS 1.2 or 1.3 with --cipher-suites and --tls-min-version, and verify the result."
sources: ["https://etcd.io/docs/v3.6/op-guide/security/", "https://etcd.io/docs/v3.6/op-guide/configuration/", "https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/setup-ha-etcd-with-kubeadm/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# etcd TLS cipher suites and minimum version

## Flags
```
--cipher-suites=TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
--tls-min-version=TLS1.2
```
`--tls-min-version` sets the minimum TLS version etcd accepts (default `TLS1.2`); `--tls-max-version` sets the
maximum and defaults to the highest version Go supports. An empty `--cipher-suites` lets Go choose. The suites
apply to both client (2379) and peer (2380) traffic. Suite names are Go TLS names; choose suites that match your
certificate key type.

## kubeadm
```yaml
etcd:
  local:
    extraArgs:
    - {name: cipher-suites, value: "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384"}
    - {name: tls-min-version, value: "TLS1.2"}
```
Apply to one member at a time; each restart briefly removes a member, so keep quorum.

## Compatibility
- Clients must offer one of the configured suites or the handshake fails, so check any tool that talks to etcd
  directly (backup jobs, monitoring).

## Verify
```bash
# a suite that is not in the list must fail the handshake (etcd docs use curl with --ciphers)
curl --cacert ca.crt --cert client.crt --key client.key https://<etcd-ip>:2379/metrics --ciphers ECDHE-RSA-AES128-GCM-SHA256
curl --cacert ca.crt --cert client.crt --key client.key https://<etcd-ip>:2379/metrics --ciphers ECDHE-RSA-DES-CBC3-SHA   # fails: handshake failure
etcdctl endpoint health --cluster
```

## Checked

Date: 2026-10-26. Documentation release: etcd v3.6 docs (etcd-io/website, repository head 2026-10-23); Kubernetes website docs (kubernetes/website main, 2026-10-26); kubeadm source (kubernetes/kubernetes master).

Confirmed: `--cipher-suites` (comma-separated list, empty auto-populates from Go) applies to client and peer traffic; the etcd security page example `TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384`; `--tls-min-version` defaults to `TLS1.2` and `--tls-max-version` defaults to the Go maximum; a handshake with a non-listed suite fails (checked with curl `--ciphers` in the etcd example); kubeadm `etcd.local.extraArgs` as a list of name and value pairs (v1beta4). Removed as unconfirmed: the ECDSA suite names, the accepted version strings for `--tls-min-version`, the TLS 1.3 cipher-suite rule, the apiserver client compatibility claim, kubeadm's default key type, and the nmap and openssl `-tls1_1` checks.

Method: documentation only; no commands were run.

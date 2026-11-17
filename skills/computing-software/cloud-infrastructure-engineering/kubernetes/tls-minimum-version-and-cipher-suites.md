---
id: computing-software.cloud-infrastructure-engineering.kubernetes.tls-minimum-version-and-cipher-suites
name: tls-minimum-version-and-cipher-suites
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, node-kubelet-hardening, tlsminversion, tls-cipher-suites, kube-apiserver, kubelet]
level: practitioner
status: docs-checked
description: "Set TLS minimum versions and cipher suites on kube-apiserver, kubelet and other components, check them with nmap or openssl, and avoid locking out clients."
sources: ["https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/", "https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/", "https://pkg.go.dev/crypto/tls#pkg-constants", "https://etcd.io/docs/v3.5/op-guide/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS minimum version and cipher suites

## kube-apiserver (also controller-manager and scheduler secure ports)
```
--tls-min-version=VersionTLS12
--tls-cipher-suites=TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305
```

## kubelet
```yaml
tlsMinVersion: VersionTLS12
tlsCipherSuites:
- TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256
- TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
- TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384
- TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
```

## Notes
- The kubelet configuration reference states TLS 1.3 cipher suites are not configurable; the list applies to TLS 1.2 and below.
- `VersionTLS13` as minimum is fine for modern clients but breaks old tooling, some load
  balancer health checks and older webhooks or aggregated APIs calling in.
- ECDSA suites only work with ECDSA certs and RSA suites with RSA certs; include both families if
  unsure what your certs use.
- etcd has its own flags (`--cipher-suites`, `--tls-min-version`); etcd v3.5 writes the value as `TLS1.2`, not `VersionTLS12`.
- The apiserver flag accepts `VersionTLS10` to `VersionTLS13`; the kubelet fields `tlsMinVersion` and `tlsCipherSuites` take values from Go's `crypto/tls` constants.

## Check
```bash
nmap --script ssl-enum-ciphers -p 6443,10250 <host>
openssl s_client -connect <host>:6443 -tls1_1 </dev/null    # must fail
openssl s_client -connect <host>:6443 -tls1_2 -cipher ECDHE-RSA-AES128-GCM-SHA256 </dev/null | grep Cipher
```

## Roll out
One control-plane node at a time; test kubectl, kubelets, webhooks, monitoring and LB probes
after each.

## Checked

Checked 2026-10-27 against Kubernetes documentation (kubernetes/website main tree, v1.38 development; latest release v1.37.1) and kubeadm/kubectl source: kube-apiserver and kube-controller-manager references (--tls-min-version values VersionTLS10 to VersionTLS13, --tls-cipher-suites accepted names including the CHACHA20 forms), kubelet configuration types (tlsMinVersion, tlsCipherSuites, TLS 1.3 suites not configurable), kube-scheduler reference (same flags listed) and etcd v3.5 configuration (--cipher-suites, --tls-min-version 'TLS1.2').

Method: documentation only; no commands were run.

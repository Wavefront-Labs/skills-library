---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cis-kubelet-remediation
name: cis-kubelet-remediation
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cis-benchmark, cis-kubelet, kubelet-configuration, kube-bench, node-hardening]
level: practitioner
status: docs-checked
description: "Fix CIS kubelet findings (anonymous auth, webhook authorization, read-only port, iptables chains, certificate rotation, ciphers) through KubeletConfiguration."
sources: ["https://www.cisecurity.org/benchmark/kubernetes", "https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/", "https://github.com/aquasecurity/kube-bench/blob/main/cfg/cis-1.9/node.yaml", "https://kubernetes.io/docs/reference/setup-tools/kubeadm/implementation-details/", "https://kubernetes.io/docs/reference/access-authn-authz/kubelet-authn-authz/", "https://raw.githubusercontent.com/kubernetes/kubernetes/master/staging/src/k8s.io/component-helpers/node/util/sysctl/sysctl.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CIS kubelet remediation

Section 4.2 of the benchmark (ids are kube-bench `cis-1.9` node checks; other versions renumber). Fix in
`/var/lib/kubelet/config.yaml` (or the `kubelet-config` ConfigMap in `kube-system` on kubeadm so new
nodes inherit it), not in systemd flags: command-line flags override the config file.

```yaml
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
authentication:
  anonymous: {enabled: false}                 # 4.2.1
  webhook: {enabled: true}
  x509: {clientCAFile: /etc/kubernetes/pki/ca.crt}   # 4.2.3
authorization:
  mode: Webhook                               # 4.2.2 (must not be AlwaysAllow)
readOnlyPort: 0                               # 4.2.4
streamingConnectionIdleTimeout: 4h0m0s        # 4.2.5, must not be 0 (field is deprecated and has no effect on current kubelets)
makeIPTablesUtilChains: true                  # 4.2.6
rotateCertificates: true                      # 4.2.10, client cert rotation (must not be false)
serverTLSBootstrap: true                      # 4.2.11 (Manual), CA-signed serving cert via the CSR API
tlsCipherSuites: [TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256, TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256, TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384]   # 4.2.12 (Manual), subset of the CIS list
protectKernelDefaults: true                   # hardening; no numbered check in cis-1.9 (set sysctls first)
```
Apply with `systemctl restart kubelet`, one node at a time.

## Care points
- `readOnlyPort: 0` disables the unauthenticated read-only port; anything that scraped it must move to
  the authenticated port (default 10250).
- `protectKernelDefaults: true` makes the kubelet error if kernel flags differ from what it expects
  (default false: it modifies them). The tunables it checks are `vm.overcommit_memory=1`,
  `vm.panic_on_oom=0`, `kernel.panic=10`, `kernel.panic_on_oops=1`, `kernel.keys.root_maxkeys=1000000`
  and `kernel.keys.root_maxbytes=25000000`; set them in `/etc/sysctl.d/` first.
- `serverTLSBootstrap` creates serving-certificate CSRs that need an approver (the field documentation
  says so): approve manually or run an approver controller.

## Verify
```bash
kube-bench run --targets node 2>/dev/null | grep -E '^\[(PASS|FAIL|WARN)\] 4\.2'
curl -sk https://<node>:10250/pods       # expect 401 Unauthorized once anonymous auth is off
```

## Checked
2026-10-28. Confirmed: check ids and wording 4.2.1-4.2.6, 4.2.10-4.2.12 and the "not 0" and "not set to
false" rules against kube-bench `cfg/cis-1.9/node.yaml`; every field name, the `protectKernelDefaults`
behaviour and default, the `serverTLSBootstrap` approver requirement, the `streamingConnectionIdleTimeout`
deprecation, port 10250 and the 4h default against the KubeletConfiguration and kubelet references; the
six kernel tunables and values against the Kubernetes source (`container_manager_linux.go` and
component-helpers `sysctl.go`); the `kubelet-config` ConfigMap and config path against the kubeadm
implementation details; "flags override the file" against the kubelet reference. Removed: the old ids
that put `protectKernelDefaults` at 4.2.6 and `makeIPTablesUtilChains` at 4.2.7 (4.2.7 is the
hostname-override check in 1.9), and the unsourced port number 10255. The "401 Unauthorized" expectation against
the Kubelet authn/authz page.
Method: documentation only; no commands were run.

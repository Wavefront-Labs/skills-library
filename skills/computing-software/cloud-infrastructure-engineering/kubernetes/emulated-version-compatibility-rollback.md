---
id: computing-software.cloud-infrastructure-engineering.kubernetes.emulated-version-compatibility-rollback
name: emulated-version-compatibility-rollback
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, emulation-version, compatibility-version, version-skew, cluster-upgrade, rollback]
level: practitioner
status: docs-checked
description: "Use kube-apiserver --emulated-version (compatibility versions, KEP-4330) to upgrade binaries while keeping the previous minor's APIs and features for a safe rollback."
sources: ["https://kubernetes.io/docs/concepts/cluster-administration/compatibility-version/", "https://github.com/kubernetes/enhancements/tree/master/keps/sig-architecture/4330-compatibility-versions", "https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Emulated and compatibility versions

The Kubernetes documentation says configurable version compatibility and emulation for control
plane components were introduced in v1.32 (KEP-4330, whose alpha milestone was v1.31). A
control-plane binary at 1.N can run with `--emulated-version=1.(N-1)`:
- Capabilities (APIs, features) introduced after the emulated version are unavailable.
- Capabilities removed after the emulated version are available again.
- `--emulated-version` takes `major.minor`, must be less than or equal to the binary version, and
  only a range of recent versions is accepted (the v1.37 reference lists `kube=1.34..1.37`;
  check `--help` of your binary).

## Minimum compatibility version
`--min-compatibility-version` (default `1.36` in the v1.37 reference) sets the oldest version the
component stays compatible with; it must be less than or equal to the emulated version. Per the
KEP, the component then tolerates workloads that expect that version's behaviour, component skew
ranges extend, and rollbacks can be performed back to that version. Keeping it fixed during a
binary or emulated-version upgrade means features are not removed from the API underneath you.

## Two-step upgrade
```yaml
# kubeadm ClusterConfiguration (v1beta4), step 1: new binaries, old behaviour
apiServer:
  extraArgs:
  - name: emulated-version
    value: "1.<N-1>"
```
1. Upgrade control-plane binaries to 1.N with `emulated-version=1.(N-1)`; soak.
2. Per the KEP, an emulation-version rollback can be performed without changing the binary
   version, and a binary rollback is supported back to the minimum compatibility version.
3. When satisfied, raise or remove the flag and restart; now 1.N behaviour is active.

kube-apiserver, kube-controller-manager and kube-scheduler references list the flag.

## Limits
- With a lower emulated version, `--runtime-config` entries for APIs introduced after it make
  the server fail to start unless `--runtime-config-emulation-forward-compatible=true`
  (kube-apiserver reference).
- The flags are defined for control-plane components; nodes still follow the normal version
  skew policy.

## Verify
```bash
kubectl get --raw /version
kubectl get --raw /metrics | grep kubernetes_build_info
```
The `kubernetes_feature_enabled` metric (labels `name`, `stage`) shows which gates are on.

## Checked

Checked 2026-10-27 against Kubernetes documentation (kubernetes/website main tree, v1.38 development; latest release v1.37.1) and kubeadm source: compatibility-version concept page (introduced in v1.32, emulated version semantics including removed capabilities being available, must be <= binary version), kube-apiserver and kube-controller-manager references (--emulated-version range kube=1.34..1.37, --min-compatibility-version default 1.36, --runtime-config-emulation-forward-compatible), kube-scheduler reference (flags listed) and KEP-4330 text on rollback. Corrected the claim that removed features cannot be emulated back and the introduction release.

Method: documentation only; no commands were run.

---
id: computing-software.cloud-infrastructure-engineering.kubernetes.seccomp-profile-generation-with-spo-and-inspektor-gadget
name: seccomp-profile-generation-with-spo-and-inspektor-gadget
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, seccomp-profile-generation, security-profiles-operator, inspektor-gadget, seccomp, runtime-security, cks]
level: advanced
status: docs-checked
description: "Generate least-privilege seccomp profiles from real workload behaviour with Security Profiles Operator recordings or Inspektor Gadget, then distribute and enforce them safely."
sources: ["https://github.com/kubernetes-sigs/security-profiles-operator/blob/main/doc/profiles.md", "https://github.com/kubernetes-sigs/security-profiles-operator/blob/main/doc/installation.md", "https://inspektor-gadget.io/docs/latest/gadgets/advise_seccomp", "https://kubernetes.io/docs/tutorials/security/seccomp/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generating seccomp profiles

`RuntimeDefault` (the runtime's default profile) is the right baseline. A per-workload
`Localhost` profile allowing only the syscalls the app uses shrinks kernel attack surface
further. Hand-writing one fails; record it.

## Security Profiles Operator (SPO)
Install the operator (kubernetes-sigs; it requires Kubernetes v1.30 or later and the manifest install
uses cert-manager), then enable recording in the namespace (only the label's presence matters):
```bash
kubectl label ns shop spo.x-k8s.io/enable-recording=true
```
```yaml
apiVersion: security-profiles-operator.x-k8s.io/v1
kind: ProfileRecording
metadata: {name: api, namespace: shop}
spec:
  kind: SeccompProfile
  recorder: Logs            # or Bpf; Logs needs the log enricher, Bpf the BPF recorder, enabled in the spod config
  podSelector: {matchLabels: {app: api}}
```
Restart the pods (recording hooks in at creation), run the **full** test suite plus
startup, shutdown, health checks and rare paths (backups, migrations), then delete the
pods. SPO writes one cluster-scoped `SeccompProfile` per container, named
`<recording>-<container>` (`api-app`), so use recording names that are unique across the cluster:
```bash
kubectl get seccompprofiles
kubectl get sp api-app -o jsonpath='{.status.localhostProfile}'   # operator/api-app.json
```
SPO saves profiles on the nodes under `/var/lib/kubelet/seccomp/operator/`. Log-based recording has no
effect on privileged containers.

## Inspektor Gadget (no operator)
```bash
kubectl gadget deploy
kubectl gadget run advise_seccomp:<tag> --podname <pod>
# exercise the app, then stop the gadget: it prints a seccomp profile for each container
```
It records per container (replicas need their profiles merged by hand) and relies on `runc` to
detect container start, so it may not work with `crun`. Save the output as a `SeccompProfile` CR
(SPO) or distribute the JSON to nodes yourself.

## Enforce
```yaml
securityContext:
  seccompProfile:
    type: Localhost
    localhostProfile: operator/api-app.json
```
Roll out with the profile's `defaultAction: SCMP_ACT_LOG` first (violations go to the
audit/kernel log, nothing breaks), watch for a full release cycle, then switch to
`SCMP_ACT_ERRNO`. SPO can also bind profiles via `ProfileBinding` by image.

## Gotchas
- A profile only allows the syscalls seen while recording; regenerate it after base image or
  language runtime upgrades.
- Recording misses code paths you never exercised; error paths are where outages hide.

## Verify
Watch the node syslog for entries from `SCMP_ACT_LOG` during the soak (see the Kubernetes seccomp
tutorial), and confirm the profile with `kubectl get sp -o wide` (STATUS `Installed`).

## Checked

Checked 2026-10-27 against the Security Profiles Operator docs (main, `doc/profiles.md` and `doc/installation.md`), the Inspektor Gadget `advise_seccomp` page and `quick-start`, and the Kubernetes seccomp tutorial (Kubernetes website content (main, v1.38 dev tree) and the v1.37 line (latest release at review time)).

- Corrected: ProfileRecording API is `security-profiles-operator.x-k8s.io/v1` with `recorder: Logs` or `Bpf` (not v1alpha1 / lower case); profiles are cluster-scoped, named `<recording>-<container>`, and referenced as `operator/<name>.json` (not `operator/<namespace>/...`).
- Confirmed: `spo.x-k8s.io/enable-recording` label, log enricher and BPF recorder enabled via spod settings, log recording ineffective for privileged containers, ProfileBinding, Kubernetes v1.30 minimum, cert-manager prerequisite for the manifest install.
- Inspektor Gadget: `kubectl gadget deploy`, `kubectl gadget run advise_seccomp:<tag> --podname`, per-container output, runc and replica limitations confirmed; the old `advise seccomp-profile` sub-command and namespace flag were removed as unconfirmed.
- The old SPO usage link in `sources` was dead and was replaced.

Method: documentation only; no commands were run.

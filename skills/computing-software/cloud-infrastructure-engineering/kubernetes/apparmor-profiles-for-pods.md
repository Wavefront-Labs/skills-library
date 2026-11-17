---
id: computing-software.cloud-infrastructure-engineering.kubernetes.apparmor-profiles-for-pods
name: apparmor-profiles-for-pods
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, apparmor, apparmor-profile, apparmor-parser, runtime-security, securitycontext]
level: practitioner
status: docs-checked
description: "Load AppArmor profiles on nodes and apply them with securityContext.appArmorProfile (RuntimeDefault, Localhost, Unconfined), migrating from the old annotation."
sources: ["https://kubernetes.io/docs/tutorials/security/apparmor/", "https://kubernetes.io/docs/concepts/security/pod-security-standards/", "https://gitlab.com/apparmor/apparmor/-/wikis/Documentation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AppArmor profiles for pods

## Load the profile on every node that may run the pod
```bash
sudo tee /etc/apparmor.d/k8s-deny-write >/dev/null <<'EOF'
#include <tunables/global>
profile k8s-deny-write flags=(attach_disconnected) {
  #include <abstractions/base>
  file,
  deny /** w,
}
EOF
sudo apparmor_parser -q /etc/apparmor.d/k8s-deny-write        # load the profile
sudo grep k8s-deny-write /sys/kernel/security/apparmor/profiles
```
Distribute with a DaemonSet (security-profiles-operator, or a privileged loader) so new nodes get
it; profiles are not loaded by Kubernetes.

## Apply (the `appArmorProfile` field; AppArmor feature stable since 1.31)
```yaml
spec:
  securityContext:
    appArmorProfile:
      type: RuntimeDefault           # pod default
  containers:
  - name: writer
    image: busybox:1.36
    securityContext:
      appArmorProfile:
        type: Localhost
        localhostProfile: k8s-deny-write
```
Types: `RuntimeDefault` (containerd's `cri-containerd.apparmor.d`), `Localhost`, `Unconfined`.
Before v1.30 AppArmor was set with the annotation
`container.apparmor.security.beta.kubernetes.io/<container>: localhost/<name>`; use the field instead.

## Failure mode
Profile not loaded in the node's kernel: the kubelet rejects the pod, or the container fails with an
event such as `apparmor profile not found <name>`. The kubelet also checks that AppArmor is enabled on
the host before admitting a pod that sets a profile. Use node labels plus nodeSelector if only some
nodes have the profile.

## Verify
```bash
kubectl exec writer -- cat /proc/1/attr/current      # k8s-deny-write (enforce)
kubectl exec writer -- touch /tmp/x                  # Permission denied
sudo dmesg | grep -i apparmor | tail                  # AppArmor logs verbose messages to dmesg
```
The Pod Security baseline level restricts `appArmorProfile.type` so the default AppArmor profile
cannot be overridden or disabled (see the Pod Security Standards page for the allowed values).

## Checked
Checked 2026-10-23 against the kubernetes/website docs (current release 1.37).
Confirmed: `appArmorProfile` field with types RuntimeDefault/Localhost/Unconfined and `localhostProfile` required only for
Localhost; AppArmor feature gate stable from 1.31 (beta 1.4 per the gate list), annotations used before v1.30;
`cri-containerd.apparmor.d` default under containerd; `/proc/1/attr/current` check; kubelet rejects pods whose profile is not
loaded; Pod Security baseline AppArmor rule. Wrong in the original: "GA since 1.30" (stable in 1.31). Sample profile,
load command, loaded-profiles file and dmesg check follow the Kubernetes AppArmor tutorial.
Method: documentation only; no commands were run.

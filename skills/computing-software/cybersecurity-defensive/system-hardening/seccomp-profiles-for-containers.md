---
id: computing-software.cybersecurity-defensive.system-hardening.seccomp-profiles-for-containers
name: seccomp-profiles-for-containers
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [container-hardening, seccomp, runtimedefault, seccomp-profile, syscall-filtering, security-profiles-operator, kubernetes]
level: advanced
status: docs-checked
description: "Restrict container syscalls with seccomp: enable RuntimeDefault everywhere, build custom profiles from recorded syscalls, deploy in Docker and Kubernetes, and debug denials."
sources: ["https://github.com/kubernetes/website/blob/main/content/en/docs/tutorials/security/seccomp.md", "https://github.com/docker/docs/blob/main/content/manuals/engine/security/seccomp.md", "https://github.com/kubernetes-sigs/security-profiles-operator/blob/main/doc/profiles.md", "https://github.com/kubernetes/website/blob/main/content/en/docs/concepts/security/pod-security-standards.md", "https://github.com/torvalds/linux/blob/master/Documentation/filesystems/proc.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Seccomp profiles for containers

Seccomp filters which Linux system calls a process may make. Docker's default profile leaves out syscalls
ordinary applications rarely need; its documentation lists the significant ones with reasons (for example `bpf`, `keyctl`, `mount`, `ptrace`, `unshare`).

## Step 1: RuntimeDefault everywhere
- Docker applies its default profile automatically (it disables around 44 system calls out of 300+) unless `--security-opt seccomp=unconfined`.
- **Kubernetes does not apply seccomp by default** (unconfined) unless the kubelet `--seccomp-default`
  flag (GA in 1.27) is set. Set per pod:
  ```yaml
  securityContext:
    seccompProfile:
      type: RuntimeDefault
  ```
  Pod Security Standards "restricted" requires RuntimeDefault or Localhost.
- Enable `seccompDefault: true` in kubelet config for cluster-wide defaults.

## Step 2: custom profiles for sensitive workloads
1. Record what the app uses: Security Profiles Operator (SPO) `ProfileRecording` with `recorder: Bpf` (eBPF) or
   `recorder: Logs` (audit or syslog), in a test environment while running the full test suite.
2. Generate an allowlist profile (`defaultAction: SCMP_ACT_ERRNO`, list `allow` syscalls).
3. Deploy:
   - Docker: `--security-opt seccomp=/path/profile.json`.
   - Kubernetes: place the file under the kubelet's seccomp directory on every node (`/var/lib/kubelet/seccomp/profiles/` in the Kubernetes tutorial; SPO instead distributes `SeccompProfile` objects and writes them under `/var/lib/kubelet/seccomp/operator/`) and
     ```yaml
     seccompProfile: {type: Localhost, localhostProfile: operator/my-namespace/myapp.json}
     ```
     `localhostProfile` is relative to the kubelet seccomp directory.
4. Start with `SCMP_ACT_LOG` default action to find missing syscalls, then switch to ERRNO.

## Debugging denials
- With `SCMP_ACT_ERRNO` the process sees a permission error (Docker's documentation: `Permission Denied`) or crashes; a profile whose default action logs (`SCMP_ACT_LOG`) records the calls instead, which the Kubernetes tutorial shows being read from the node's syslog.

## Stack with other controls
Seccomp + dropped capabilities + `allowPrivilegeEscalation: false` + read-only root FS + AppArmor/SELinux +
non-root user. In Kubernetes, privileged containers always run as `Unconfined`, so a seccomp profile cannot be applied to them.

## Gotchas
- Runtime or base image updates may need syscalls that were not in the recorded profile; re-record custom
  profiles after upgrades.
- A `Localhost` profile has to be present in the kubelet's seccomp directory on the node that runs the pod (the Kubernetes tutorial copies the profiles there before creating pods).

## Verify
`kubectl get pod -o jsonpath='{.spec.securityContext.seccompProfile}'` shows the profile; inside the
container `grep Seccomp /proc/1/status` shows a non-zero seccomp mode (the proc(5) `Seccomp` field reports the mode; 2 is filter mode); under Docker's default profile `unshare --map-root-user` is blocked (the example in Docker's seccomp page).

## Checked
Checked 2026-10-25 against the Kubernetes seccomp tutorial and Pod Security Standards (kubernetes/website, 2026-10-24), Docker's seccomp page (docker/docs, 2026-10-23), the Security Profiles Operator profiles guide (kubernetes-sigs/security-profiles-operator) and the kernel proc documentation. Confirmed: Docker default profile (about 44 of 300+ syscalls disabled, `SCMP_ACT_ERRNO` default action, `seccomp=unconfined` override); Kubernetes `RuntimeDefault` when `seccompDefault` is enabled, otherwise `Unconfined`; `--seccomp-default` GA in 1.27; restricted PSS requires `RuntimeDefault` or `Localhost`; privileged containers always run Unconfined; SPO `ProfileRecording` with `recorder: Bpf` or `Logs`; SPO profile path `operator/...`. Removed unconfirmed: `ausearch -m seccomp`/`ausyscall` steps, strace and OCI hook recording, glibc syscall names, and the claim that `unshare -r` fails (the Docker page uses `unshare --map-root-user`).

Method: documentation only; no commands were run.

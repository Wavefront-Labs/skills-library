---
id: computing-software.cybersecurity-defensive.system-hardening.linux-capabilities
name: linux-capabilities
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [linux-capabilities, cap-drop, container-hardening, cap-net-bind-service, cap-sys-admin, least-privilege]
level: practitioner
status: docs-checked
description: "Apply Linux capabilities for least privilege: drop ALL and add back only what is needed in containers and systemd units, file capabilities over setuid, and auditing."
sources: ["https://github.com/mkerrisk/man-pages/blob/master/man7/capabilities.7", "https://github.com/moby/moby/blob/master/daemon/pkg/oci/caps/defaults.go", "https://github.com/docker/cli/blob/master/docs/reference/commandline/container_run.md", "https://github.com/kubernetes/website/blob/main/content/en/docs/concepts/security/pod-security-standards.md", "https://github.com/kubernetes/website/blob/main/content/en/docs/tasks/configure-pod-container/security-context.md", "https://github.com/systemd/systemd/blob/main/man/systemd.exec.xml", "https://github.com/torvalds/linux/blob/master/Documentation/networking/ip-sysctl.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linux capabilities

Capabilities split root's powers into distinct units (`CAP_NET_BIND_SERVICE`, `CAP_SYS_ADMIN`, ...; see
capabilities(7) for the full list). Processes should hold only the capabilities they need; most need none.

## Dangerous capabilities to never grant casually
- `CAP_SYS_ADMIN`: overloaded (capabilities(7) says so); covers mount, namespace and many other administrative operations.
- `CAP_SYS_PTRACE`: trace and inspect arbitrary processes.
- `CAP_SYS_MODULE`: load and unload kernel modules.
- `CAP_DAC_READ_SEARCH`, `CAP_DAC_OVERRIDE`: bypass file read/search and other permission checks.
- `CAP_NET_ADMIN`, `CAP_NET_RAW` (raw and packet sockets; Docker's default set includes NET_RAW).
- `CAP_SETUID`/`CAP_SETGID`, `CAP_CHOWN`, `CAP_FOWNER`: change identities and ownership.
- `CAP_BPF` and `CAP_PERFMON` (both since Linux 5.8), `CAP_SYS_RAWIO`.

## Containers
Docker's default set (from the moby source) is CHOWN, DAC_OVERRIDE, FSETID, FOWNER, MKNOD, NET_RAW, SETGID, SETUID,
SETFCAP, SETPCAP, NET_BIND_SERVICE, SYS_CHROOT, KILL, AUDIT_WRITE. Drop them all:
```bash
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE --security-opt=no-new-privileges image
```
Kubernetes:
```yaml
securityContext:
  runAsNonRoot: true
  allowPrivilegeEscalation: false
  capabilities:
    drop: ["ALL"]
    add: ["NET_BIND_SERVICE"]     # only if binding <1024; better: listen on 8080
```
Pod Security Standards "restricted" requires dropping ALL and allows adding back only NET_BIND_SERVICE.
Never `privileged: true` except for vetted node agents.
Note: for a non-root process, capabilities survive `execve` only through file capabilities or the ambient set
(capabilities(7) transformation rules); listening on a high port avoids the question.

## systemd services
```ini
[Service]
User=app
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
AmbientCapabilities=CAP_NET_BIND_SERVICE
NoNewPrivileges=yes
```
Assigning the empty string to `CapabilityBoundingSet=` resets the bounding set to empty. `systemd-analyze security <unit>` scores the exposure.

## File capabilities instead of setuid
Replace setuid-root binaries with narrow file capabilities (`setcap(8)`), for example `setcap cap_net_raw+ep /usr/bin/ping`;
the kernel's `net.ipv4.ping_group_range` sysctl is the alternative that lets unprivileged users open ICMP echo sockets.
Audit with `getcap -r /` (see getcap(8)); unexpected entries, especially `cap_setuid` or `cap_dac_override` on interpreters
or editors, are privilege escalation paths.

## Inspect
- `grep Cap /proc/<pid>/status` shows the `CapInh`, `CapPrm`, `CapEff`, `CapBnd` and `CapAmb` masks; `capsh(1)` can decode them and `pscap(8)` (libcap-ng) lists capabilities of running
  processes.
- Find what an app actually needs: run with all dropped and read the errors, then add back one capability at a time.

## Verify
`docker inspect` / pod spec shows drop ALL; the `CapBnd` mask in `/proc/1/status` inside the container (decoded with `capsh`) is empty
(except approved adds); `getcap -r /` on hosts matches the approved list.

## Checked
Checked 2026-10-25. Sources: capabilities(7) (mkerrisk/man-pages mirror, last updated 2021, so newer capabilities may be missing from that copy), moby `defaults.go` for Docker's default capability set (14 entries, matches), Docker `container run` reference, Kubernetes Pod Security Standards (restricted: drop ALL, only NET_BIND_SERVICE may be added back; v1.22+, Linux-only enforcement v1.25+), Kubernetes security-context task, systemd.exec(5) (`CapabilityBoundingSet=`, `AmbientCapabilities=`, `NoNewPrivileges=`), and the kernel networking sysctl documentation (`ping_group_range`). Removed unconfirmed claims: the Shocker reference, the "about 40" count, distribution ICMP defaults and the bpftrace/BCC tracing tip.

Method: documentation only; no commands were run.

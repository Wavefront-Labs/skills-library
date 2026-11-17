---
id: computing-software.cloud-infrastructure-engineering.docker.custom-seccomp-profiles-and-denied-syscalls
name: custom-seccomp-profiles-and-denied-syscalls
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, seccomp, seccomp-profile, custom-seccomp, seccomp-json, seccomp-unconfined, seccomp-denied-syscall, seccomp-profile-generation, oci-seccomp-bpf-hook]
level: sme
description: "Diagnose syscalls blocked by Docker's default seccomp profile, write a custom seccomp JSON (allowlist or targeted additions), and generate profiles from traces."
sources: ["https://docs.docker.com/engine/security/seccomp/", "https://github.com/moby/profiles/blob/main/seccomp/default.json", "https://github.com/containers/oci-seccomp-bpf-hook", "https://docs.docker.com/reference/cli/dockerd/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom seccomp profiles and denied syscalls

## Diagnosing a denial
Symptom: `Operation not permitted` (EPERM) for something that works on the host, even as root
in the container, e.g. `unshare`, `mount`, `perf_event_open`, `io_uring_setup` (the Docker seccomp page lists the significant blocked syscalls and why).
```sh
docker run --rm --security-opt seccomp=unconfined app:1     # works now? -> seccomp is the cause
```
Never ship `seccomp=unconfined`: it removes the default filter, which blocks around 44 of 300+ syscalls.

## Writing a profile
Start from Docker's default (`moby/profiles` `seccomp/default.json`) and add only what you need:
```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "defaultErrnoRet": 1,
  "archMap": [{ "architecture": "SCMP_ARCH_X86_64", "subArchitectures": ["SCMP_ARCH_X86", "SCMP_ARCH_X32"] }],
  "syscalls": [
    { "names": ["accept4", "read", "write", "..."], "action": "SCMP_ACT_ALLOW" },
    { "names": ["io_uring_setup", "io_uring_enter", "io_uring_register"], "action": "SCMP_ACT_ALLOW" },
    { "names": ["personality"], "action": "SCMP_ACT_ALLOW",
      "args": [{ "index": 0, "value": 8, "op": "SCMP_CMP_EQ" }] }
  ]
}
```
```sh
docker run --security-opt seccomp=/etc/docker/seccomp/app.json app:1
```
daemon-wide: `"seccomp-profile": "/etc/docker/seccomp/default-plus.json"`.
Compose: `security_opt: ["seccomp=/etc/docker/seccomp/app.json"]` (the CLI sends the profile contents to the daemon, so the file must exist on the client host).
- Default profile also allows some syscalls **conditionally on capabilities** (`includes.caps`):
  adding `--cap-add SYS_ADMIN` unlocks `mount`, etc. Keep that structure when copying.
- `io_uring_setup`, `io_uring_enter` and `io_uring_register` are blocked by default because of
  vulnerabilities that can be exploited to break out of containers (moby/moby#46762); allow them only
  if you accept that risk.

## Generating from traces
- **oci-seccomp-bpf-hook** (Podman): `sudo podman run --annotation io.containers.trace-syscall="of:/path/out.json" app:1`
  records the syscalls the container makes and writes a profile to the `of:` path (`of:` is mandatory;
  an optional `if:` input file gives a baseline, and syscalls blocked in the baseline stay blocked).
Generated profiles miss rare code paths (error handling, signals, DNS fallbacks): run the full
test suite before enforcing.

## Verify
`docker inspect -f '{{.HostConfig.SecurityOpt}}' app`; `grep Seccomp /proc/1/status` inside
shows `2` (filter mode); the previously failing call now succeeds and a disallowed one returns EPERM.

## Checked
Date: 2026-10-24. Documentation: Docker docs seccomp page and `dockerd` reference (docker/docs main), moby/profiles `seccomp/default.json` (main), containers/oci-seccomp-bpf-hook README.
- Confirmed the default profile uses `defaultAction` `SCMP_ACT_ERRNO` with `defaultErrnoRet` 1, an `archMap`, `SCMP_ARCH_X86_64` sub-architectures, a `personality` rule with `args` `index 0` `value 8` `op SCMP_CMP_EQ`, and `includes.caps` (for example `CAP_SYS_ADMIN` unlocks `mount`, `unshare`, `clone3`, `perf_event_open`).
- Confirmed `--security-opt seccomp=<file>`, `seccomp=unconfined`, the daemon `seccomp-profile` option, the "around 44 of 300+" figure, the io_uring block and the oci-seccomp-bpf-hook annotation grammar (`of:` mandatory, `if:` optional).
- Removed strace, dmesg, `SCMP_ACT_LOG`, `perf trace` and Inspektor Gadget guidance that no checked source covers.
Method: documentation only; no commands were run.

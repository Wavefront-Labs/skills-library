---
id: computing-software.cloud-infrastructure-engineering.docker.tracee-and-tetragon-for-container-runtime-security
name: tracee-and-tetragon-for-container-runtime-security
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, tracee, tetragon, ebpf, runtime-security, falco-alternative, tracing-policy, enforcement, container-monitoring, btf]
level: advanced
status: docs-checked
description: "Run Aqua Tracee and Cilium Tetragon on Docker hosts as eBPF runtime security: install commands, event selection, TracingPolicies with kill enforcement, and choosing vs Falco."
sources: ["https://aquasecurity.github.io/tracee/latest/docs/install/docker/", "https://aquasecurity.github.io/tracee/latest/docs/flags/scope.1/", "https://aquasecurity.github.io/tracee/latest/docs/flags/output.1/", "https://tetragon.io/docs/installation/container/", "https://tetragon.io/docs/concepts/tracing-policy/", "https://tetragon.io/docs/concepts/enforcement/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tracee and Tetragon for container runtime security

Both are eBPF-based like Falco's modern driver; they differ in focus.

| | Falco | Tracee (Aqua) | Tetragon (Cilium/Isovalent) |
|---|---|---|---|
| Model | rules over syscall events | events + built-in detections | TracingPolicies on kprobes, tracepoints and uprobes |
| Enforcement | alert only | alert only | can send a signal (for example SIGKILL) or override a function's return value |
| Output | JSON, Falcosidekick | table, JSON, gotemplate; file, webhook and forward destinations | JSON export, `tetra` CLI, gRPC |

Kernel requirements: BTF (`/sys/kernel/btf/vmlinux` present); check each project's prerequisites page for the supported kernels.

## Tracee on a Docker host
```bash
docker run --name tracee -d --rm \
  --pid=host --cgroupns=host --privileged \
  -v /etc/os-release:/etc/os-release-host:ro \
  -v /var/run:/var/run:ro \
  aquasec/tracee:latest
docker logs -f tracee            # signature detections as JSON
```
Narrow scope and events:
```bash
docker run ... aquasec/tracee:latest \
  --scope container --events execve,security_file_open \
  --output destinations.stdout_json.format=json
```
- `--scope container` selects events that originate from a container; `--scope container=new`
  selects newly created containers and `container=started` containers that finished starting.
- `--events` takes event names (prefix `-` to exclude) or `tag=<tag>` selections.
- `--output` uses `destinations.<name>.<field>=<value>`; the format is `json`, `table` or
  `gotemplate=<file>` (default `table` for a file, `json` for webhook and forward destinations).
- `--artifacts executable` captures executed files and `--artifacts network` captures
  traffic as pcap; this costs disk. YAML detectors are loaded from `/etc/tracee/detectors` by default (`--detectors`).

## Tetragon on a Docker host
```bash
docker run --name tetragon -d --rm \
  --pid=host --cgroupns=host --privileged \
  -v /sys/kernel/btf/vmlinux:/var/lib/tetragon/btf \
  -v "$PWD/policies":/etc/tetragon/tetragon.tp.d:ro \
  quay.io/cilium/tetragon:<version>
docker exec tetragon tetra getevents -o compact     # process exec/exit events
```
The container docs give the first command (without the policy mount); the daemon automatically loads
policies from `/etc/tetragon/tetragon.tp.d/` (change it with `--tracing-policy-dir`), and
`--tracing-policy` loads one file. Settings can also be passed as `TETRAGON_*` environment variables or
drop-ins in `/etc/tetragon/tetragon.conf.d/`. Example policy from the Tetragon docs, which
kills any process that creates a file descriptor for `/tmp/tetragon` (illustration only: the
docs warn it can be bypassed, for example with hard links):
```yaml
apiVersion: cilium.io/v1alpha1
kind: TracingPolicy
metadata:
  name: "fd-install"
spec:
  kprobes:
  - call: "fd_install"
    syscall: false
    args:
    - index: 0
      type: "int"
    - index: 1
      type: "file"
    selectors:
    - matchArgs:
      - index: 1
        operator: "Equal"
        values:
        - "/tmp/tetragon"
      matchActions:
      - action: Sigkill
```
The default selector action is `Post` (post an event, observe only); other actions include `Sigkill`,
`Override` and `Signal`. Start observing and add enforcement after a soak period; enforcement mistakes
kill legitimate processes.

## Choosing
- Falco: a community-maintained ruleset with output forwarding through Falcosidekick.
- Tracee: built-in events and detections, with artifact capture.
- Tetragon: policies that can enforce (signal or override return value) and Kubernetes integration.
Pick one primary tool per host to keep the rule and policy sets manageable.

## Verify
```bash
docker exec tetragon tetra getevents -o compact        # Tetragon: shows exec/exit and policy matches
docker logs tracee 2>&1 | tail -5                       # Tracee: recent events
```

## Checked
Documentation release: aquasecurity/tracee v0.24.1 docs (install/docker, flags scope, events, artifacts, output, detectors) and cilium/tetragon v1.7.1 docs (installation/container, tracing-policy index, selectors, enforcement, example, daemon configuration), checked 2026-10-26.
Confirmed: Tracee `docker run` flags and mounts; `--scope container`, `container=new`, `container=started`; `--events` syntax; `--output destinations.<name>.format`; `--artifacts executable|network`; Tetragon container run command, `tetra getevents -o compact`, `/etc/tetragon/tetragon.tp.d/` default policy directory, `--tracing-policy-dir`, `TracingPolicy` kprobe structure with `matchArgs`/`matchActions`, `Sigkill`, default action `Post`, enforcement by signals and return-value override.
Corrected: Tracee `--output json` and `--capture` no longer exist (replaced by `--output destinations...` and `--artifacts`); signatures are now YAML detectors; the Tetragon image pin v1.2.0 was replaced by a placeholder and the `/etc/passwd` MAY_WRITE policy by the documented `fd_install` example. Removed as unsupported: `TRC-*` signature categories, the kernel version thresholds, the metadata-source row, "default runs signatures only", the `exit 137` check and the overhead claim.
Method: documentation only; no commands were run.

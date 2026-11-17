---
id: computing-software.cloud-infrastructure-engineering.docker.runtime-security-monitoring-with-falco
name: runtime-security-monitoring-with-falco
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, falco, runtime-security, container-monitoring, audit, auditd, docker-events, ebpf, falco-rules, falcosidekick, intrusion-detection, drift-detection, syscall-monitoring, falco-install, falco-docker, falco-custom-rules]
level: advanced
status: docs-checked
description: "Detecting bad behaviour in running containers: Falco on a Docker host (eBPF driver, container metadata, custom rules, Falcosidekick alerts), auditd rules for the daemon, docker events audit."
sources: ["https://falco.org/docs/setup/container/", "https://falco.org/docs/concepts/rules/overriding/", "https://falco.org/docs/concepts/event-sources/kernel/", "https://github.com/falcosecurity/rules", "https://github.com/falcosecurity/falcosidekick", "https://github.com/docker/docker-bench-security", "https://docs.docker.com/reference/cli/docker/system/events/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Runtime security monitoring with Falco

**Goal:** get an alert within seconds when a container spawns a shell, writes to `/etc`,
reads a secret it shouldn't, or someone `docker exec`s into production — and have an
audit trail for who touched the daemon.

## Falco on a plain Docker host
Falco watches syscalls from the kernel (not the container), so it sees every container
without any agent inside images. The modern eBPF probe is the default driver, is bundled in the
Falco binary and needs no driver installation. The Falco container docs give this command:
```bash
docker run --rm -it \
  --privileged \
  -v /sys/kernel/tracing:/sys/kernel/tracing:ro \
  -v /var/run/docker.sock:/host/var/run/docker.sock \
  -v /proc:/host/proc:ro \
  -v /etc:/host/etc:ro \
  falcosecurity/falco:<version>
```
- The docker socket mount is what lets Falco enrich events with container metadata.
- The `tracefs` mount (`/sys/kernel/tracing`, or `/sys/kernel/debug/tracing` on some systems) is
  optional but recommended: without it you lose the TOCTOU mitigation.
- Least privilege (recommended in the docs): replace `--privileged` with `--cap-drop all
  --cap-add sys_admin --cap-add sys_resource --cap-add sys_ptrace` (the documented minimum for modern eBPF is
  `CAP_SYS_PTRACE`, `CAP_SYS_RESOURCE`, `CAP_BPF`, `CAP_PERFMON`; the command uses `CAP_SYS_ADMIN` because
  Docker did not support the last two).
- The other driver is the kernel module (`falco -o engine.kind=kmod`), which needs the driver
  installed on the host first with the `falcosecurity/falco-driver-loader` image and cannot run with capabilities alone.
- The modern eBPF probe needs BPF ring buffer support and a kernel that exposes BTF; kernels
  from about 5.8 usually qualify.
- A package install of Falco runs as a service and is the simpler option on a long-lived host.

## The default rules worth knowing (and tuning)
Falco's default configuration loads `/etc/falco/falco_rules.yaml`, then
`/etc/falco/falco_rules.local.yaml`, then `/etc/falco/rules.d` (the `rules_files` list in
`falco.yaml`). Only the **stable** rules from the falcosecurity/rules repository are bundled by
default; **incubating** and **sandbox** rule files must be added. Rules worth knowing:
- Stable: `Terminal shell in container` (a shell with an attached terminal, such as `docker exec -it ... sh`),
  `Read sensitive file untrusted`, `Contact K8S API Server From Container`.
- Incubating: `Launch Package Management Process in Container`.
- Sandbox: `Write below etc`, `Write below binary dir`, `Modify binary dirs` and
  `Container Drift Detected (chmod)` / `(open+create)`; the two drift rules are shipped with
  `enabled: false`.

Override, don't edit: put files in `/etc/falco/rules.d/` (listed after the defaults, so they can
override). Mute per container/image:
```yaml
- list: allowed_shell_images
  items: [docker.io/library/busybox, ghcr.io/org/debug-sidecar]
- rule: Terminal shell in container
  condition: and not container.image.repository in (allowed_shell_images)
  override: {condition: append}
```
A custom rule:
```yaml
- rule: Secret file read by app container
  desc: app read a mounted secret outside startup
  condition: >
    open_read and container and fd.name startswith /run/secrets/
    and container.image.repository = "ghcr.io/org/api"
    and proc.name != "api"
  output: "secret read by %proc.name in %container.name (%container.image.repository) file=%fd.name user=%user.name"
  priority: WARNING
  tags: [custom, secrets]
```
`falco -L` shows the name and description of all rules; `falco --validate rules.d/custom.yaml`
(`-V`) validates rule files and exits; `falco --dry-run` checks the configuration and rules without processing
events. Rule tuning is the whole job: expect a period of adding exceptions before alerts are trusted.

## Shipping alerts
Falco prints JSON when `json_output: true` is set in `falco.yaml`. **Falcosidekick** forwards
Falco events to many destinations (it listens on port 2801 by default):
```bash
docker run -d --name falcosidekick -p 2801:2801 \
  -e SLACK_WEBHOOKURL=<WEBHOOK> falcosecurity/falcosidekick
# falco.yaml:  http_output: {enabled: true, url: "http://falcosidekick:2801/"}
```
Falcosidekick UI gives a web view. The `priority` setting in `falco.yaml` is the minimum rule
priority that is loaded and run, so raising it (for example to `warning`) also reduces noise.

## The cheap layer: docker events and auditd
Even without Falco, record who does what to the daemon:
```bash
docker events --filter type=container --filter event=exec_create --format '{{json .}}'
```
(`exec_create`, `exec_start` and `exec_die` are documented container events.) Run that under a
service piping to your log shipper. The CIS Docker Benchmark checks implemented by
docker-bench-security (section 1.1) ask for auditd watch rules on Docker files, for example:
```
-w /usr/bin/dockerd -k docker
-w /var/lib/docker -k docker
-w /etc/docker -k docker
-w /etc/docker/daemon.json -k docker
```
The tool's remediation text adds them to the audit rules under `/etc/audit/rules.d/` and restarts
the audit daemon; `docker-bench-security` checks that they are present.

## Alternatives
Tracee (Aqua, eBPF) and Tetragon (Cilium, can *enforce* by sending a signal such as SIGKILL,
not just alert); see `tracee-and-tetragon-for-container-runtime-security`. gVisor/Kata
(`alternative-runtimes`) reduce the attack surface instead of watching it; they are
complementary.

## Verify
```bash
docker run --rm -it alpine sh -c 'cat /etc/shadow'
docker logs falco --since 1m | grep -E 'shell was spawned|sensitive file'
```
`Terminal shell in container` and `Read sensitive file untrusted` should fire; the event-generator
project (falcosecurity/event-generator) can produce further test events for specific rules.
Without the docker socket mount, container metadata fields in the output are not populated.

## Checked
Documentation release: Falco 0.45.1 (falcosecurity/falco falco.yaml and CLI options source), falcosecurity/falco-website docs (setup/container, kernel event sources, rules overriding and controlling pages, master as of 2026-10-24), falcosecurity/rules (stable, incubating and sandbox rule files), falcosidekick README, docker-bench-security tests, Docker engine `docker system events` reference, checked 2026-10-26.
Confirmed: modern eBPF is the default engine; kernel module needs prior driver install; container run commands and capabilities; tracefs mount and TOCTOU note; `rules_files` order; stable/incubating/sandbox split and where each named rule lives; drift rules `enabled: false`; `-L`, `-V/--validate`, `--dry-run`; `json_output`, `http_output`, `priority`; Falcosidekick port 2801 and `SLACK_WEBHOOKURL`; CIS 1.1 auditd checks for `/usr/bin/dockerd`, `/var/lib/docker`, `/etc/docker`, `/etc/docker/daemon.json`; `exec_create` event.
Corrected: dropped `-e FALCO_BPF_PROBE`, the classic `engine.kind=ebpf` option, `--list-drivers`, `falco-no-driver`; rule names were attributed to the wrong rule files (only three are in the default stable file); removed `Outbound Connection to C2 Servers`, `SLACK_MINIMUMPRIORITY`, the `<NA>` container name, `augenrules`/`ausearch` commands, the `containerd.sock` and `docker.sock` audit paths and the `docker events` attribute names as unsupported by the sources read.
Method: documentation only; no commands were run.

---
id: computing-software.cloud-infrastructure-engineering.podman.generate-systemd-deprecated-units
name: generate-systemd-deprecated-units
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [generate-systemd, deprecated, unit-files, restart-policy, new, files, sdnotify]
level: practitioner
status: docs-checked
description: "Use deprecated podman generate systemd: --files, --new, --name, restart policy, dependencies, prefixes, sdnotify override and pod infra needs."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-generate-systemd.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: generate legacy unit files when Quadlet is not an option.

The command is deprecated: the page recommends Quadlet files, says there are no plans to remove the command, and that it only gets urgent bug fixes. `podman generate systemd [options] container|pod` prints unit content to stdout. Pod units require the pod to have an infra container (`--infra=true`), which lives for the pod's whole life.

Options: `--files`/`-f` writes `{container,pod}-{ID,name}.service` files into the current directory (with SELinux, the files inherit that directory's context, so `restorecon`, `chcon`, `semanage` or `-Z` on `mv`/`cp` may be needed). `--name`/`-n` uses the container name in start, stop and description. `--format` prints JSON. `--no-header` drops the metadata header.

`--new` yields units that create and remove containers at start and stop (`ExecStartPre`, `ExecStopPost`) so they are not tied to one machine; best effort, review before production. It only works for containers and pods made directly with Podman, not via the REST API or `podman kube play`.

Dependencies and naming: `--after`, `--requires`, `--wants` (appended; defaults like `online.target` are not removed), `--container-prefix` (default `container`), `--pod-prefix` (default `pod`), `--separator` (default `-`).

Restart: `--restart-policy` is one of no, on-success, on-failure, on-abnormal, on-watchdog, on-abort, always (default on-failure); `--restart-sec`, `--start-timeout`, `--stop-timeout` in seconds. A custom `--restart` on the container without `--new` can cause shutdown issues, so set the policy at generation time instead.

The generated `podman run` uses `--sdnotify` from the container, but replaces unset or `ignore` with `conmon`, because almost no workloads send notify messages and systemd would wait forever.

## Checked

2026-11-09. Read against the official page text (podman-generate-systemd.1); options, defaults, restart-policy values, the --new limits and the sdnotify note were confirmed there. Nothing removed.
Method: documentation only; no commands were run.


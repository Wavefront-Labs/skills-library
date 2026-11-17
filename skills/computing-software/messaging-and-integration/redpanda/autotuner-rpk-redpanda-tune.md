---
id: computing-software.messaging-and-integration.redpanda.autotuner-rpk-redpanda-tune
name: autotuner-rpk-redpanda-tune
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [rpk, autotuner, tuning, linux, redpanda-tuner, production-mode]
level: advanced
status: docs-checked
description: "Run and persist hardware tuning with rpk redpanda tune: enable tuners via rpk.tune keys, list support, use production mode, and start the redpanda-tuner service at boot."
sources:
  - https://docs.redpanda.com/streaming/current/reference/rpk/rpk-redpanda/rpk-redpanda-tune/
  - https://docs.redpanda.com/streaming/current/reference/rpk/rpk-redpanda/rpk-redpanda-tune-list/
  - https://docs.redpanda.com/streaming/current/deploy/redpanda/manual/linux-system-tuning/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`rpk redpanda tune` (the autotuner) analyzes the node's hardware and sets kernel options. It is Linux only, needs root privileges, and the page warns not to use it in Azure self-managed environments. Redpanda recommends running it as part of production deployment workflows.

**Commands**
- `rpk redpanda tune list` shows each tuner with ENABLED, SUPPORTED and an UNSUPPORTED-REASON.
- `rpk redpanda tune all` runs every tuner; `rpk redpanda tune <tuner>` runs one; `rpk redpanda tune help <tuner>` explains it.
- `rpk redpanda mode prod` enables the predetermined production set by changing `redpanda.yaml`.

**Enabling a tuner** is a node property in `redpanda.yaml` under `rpk`:

```text
rpk:
    tune_cpu: true
    tune_swappiness: true
```

or from the CLI (the `aio_events` key is `rpk.tune_aio_events`):

```bash
rpk redpanda config set rpk.tune_aio_events true
```

**Useful flags:** `--cpu-set` (cpuset format), `-r/--dirs` data directories, `-d/--disks`, `-n/--nic`, `-m/--mode` (`sq`, `sq_split`, `mq`), `--reboot-allowed` (lets tuners change boot parameters and request a reboot), `--output-script FILE` (generate a tuning script), `--timeout`.

**Persisting across reboots:** the `redpanda-tuner` service runs `rpk redpanda tune all`. On RHEL after installing the rpm, run `sudo systemctl start redpanda-tuner` and `sudo systemctl enable redpanda-tuner`. On Ubuntu with the apt package it is already enabled; just start it.

Kubernetes: tune at the host node level instead.

## Checked

2026-11-04. Tuner names, flags, the tuner list example, production mode, the YAML keys and the redpanda-tuner service steps were confirmed on the rpk redpanda tune and tune list pages. The Kubernetes note and recommendation come from the Linux System Tuning page.

Method: documentation only; no commands were run.

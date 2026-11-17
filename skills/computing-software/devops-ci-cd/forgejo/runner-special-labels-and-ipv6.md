---
id: computing-software.devops-ci-cd.forgejo.runner-special-labels-and-ipv6
name: runner-special-labels-and-ipv6
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [special-labels, multi-label-runs-on, enable-ipv6, daemon-json]
level: advanced
status: docs-checked
description: "Route jobs to special hardware with multi-value runs-on and enable IPv6 in runner-created networks."
sources:
  - https://forgejo.org/docs/latest/admin/actions/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Special labels mark capabilities. If three runners share `docker` but only one has a GPU, give that runner a `gpu` label and let jobs ask for both:

```
runs-on: [docker, gpu]
```

with runner labels such as `docker:docker://ghcr.io/catthehacker/ubuntu:act-22.04` and `gpu:docker://...`. Only a runner with both labels takes the job, and the containerization platform comes from the first label in the `runs-on` array.

IPv6 is off by default in networks the runner creates. For Docker, the daemon needs `/etc/docker/daemon.json` with at least `ipv6: true`, `experimental: true`, `ip6tables: true`, a `fixed-cidr-v6` and `default-address-pools`, then `systemctl restart docker.service`. Test with a workflow that runs `curl http://ipv6.google.com`; with `forgejo-runner exec` it fails until you add `--enable-ipv6`. Finally set in the runner config:

```
container:
  enable_ipv6: true
```

and restart the daemon. Rootless Podman uses tap networks with their own limitations.

Labels are declared under `runner.labels` in the runner configuration file, and Forgejo inspects a job's `runs-on` field to evaluate which runners can run it.

## Checked

Date: 2026-11-07
Confirmed against the "Forgejo Runner Configuration" page, read in full including its code blocks (the page is long; the Cache configuration and configuration reference sections were read but are not used here): the multi-label `runs-on: [docker, gpu]` example and the two matching `runner.labels` entries, "only a runner with both labels", the containerization platform taken from the first label, IPv6 off by default, the `/etc/docker/daemon.json` keys (`ipv6`, `experimental`, `ip6tables`, `fixed-cidr-v6`, `default-address-pools`), `systemctl restart docker.service`, the `curl http://ipv6.google.com` test workflow, the `forgejo-runner exec --enable-ipv6` behaviour, `container.enable_ipv6: true`, and the rootless Podman tap-network note.
Corrected: the final sentence over-generalised label matching; it now says only what the page states. Page-cited URLs `ipv6.google.com` and `example.com` are test targets, not sources.
Method: documentation only; no commands were run.

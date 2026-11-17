---
id: computing-software.cloud-infrastructure-engineering.podman.generate-systemd-templates-and-kube-service
name: generate-systemd-templates-and-kube-service
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [generate-systemd, template, env, podman-kube-service, systemd-escape, kubernetes-yaml, instances]
level: advanced
status: docs-checked
description: "Run many instances from one generated unit with --template, forward environment variables with --env, and run Kubernetes YAML with the podman-kube@.service template."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-generate-systemd.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: parameterise generated units and launch YAML workloads under systemd.

`--template` adds template specifiers so one unit file runs multiple services. If `--new` was not set it is set to true automatically; the command fails if `--new` is explicitly set to false.

`--env`/`-e` sets environment variables in the unit files. A variable given without a value is read from the host environment and set only if it exists there. As a special case, a name ending in `*` without a value adds every host variable starting with that prefix.

Kubernetes integration: a YAML file can run through the `podman-kube@.service` template whose argument is the escaped path of the file. For `workload.yaml` in the home directory:

```
$ escaped=$(systemd-escape ~/workload.yaml)
$ systemctl --user start podman-kube@$escaped.service
$ systemctl --user is-active podman-kube@$escaped.service
active
```

For containers from `podman kube play`, this template is the supported route, because `--new` does not work for them.

Remote clients: with the remote client (including Mac and Windows, excluding WSL2), place the generated units on the remote system and make sure `XDG_RUNTIME_DIR` is set, for example `export XDG_RUNTIME_DIR=/run/user/$(id -u)`.

## Checked

2026-11-09. Read against the official page text (podman-generate-systemd.1); --template, --env, the podman-kube@.service example and the remote-client note were confirmed there. Nothing removed.
Method: documentation only; no commands were run.


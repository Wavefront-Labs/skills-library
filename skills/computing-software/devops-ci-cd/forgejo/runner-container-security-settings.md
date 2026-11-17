---
id: computing-software.devops-ci-cd.forgejo.runner-container-security-settings
name: runner-container-security-settings
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [container-privileged, container-network, valid-volumes, container-options]
level: advanced
status: docs-checked
description: "Review the security-sensitive container.* runner settings and keep their safe defaults."
sources:
  - https://forgejo.org/docs/latest/admin/actions/security/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For Docker labels, several keys in the runner's `container` section are security sensitive; the defaults minimise risk.

- `container.privileged` defaults to `false`. When `true`, job, service and step containers start with `--privileged`, which lets an attacker who can change workflows act as root on the runner machine.
- `container.network` defaults to `""`, creating a new isolated network per job. `"host"` removes job isolation and exposes services bound to 127.0.0.1; `"bridge"` allows access to other containers on the default bridge; a custom network name isolates the network of all job containers but not from each other, and with `runner.capacity` above 1 can cause container name conflicts (two service containers with the same name make DNS round-robin between them).
- `container.valid_volumes` defaults to `[]`. Volumes listed can be read and written by any workflow, so treat their data as non-confidential and unverified.
- `container.options` can limit resources, for example `--memory=1g` or `--cpus=2`, combined with `runner.capacity`. There is no cap on service containers per job and no disk or network I/O limits.
- Docker or Podman logins to private registries make those images available to any workflow using `container:`.

The page's job timeout default is 3 hours (`runner.timeout`), so with capacity 1 a loop can block the runner that long.

## Checked

Date: 2026-11-07
Confirmed against the "Securing Forgejo Actions Deployments" page, read in full: the defaults of `container.privileged` (`false`), `container.network` (`""`), `container.valid_volumes` (`[]`), the `--privileged` effect, host/bridge/custom network behaviour, `--memory=1g` and `--cpus=2`, no limit on service containers and no disk or network I/O limits, private registry login behaviour, and the 3 hour default job timeout with `runner.capacity` of 1.
Corrected: the custom-network bullet said it isolates "from the host"; the page says it isolates the network of all job containers but not from each other. Added the DNS round-robin detail from the page. Reworded the timeout sentence, which the page states as "the default 3 hour job timeout".
Method: documentation only; no commands were run.

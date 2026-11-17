---
id: computing-software.cloud-infrastructure-engineering.portainer.keep-portainer-configuration-persistent
name: keep-portainer-configuration-persistent
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [persistence, volumes, swarm, placement-constraint, storageclass]
level: practitioner
status: docs-checked
description: "Ensure Portainer data survives restarts and rescheduling on Docker, Swarm and Kubernetes, and change its port or run under SELinux."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/faqs/installing/how-can-i-ensure-portainers-configuration-is-retained.md
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/faqs/installing/how-do-i-change-the-port-that-portainer-runs-on.md
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/faqs/installing/my-host-is-using-selinux.-can-i-use-portainer.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Docker Standalone: the `portainer_data` volume from the install guide keeps configuration through restart, upgrade or removal of the container.

Docker Swarm: the recommended stack constrains Portainer to a manager node, fine with a single manager. With multiple managers, each stack or service update could move the container between managers and it would lose its data. Pin it: note the hostname of the node holding the volume, open Services, choose the `portainer_portainer` service, click Placement constraints, add a constraint with Name `node.hostname` and the hostname as Value.

Kubernetes: use a default StorageClass backed by cluster-available storage, or restrict the pod to a chosen node with a nodeSelector as described in the install guide.

Changing the port: Portainer listens on 9443 by default. Edit the `-p` mapping, for example `-p 443:9443` to serve on 443.

SELinux: to manage a local Docker environment with SELinux enabled, add `--privileged` to the `docker run` command, for either edition. The page also links a helper.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. Removed the unconfirmed description of the linked SELinux helper.

Method: documentation only; no commands were run.

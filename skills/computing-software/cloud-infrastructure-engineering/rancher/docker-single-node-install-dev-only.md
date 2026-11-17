---
id: computing-software.cloud-infrastructure-engineering.rancher.docker-single-node-install-dev-only
name: docker-single-node-install-dev-only
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [docker, single-node, privileged, development, migration, backup-operator]
level: intro
status: docs-checked
description: "The single-container Docker install of Rancher: dev and test only, the privileged flag, certificate options, and migrating to an HA cluster with the backup operator."
sources:
  - https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/other-installation-methods/rancher-on-a-single-node-with-docker
  - https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/installation-references/tls-settings
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Docker install runs Rancher in one container on one Linux host and is recommended **only for development and testing**. The page carries a Docker support warning, and says the ability to move to a high-availability cluster depends on the Rancher version. Where it is possible, use the Rancher backup operator to migrate from the Docker install to an HA Kubernetes cluster by following the migrate-to-a-new-cluster guide.

The container must be run with `--privileged`. A local Kubernetes cluster is installed inside the container, many Rancher features run as deployments, and privileged mode is required to run containers within containers.

Five SSL options are listed: the default Rancher-generated self-signed certificate; your own self-signed certificate; your own certificate signed by a recognised CA; Let's Encrypt; and localhost tunnelling with no certificate. The simplest, for non-identity-sensitive environments, is:

```
docker run -d --restart=unless-stopped \
  -p 80:80 -p 443:443 \
  --privileged \
  rancher/rancher:latest
```

For your own certificates the files must be PEM, with your certificate first followed by intermediates, and are mounted into the container with `-v`. For an external load balancer, a proxy, a custom CA, air gap or API auditing, the page points to separate Docker-specific pages.

Related knob for Docker installs: TLS defaults to TLS 1.2 with a restricted cipher list, adjustable with the `CATTLE_TLS_MIN_VERSION` and `CATTLE_TLS_CIPHERS` environment variables.

## Checked

2026-11-04. Checked against the Rancher Manager documentation pages: Installing Rancher on a Single Node Using Docker; TLS Settings. Removed the CATTLE_BOOTSTRAP_PASSWORD claim, which is not on the cited pages.

Method: documentation only; no commands were run.

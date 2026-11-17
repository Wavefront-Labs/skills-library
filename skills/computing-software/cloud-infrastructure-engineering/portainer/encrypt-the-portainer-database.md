---
id: computing-software.cloud-infrastructure-engineering.portainer.encrypt-the-portainer-database
name: encrypt-the-portainer-database
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [encryption, boltdb, secret, docker-standalone]
level: advanced
status: docs-checked
description: "Encrypt Portainer's BoltDB database with a mounted secret, and understand that the change is not reversible."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/advanced/db-encryption.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Portainer stores configuration in a BoltDB database inside the `portainer_data` volume. You can encrypt it with a secret provided when the Server starts. Encryption can be added at initial install or to an existing instance, and at present it is not reversible, so decide before you do it and keep the secret safe: it is the key.

On Docker Standalone:

1. Create a text file containing the secret on the Docker host, somewhere secure, for example `/path/to/secrets/portainer`.
2. If Portainer is running, `docker stop portainer` and `docker rm portainer` (the data volume stays).
3. Re-run the container with a bind mount of that file into the container as a secret, for example `-v /path/to/secrets/portainer:/run/secrets/portainer`, alongside the usual socket and `portainer_data:/data` mounts.

The page's Business Edition and Community Edition commands differ: the BE tab shows the mount target as `/run/portainer/portainer` while the text and the CE tab use `/run/secrets/portainer`, so check the page for your edition before relying on a path. On Swarm the secret is a Docker secret named `portainer` mounted at `/run/secrets/portainer` (added with `docker service update --secret-add` or in the stack file); on Kubernetes it is a secret mounted as a volume. Follow the page for the exact manifests.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. Fixed the claim that the editions differ only by image name (the mount path differs on the page).

Method: documentation only; no commands were run.

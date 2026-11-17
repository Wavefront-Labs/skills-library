---
id: computing-software.messaging-and-integration.node-red.node-red-docker-install-and-data
name: node-red-docker-install-and-data
category: computing-software
field: messaging-and-integration
product: node-red
tags: [node-red, docker, docker-volume, data-folder, nodered-node-red, uid-1000, bind-mount, image-tags]
level: practitioner
status: docs-checked
description: "Run Node-RED in Docker with the nodered/node-red image, persist /data in a named volume or bind mount with the right ownership, update the image, and choose Alpine or Debian tags."
sources: ["https://nodered.org/docs/getting-started/docker"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Node-RED in Docker

Quick start:

```
docker run -it -p 1880:1880 -v node_red_data:/data --name mynodered nodered/node-red
```

`-p 1880:1880` connects host port 1880 to the container's port 1880, `-v node_red_data:/data` mounts a named volume at `/data`, where Node-RED stores user configuration data, and `--name mynodered` names the container. Detach with `Ctrl-p Ctrl-q` (the container keeps running), reattach with `docker attach mynodered`, and use `docker start mynodered` and `docker stop mynodered`. The Docker Hub repository has been `nodered/node-red` since Node-RED 1.0.

Images support amd64, arm32v6, arm32v7, arm64v8 and s390x. Docker discovers the host architecture and pulls the matching tag, so the same `docker run` works across systems. Docker's architecture detection fails for arm32v6 (Raspberry Pi Zero or 1); there you must give the full image tag. The images are based on Alpine Node.js images to stay small, which removes dependencies needed to compile native modules; since Node-RED 3.1.0 there is also a Debian based image for nodes with native components.

Bind mount: `-v <host-dir>:/data`. The Node-RED user in the container is uid 1000 by default and must match the owner of the host directory; the page's migration note suggests `sudo chown -R 1000:1000 <host-dir>` to force that.

Named volume backup while running: `docker cp mynodered:/data /your/backup/directory`. Update with `docker pull nodered/node-red`, `docker stop mynodered`, `docker rm mynodered`, then the same `docker run` again; `/data` is preserved. The first start warns that the credentials file is encrypted with a system-generated key; set your own with the `credentialSecret` option in the settings file (the page shows `process.env.NODE_RED_CREDENTIAL_SECRET` with `-e` on `docker run`).

## Checked

2026-11-04. Confirmed against the Node-RED user guide page Running under Docker. Removed: the list of what /data holds beyond 'user configuration data' and the claim that chown is always required (the page ties it to uid matching and 0.20 to 1.0 migration).

Method: documentation only; no commands were run.

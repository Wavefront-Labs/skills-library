---
id: computing-software.systems-network-administration.frigate.frigate-docker-installation-and-storage
name: frigate-docker-installation-and-storage
category: computing-software
field: systems-network-administration
product: frigate
tags: [installation, docker-container, storage-paths, ports, shm-size, tmpfs-cache, mqtt-broker]
level: practitioner
status: docs-checked
description: "Install Frigate as a Docker container, understand its storage locations and ports, size shared memory and choose a host OS."
sources: ["https://docs.frigate.video/frigate/installation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Installing Frigate with Docker

Frigate is a Docker container that runs on any Docker host, including as a Home Assistant App (not the same as the Home Assistant integration). An MQTT broker is optional, but required for the integration, and both must use the same broker.

Host: bare-metal Debian-based Docker gives the best performance because Coral and GPU devices need low-overhead access. Running in a VM on Proxmox, ESXi or Virtualbox is not recommended, though some users have had success with Proxmox. Windows is not officially supported.

Container paths: `/config` holds the config file and SQLite database; `/media/frigate/clips` holds snapshots; `/media/frigate/recordings` holds recording segments; `/media/frigate/exports` holds exported clips; `/tmp/cache` is the segment cache (a 1 GB tmpfs mount is common); `/dev/shm` holds decoded frames and should not be mapped. The clips and recordings structure is not meant to be browsed or edited. Snap-packaged Docker cannot use storage outside the home folder.

Ports: `8971` authenticated UI and API without TLS (reverse proxies should use this), `5000` internal unauthenticated UI and API (limit access), `8554` RTSP restream (unauthenticated by default), `8555` WebRTC for cameras with two-way talk.

Shared memory: Docker's default `shm-size` is 64 MB. Frigate needs roughly 210 MB for two cameras detecting at 720p. A "Bus error" exit means the value is too small; raise it with `--shm-size` or `shm_size`.

For some hardware (for example Rockchip, MemryX, Synaptics) the docs advise running privileged during configuration and then granting only the required devices.

## Checked

2026-11-04. Confirmed against the Installation page: Docker host and Home Assistant App wording, MQTT broker requirement, storage paths, ports 8971, 5000, 8554 and 8555, tmpfs cache, Snap Docker limit, 64 MB default shm-size, 210 MB for two 720p cameras and the Bus error symptom. Fixed the VM claim (the page says not recommended) and the privileged-mode example (the Hailo section needs only a device mapping).
Method: documentation only; no commands were run.

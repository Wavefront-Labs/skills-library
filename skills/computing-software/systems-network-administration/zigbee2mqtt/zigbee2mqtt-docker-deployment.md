---
id: computing-software.systems-network-administration.zigbee2mqtt.zigbee2mqtt-docker-deployment
name: zigbee2mqtt-docker-deployment
category: computing-software
field: systems-network-administration
product: zigbee2mqtt
tags: [zigbee2mqtt, docker, docker-compose, podman, rootless, ghcr, udev, dialout, container]
level: practitioner
status: docs-checked
description: "Run Zigbee2MQTT in Docker or Compose: device mapping by serial by-id, data volume, udev mount, rootless user and group-add, Podman, SELinux and update steps."
sources: ["https://www.zigbee2mqtt.io/guide/installation/02_docker.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zigbee2MQTT in Docker

Image: `ghcr.io/koenkk/zigbee2mqtt` (tags `latest`, `latest-dev`, or a version like `2.0.0`, `2.0`, `2`). Architectures: linux/386, amd64, arm/v6, arm/v7, arm64 and riscv64.

```yaml
services:
    zigbee2mqtt:
        container_name: zigbee2mqtt
        image: ghcr.io/koenkk/zigbee2mqtt
        restart: unless-stopped
        volumes:
            - ./data:/app/data
            - /run/udev:/run/udev:ro
        ports:
            - 8080:8080
        environment:
            - TZ=Europe/Berlin
        devices:
            - /dev/serial/by-id/usb-Texas_Instruments_TI_CC2531_USB_CDC___0X00124B0018ED3DDF-if00:/dev/ttyACM0
```

- Map the adapter with the host `/dev/serial/by-id/...` path (stable) to a container path.
- `/run/udev:/run/udev:ro` is needed for adapter auto-detection.
- `./data:/app/data` holds `configuration.yaml` and state; first start launches onboarding on port 8080.
- If the broker is on the host, the `docker0` bridge IP works: `server: mqtt://172.17.0.1`.

Rootless: find the device group (`ls -l /dev/ttyACM0`, often `dialout`) and your uid/gid (`id`), then `--user 1001:1001 --group-add dialout` or in Compose `group_add: [dialout]` and `user: 1000:1000`. Podman (above 3.2): `--group-add keep-groups`. With SELinux append `:z` to the data volume.

Update: `docker compose pull zigbee2mqtt && docker compose up -d zigbee2mqtt` (plain Docker: pull, `docker rm -f`, rerun). A Raspberry Pi 1 or Zero needs `docker pull ghcr.io/koenkk/zigbee2mqtt --platform linux/arm/v6` first because of a Docker architecture-selection bug.

## Checked

2026-11-03. Confirmed against the Docker installation page: image and tags, architectures, compose file, device mapping, udev mount, TZ, docker0 tip, rootless Docker and Compose options, Podman keep-groups, SELinux :z, update commands, Raspberry Pi 1/Zero arm/v6 note. Removed: the 32-bit end-of-life and arm/v6 2.7.1 claims, which are not on the page.
Method: documentation only; no commands were run.

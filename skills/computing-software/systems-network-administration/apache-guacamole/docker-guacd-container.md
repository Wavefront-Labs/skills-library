---
id: computing-software.systems-network-administration.apache-guacamole.docker-guacd-container
name: docker-guacd-container
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, docker, guacd, guacamole-guacd-image, docker-network, log-level, container]
level: practitioner
status: draft
description: "Run the guacamole/guacd image on a private Docker network or exposed on 4822, set LOG_LEVEL, and avoid exposing the unauthenticated daemon."
sources:
  - https://guacamole.apache.org/doc/gug/guacamole-docker.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# guacamole/guacd container

`guacamole/guacd` runs guacd on port 4822 with VNC, RDP, SSH, telnet and Kubernetes support.

Recommended: private network, no published port.
```
docker run --network=some-network --name some-guacd -d guacamole/guacd
```
Debug logging (`LOG_LEVEL` default `info`):
```
docker run --network=some-network --name some-guacd -e LOG_LEVEL=debug -d guacamole/guacd
```
Only if something outside Docker must reach it:
```
docker run --name some-guacd -d -p 4822:4822 guacamole/guacd
```

Warning from the manual: guacd performs no authentication. Anyone who can reach port 4822 can use it to connect to other systems, so keep it off untrusted networks.

Pair it with the web app container via `GUACD_HOSTNAME=some-guacd` (see apache-guacamole.docker-guacamole-webapp).

Check logs with `docker logs some-guacd`.

Verify: from the web app container, guacd's name resolves and a test connection opens.

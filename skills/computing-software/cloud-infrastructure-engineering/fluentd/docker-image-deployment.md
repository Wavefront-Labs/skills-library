---
id: computing-software.cloud-infrastructure-engineering.fluentd.docker-image-deployment
name: docker-image-deployment
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, docker, container, fluent-fluentd, edge-debian, jemalloc]
level: practitioner
status: docs-checked
description: "Run the official fluent/fluentd Docker image: Debian vs Alpine tags, mounting a config at /fluentd/etc, and a test with the http input."
sources:
  - https://docs.fluentd.org/container-deployment/install-by-docker
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd Docker image
Image: `fluent/fluentd` (maintained by Treasure Data). `docker pull fluent/fluentd:edge-debian` gets the latest Fluentd on Debian. Debian is officially recommended because of `jemalloc` support; Alpine is smaller; a Windows Server version also exists.

Test config mounted at `/fluentd/etc` (http input to stdout):
```
<source>
  @type http
  port 9880
  bind 0.0.0.0
</source>
<match **>
  @type stdout
</match>
```
```
docker run -p 9880:9880 -v $(pwd)/tmp:/fluentd/etc fluent/fluentd:edge-debian -c /fluentd/etc/fluentd.conf
curl -X POST -d "json={\"json\":\"message\"}" http://127.0.0.1:9880/sample.test
docker logs <container-id> | tail -n 1
```
The log line shows `sample.test: {"json":"message"}`. On Windows use cmd.exe for the curl command, since PowerShell needs different JSON escaping. The example run output shows the container starting Fluentd with `--plugin /fluentd/plugins`. Related: `docker-compose-efk-stack`.

## Checked

2026-11-04. Confirmed against the Fluentd Docker Image page (docs.fluentd.org/container-deployment/install-by-docker): image name, edge-debian tag, Debian/jemalloc/Alpine/Windows note, test config, docker run and curl commands, cmd.exe note, /fluentd/plugins in the sample log. Removed: the default config path and FLUENT_CONF claim and the plugin-image build advice (not on this page).

Method: documentation only; no commands were run.

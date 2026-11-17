---
id: computing-software.devops-ci-cd.gitlab-runner.runner-behind-proxy
name: runner-behind-proxy
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [proxy, http-proxy, https-proxy, cntlm, systemd-drop-in]
level: practitioner
status: docs-checked
description: "Run the runner and Docker daemon behind an HTTP proxy."
sources: ["https://docs.gitlab.com/runner/configuration/proxy/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Running behind a proxy

The guide targets the Docker executor and covers three places the proxy must be set.

1. cntlm (optional, for an authenticating proxy): bind it to the `docker0` address (usually `172.17.0.1`) with `Listen 172.17.0.1:3128` in `/etc/cntlm.conf`. Containers can reach it but the outside world cannot, and credentials live in one place and cannot be read by the Docker runners.
2. Docker daemon: a systemd drop-in with `Environment="HTTP_PROXY=http://docker0_interface_ip:3128/"` and `HTTPS_PROXY`.
3. The runner service: create `/etc/systemd/system/gitlab-runner.service.d/http-proxy.conf` with the same variables so the runner can reach GitLab.

For registration, export `HTTP_PROXY` and `HTTPS_PROXY` and run `sudo -E gitlab-runner register`.

## Checked

2026-11-03. Confirmed against cntlm/docker0 setup and proxy steps on the Proxy page.

Method: documentation only; no commands were run.

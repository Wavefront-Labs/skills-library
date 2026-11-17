---
id: computing-software.collaboration-platform-administration.mattermost.health-check-probes
name: health-check-probes
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [health-check, system-ping, goroutine-threshold, kubernetes-probe]
level: practitioner
status: docs-checked
description: "Probe a Mattermost server with GET /system/ping and GoRoutineHealthThreshold, usable as a Kubernetes probe, or with the community Mattermost Probe."
sources: ["https://docs.mattermost.com/administration-guide/manage/configure-health-check-probes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Server health check probes

Two ways to check that a self-hosted Mattermost server is healthy. You need a running server first; highly available clusters need Mattermost Enterprise.

1. Ping the APIv4 endpoint. GET /system/ping reports whether the server is up and healthy using the GoRoutineHealthThreshold configuration setting. If the threshold is set and the number of goroutines on the server exceeds it, the server is judged unhealthy. If the threshold is not set, or the goroutine count is below it, the server is judged healthy. The endpoint can also be provided to schedulers such as Kubernetes. The docs show a Go client example: create a client with model.NewAPIv4Client pointing at your server URL, log in, then call GetPing and inspect the returned status and error.

2. Ping the server with the Mattermost Probe, a community-contributed open-source project that continually runs a variety of probes against a server. Probes can be set up to verify core features: sending and receiving messages, joining channels, pinging the login page, and searching users and channels. The project is contributed by the Mattermost open source community.

## Checked

2026-11-03. Confirmed against the Mattermost documentation page https://docs.mattermost.com/administration-guide/manage/configure-health-check-probes. Removed the unsupported liveness/readiness and threshold-tuning advice.

Method: documentation only; no commands were run.

---
id: computing-software.cybersecurity-defensive.pomerium.find-authorize-logs
name: find-authorize-logs
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [authorize-log, journalctl, kubectl-logs, log-filtering, jq]
level: intro
status: docs-checked
description: "Locate and filter Pomerium authorization service logs on a systemd daemon, Docker or Kubernetes, and pretty-print them with jq."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/audit-logs.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pomerium logs verbosely; the authorize service logs are the most useful when first configuring access.

Find logs by install type (container and deployment names depend on your configuration):
- System daemon: `sudo journalctl -u pomerium.service`
- Docker: `docker logs pomerium`
- Kubernetes: `kubectl logs -f deploy/pomerium-authorize`

Add `-f` to follow new entries.

Keep only authorize service entries by piping to `grep '"service":"authorize"'`, for example:

```
docker logs pomerium | grep '"service":"authorize"'
```

For readable output install `jq` and pipe through it:

```
kubectl logs -f deploy/pomerium-authorize | grep '"service":"authorize"' | jq
```

An entry carries `level`, `service`, `request-id`, `check-request-id`, `method`, `path`, `host`, `session-id`, `allow`, `allow-why-false`, `deny`, `deny-why-false`, `user`, `email`, `message` ("authorize check") and databroker version fields. See read-authorize-log-fields for what the allow and deny keys mean.

## Checked

2026-11-04. Confirmed against the Audit Logs page: journalctl, docker logs and kubectl logs commands, the grep filter, jq pipe, and the log entry keys. Nothing removed.

Method: documentation only; no commands were run.

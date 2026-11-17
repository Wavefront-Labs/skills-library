---
id: computing-software.devops-ci-cd.argo-events.argo-events-github-eventsource-webhook-setup
name: argo-events-github-eventsource-webhook-setup
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, github-eventsource, webhook, personal-access-token, repo-hook, ingress, secret]
level: practitioner
status: docs-checked
description: "Set up the GitHub EventSource that registers repository webhooks itself, with a token Secret, an Ingress or Route and a Sensor."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/eventsources/setup/github.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events github eventsource webhook setup

The GitHub EventSource programmatically configures webhooks for projects on GitHub. Event data is `body` (the GitHub event) and `headers`.

Steps:
1. Create a GitHub API token with the `repo_hook` permission.
2. Base64-encode it (`echo -n <token> | base64`) and create a Secret `github-access` with keys `token` and, if you use one, `secret` (webhook secret), both base64-encoded:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: github-access
type: Opaque
data:
  token: <base64-token>
  secret: <base64-webhook-secret>
```

3. Apply the Secret in `argo-events`.
4. The EventSource creates a pod and a Service named `<event-source-name>-eventsource-svc`. Create an Ingress or OpenShift Route so GitHub can reach it, and put that public address in the `url` field of the EventSource (example: `examples/event-sources/github.yaml`).
5. Apply the EventSource, then check Settings, Webhooks in the repo or the EventSource pod logs for the registration.
6. Apply `examples/sensors/github.yaml`, push a commit, and find the workflow with `argo list`.

A full pull-request walkthrough exists as tutorial 08.

## Checked

2026-11-04. Confirmed against the GitHub EventSource page: event data (`body`, `headers`), the `repo_hook` permission, base64 encoding, the `github-access` Secret keys, the `<event-source-name>-eventsource-svc` Service, the Ingress or OpenShift Route requirement, the `url` field, verification in the repo's Webhooks settings or pod logs, the sensor example, `argo list` and the tutorial 08 pointer. Nothing removed.
Method: documentation only; no commands were run.

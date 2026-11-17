---
id: computing-software.cloud-infrastructure-engineering.docker.registry-notifications-and-webhooks
name: registry-notifications-and-webhooks
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, registry, private-registry, registry-notifications, registry-webhooks, harbor-webhooks, event-driven-deploy]
level: advanced
description: "Emit push and pull events from distribution registry notifications endpoints, or Harbor/Hub webhooks, to trigger scans, deploys and audit logs reliably."
sources: ["https://distribution.github.io/distribution/about/notifications/", "https://goharbor.io/docs/main/working-with-projects/project-configuration/configure-webhooks/", "https://docs.docker.com/docker-hub/repos/manage/webhooks/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Registry notifications and webhooks

## distribution (registry:2) endpoints
```yaml
notifications:
  events:
    includereferences: true
  endpoints:
    - name: deployer
      url: https://hooks.example.com/registry
      headers:
        Authorization: [Bearer <token>]
      timeout: 1s
      threshold: 5
      backoff: 10s
      ignoredmediatypes: [application/octet-stream]
      ignore:
        actions: [pull]          # only pushes/deletes
```
Payload: `{"events":[{"action":"push","target":{"mediaType":...,"digest":"sha256:...","repository":"team/api","tag":"1.4.0","url":...},"request":{...},"actor":{"name":"ci"}}]}`.
Media type `application/vnd.docker.distribution.events.v2+json`. The registry may group unrelated
events into one envelope, so the receiver must handle several per request.

## Reliability
- Queues are **in memory**: if an instance is lost, messages may be dropped, so endpoints should be
  reasonably reliable. Treat webhooks as hints and reconcile (list tags) periodically.
- Layer pushes and pulls also generate events; use `ignoredmediatypes` or `ignore.mediatypes` /
  `ignore.actions` to drop what you do not need.
- Monitor endpoint queue size ("Pending") and failures through the registry's metrics; rising values
  indicate a problem.
- Each endpoint has its own queue, retry configuration and target. `threshold` and `backoff` control
  failure backoff.

## Harbor
Project -> Webhooks: events `PUSH_ARTIFACT`, `PULL_ARTIFACT`, `DELETE_ARTIFACT`,
`SCANNING_COMPLETED`, `SCANNING_STOPPED`, `SCANNING_FAILED`, `QUOTA_EXCEED`, `QUOTA_WARNING`,
`REPLICATION`, `TAG_RETENTION`. Endpoint types are `HTTP` (Default or CloudEvents payload) and `SLACK`.
Harbor runs webhooks as jobs with a configurable retry count (`webhook_job_max_retry`, 3 in the sample config).

## Docker Hub
Repository -> Webhooks: POST on push with `push_data.tag` and `repository.repo_name`.
The documentation shows a JSON body with `push_data.tag` and `repository.repo_name` and describes no signature, so treat the payload as untrusted and validate the repository name and a secret path segment you control. `callback_url` is a legacy field.

## Typical receivers
- Trigger a vulnerability scan / signature verification on push.
- GitOps: open a PR bumping the digest (Argo CD Image Updater / Flux image automation poll
  instead and are usually more robust).
- Audit trail of who pushed what (`actor.name`).

## Verify
Point an endpoint at a test receiver of your own, push an image, and inspect the envelope.

## Checked

2026-10-26. Documentation release: distribution/distribution docs/content at main (notifications and configuration pages), Harbor website docs main (configure-webhooks), docker/docs main (Docker Hub webhooks). Confirmed: notifications.endpoints keys (name, url, headers, timeout, threshold, backoff, ignoredmediatypes, ignore.mediatypes/actions, events.includereferences), events.v2+json envelope media type, in-memory queues and possible message loss, Harbor event type names and endpoint types, Harbor webhook retry setting, Docker Hub push_data.tag and repository.repo_name fields. Removed unconfirmed claims: events.v1 media type (it is v2), batching behaviour of multi-arch pushes, a metric or log keyword, and the echo-server test image.

Method: documentation only; no commands were run.

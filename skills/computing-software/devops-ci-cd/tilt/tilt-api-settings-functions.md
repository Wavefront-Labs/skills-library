---
id: computing-software.devops-ci-cd.tilt.tilt-api-settings-functions
name: tilt-api-settings-functions
category: computing-software
field: devops-ci-cd
product: tilt
tags: [api-settings-functions]
level: practitioner
status: docs-checked
description: "Tiltfile settings functions: update_settings, ci_settings, watch_settings, docker_prune_settings, default_registry, allow_k8s_contexts and more."
sources:
  - "https://docs.tilt.dev/api.html#api.update_settings"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tiltfile settings functions

Goal: configure how Tilt updates, watches, builds and reports.

- `update_settings(max_parallel_updates=3, k8s_upsert_timeout_secs=30, suppress_unused_image_warnings=None, k8s_server_side_apply="auto")`: `max_parallel_updates` must be a positive integer; the upsert timeout minimum is 1; `suppress_unused_image_warnings` takes image names or '*'; server-side apply accepts true, false or auto.
- `ci_settings(k8s_grace_period='', timeout='30m', readiness_timeout='5m')`: configures `tilt ci`. `k8s_grace_period` and `timeout` are duration strings. Readiness timeout is measured from when the resource starts and does not affect Kubernetes jobs.
- `watch_settings(ignore)`: global ignore patterns, equivalent to adding to .tiltignore; may be called multiple times. Relative patterns are evaluated relative to the current working dir.
- `default_registry(host, host_from_cluster=None, single_name="")`: renames built images to the registry by replacing `/` and `@` with `_` and prepending `host` and `/`. `default_registry('gcr.io/myorg')` turns `user-service` into `gcr.io/myorg/user-service`. `single_name` pushes to one repository and embeds the image name in the tag (for ECR).
- `allow_k8s_contexts(contexts)`: allow Tilt to run against extra context names. By default Minikube, Docker for Desktop, Microk8s, Red Hat CodeReady Containers, Kind, K3D and Krucible are allowed. To disable the check: `allow_k8s_contexts(k8s_context())`.
- `docker_prune_settings(disable=False, max_age_mins=360, num_builds=0, interval_hrs=1, keep_recent=2)`: configures the background Docker pruner. It prunes stopped containers, images and dangling build caches at least `max_age_mins` old, keeping the `keep_recent` most recent images per name. It runs every `num_builds` builds if set, else every `interval_hrs` hours.
- `analytics_settings(enable)`: overrides telemetry. By default Tilt does not send telemetry.
- `version_settings(check_updates=True, constraint="")`: GitHub update check; `constraint` such as `<0.17.0` or `>=0.13.2` errors if the running version does not match.
- `secret_settings(disable_scrub=False)`: by default Tilt scrubs Kubernetes Secret text from logs; True turns this off.
- `disable_snapshots()`: disables and hides the snapshots feature; provides no real security.
- `enable_feature(feature_name)`: enables non-default features; only use it when directed to.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/api.html#api.update_settings (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). Narrowed "values are duration strings" to the two parameters the page says are duration strings.

Method: documentation only; no commands were run.

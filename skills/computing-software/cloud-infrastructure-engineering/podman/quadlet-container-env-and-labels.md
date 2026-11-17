---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-container-env-and-labels
name: quadlet-container-env-and-labels
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet, environment, environmentfile, label, annotation, logdriver, podmanargs, globalargs]
level: practitioner
status: docs-checked
description: "Pass configuration into Quadlet containers with Environment, EnvironmentFile, Label, Annotation, LogDriver, LogOpt, GlobalArgs and the PodmanArgs escape hatch."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: set env, metadata and logging, and reach options Quadlet lacks.

From the table: `Environment=foo=bar` is `--env foo=bar`; `EnvironmentFile=/tmp/env` is `--env-file`; `EnvironmentHost=true` is `--env-host`; `Label="XYZ"` is `--label`; `Annotation="XYZ"` is `--annotation`; `HttpProxy=true` is `--http-proxy=true`; `LogDriver=journald` is `--log-driver journald`; `LogOpt=path=/var/log/mykube.json` is `--log-opt`. For relative `EnvironmentFile` paths that begin with a systemd specifier use `./`.

`ContainersConfModule=` maps to `--module` and `GlobalArgs=` passes global Podman options such as `--log-level=debug`.

`PodmanArgs=` passes arguments directly to the end of the `podman run` command, right before the image name, for features the generator does not support. The page says that because the generator cannot know what unexpected interactions follow, using it is not recommended. Format: space separated, with individual arguments escapable to include whitespace; repeatable.

`Pull=` sets the pull policy (`--pull`), with `Retry=` and `RetryDelay=` for retrying image pulls after HTTP errors.


Example values: `Environment=foo=bar`, `EnvironmentFile=/tmp/env`, `Label="XYZ"`, `Annotation="XYZ"`, `LogOpt=path=/var/log/mykube.json`, and `GlobalArgs=--log-level=debug`.

`EnvironmentHost=true` copies the host environment into the container as `--env-host` does, and `HttpProxy=true` maps to `--http-proxy=true`, which forwards proxy settings from the host.

## Checked

2026-11-03. Read against the official page text (podman-systemd.unit.5); every key, value, default, path and example left in this skill was confirmed there. Nothing removed.
Method: documentation only; no commands were run.

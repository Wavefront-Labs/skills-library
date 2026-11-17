---
id: computing-software.cloud-infrastructure-engineering.keda.authentication-via-scaledobject-metadata
name: authentication-via-scaledobject-metadata
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [authentication, secret-reference, envfrom, envsourcecontainername, scaledobject-metadata]
level: practitioner
status: docs-checked
description: "Authenticate a KEDA trigger by referencing a secret that the target container already consumes, and know the three limits that push you to TriggerAuthentication."
sources:
  - https://keda.sh/docs/2.17/concepts/authentication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
KEDA offers three authentication patterns: per-ScaledObject configuration, a namespaced `TriggerAuthentication`, and a global `ClusterTriggerAuthentication`.

Some trigger parameters cannot take a literal value and must reference a secret, config map or environment variable defined on the target container. The page's RabbitMQ example: the `host` parameter may embed a password, so you store the AMQP URL in a Secret, expose it to the Deployment with `envFrom: - secretRef: name: {secret-name}`, then set the trigger metadata `host: {secret-key-name}`, the key name, not the value. KEDA resolves it from the container environment.

Creation order matters: create the Secret before the Deployment that references it, and the ScaledObject after both, otherwise the references are invalid.

With several containers, set `scaleTargetRef.envSourceContainerName`; without it KEDA reads the first container and resolves secrets, config maps and environment variables from there.

The documented downsides:
- auth configuration is hard to share across ScaledObjects;
- you cannot reference a secret directly, only secrets the container itself references;
- flows such as pod identity, where no secret or connection string exists, are unsupported.

Those gaps are why `TriggerAuthentication` exists.

## Checked

2026-11-03. Confirmed in the 2.17 Authentication page source (keda-docs repository): creation-order tip, envSourceContainerName, the three downsides. Removed: the claim that the per-ScaledObject pattern is the simplest.

Method: documentation only; no commands were run.

---
id: computing-software.ai-ml-engineering.seldon-core-2.serverconfig-resource
name: serverconfig-resource
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, serverconfig, crd, mlserver, triton, open-inference-protocol, agent, rclone]
level: advanced
status: docs-checked
description: "ServerConfig defines how a Seldon Core 2 inference server pod is built: the default MLServer and Triton configs, the Agent reverse proxy and Rclone sidecar."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/kubernetes/resources/serverconfig.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ServerConfig resource

A ServerConfig defines how an inference server is created. It is an advanced resource, needed only when you want new types of inference servers.

## What it contains
- The definition of the Kubernetes ReplicaSet for the server.
- The Seldon Agent reverse proxy container that sits in front of the server.
- An Rclone server used to download model artifacts for the server.

Two ServerConfigs are provided by default: one for Seldon MLServer and one for NVIDIA Triton Inference Server. The MLServer source is `operator/config/serverconfigs/mlserver.yaml` in the repository.

## Requirement for new servers
Every inference server must support the Open Inference Protocol. Both the shipped servers do.

## How it is used
A Server resource names a ServerConfig in `spec.serverConfig` and can add `extraCapabilities`, override `capabilities`, override the agent or rclone image, or patch the `podSpec`.

When a ServerConfig changes, Servers that reference it are normally updated. With `disableAutoUpdate: true` the Server is not updated immediately when its ServerConfig changes; explicit changes to the Server itself still force a reconcile.

If you only need a different image or a mounted volume, a Server with `podSpec` overrides is enough (the Server page shows both). Create your own ServerConfig for more complex cases or when you want the Server definition standardised in one place.

## Checked
2026-11-09. Confirmed against docs-gb/kubernetes/resources/serverconfig.md and server.md (Seldon Core v2 branch): ServerConfig is advanced usage for new types of inference server; the two defaults (MLServer, NVIDIA Triton); the Open Inference Protocol requirement; the ReplicaSet with Agent reverse proxy and Rclone server; the MLServer file path `operator/config/serverconfigs/mlserver.yaml`; the Server fields (`serverConfig`, `extraCapabilities`, `capabilities`, `imageOverrides`, `podSpec`) and `disableAutoUpdate` semantics. Removed: the advice to hold production Servers on the old definition (not stated in the docs), and the claim that Servers are updated on change as a default guarantee, now worded from the `disableAutoUpdate` comment.
Method: documentation only; no commands were run.

---
id: computing-software.ai-ml-engineering.seldon-core-2.architecture-control-and-data-plane
name: architecture-control-and-data-plane
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, architecture, control-plane, data-plane, scheduler, agent, envoy, controller]
level: practitioner
status: docs-checked
description: "Seldon Core 2 microservice layout: Scheduler, Agent and Controller on the control plane; Envoy, pipeline gateway, model gateway and dataflow engine on the data plane."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/architecture/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Seldon Core 2 architecture: control plane and data plane

Seldon Core 2 is a set of small services that talk gRPC internally and scale independently. They split into two planes.

## Control plane
- **Scheduler**: loads and unloads Models, Pipelines and Experiments on the right services and matches Models to Servers so infrastructure use is optimised. Only one Scheduler instance is allowed, because its state is persisted on disk.
- **Agent**: runs next to each inference server, loads and unloads models on it, and acts as a reverse proxy over REST/gRPC. Because traffic passes through it, it collects the stats and metrics used for observability and scaling.
- **Controller**: the Kubernetes operator (Controller Manager) that reconciles CRDs with the Scheduler. Only one instance is supported. Every service except the Controller is Kubernetes agnostic and can run on Docker Compose.

## Data plane
- **Envoy**: the single ingress for inference traffic. It routes to the relevant MLServer or Triton pods and load balances replicas with weighted least-request.
- **Pipeline Gateway**: turns synchronous REST/gRPC calls to a Pipeline into Kafka messages on the pipeline input topic and reads the output topic to answer.
- **Model Gateway**: moves data between Kafka and model servers.
- **Dataflow Engine**: chains and joins models inside pipelines using Kafka Streams.

## Resilience
Control and data planes are separate, so an outage of control plane services such as the Scheduler does not stop inference from being served, and Core 2 can be provisioned to be highly available on the data plane path.

## Checked
Method: docs-checked 2026-11-09 against docs-gb/architecture/README.md (read in full). Dropped an unsupported claim that Kafka is only needed for Pipelines.

---
id: computing-software.devops-ci-cd.concourse-ci.architecture-atc-tsa-workers
name: architecture-atc-tsa-workers
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [architecture, atc, tsa, worker, garden, baggageclaim, postgresql]
level: intro
status: docs-checked
description: "Map Concourse's components: web node (ATC plus TSA), PostgreSQL, and workers running Garden and Baggageclaim, with default ports and what each part is responsible for."
sources:
  - https://concourse-ci.org/docs/internals/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Concourse is a distributed system of three parts: web nodes, PostgreSQL, and workers.

**ATC** runs the web UI and API and does all pipeline scheduling. It stores pipeline data, including build logs, in PostgreSQL. Several ATCs can form one cluster as long as they point at the same database; they synchronise with basic locking and roughly spread work. It listens on port `8080` by default and usually sits behind a load balancer. For `fly intercept` to work, the load balancer must do TCP or SSL forwarding, not HTTP or HTTPS. Inside the ATC are four components: the checker (looks for new resource versions), the scheduler (decides which job builds to create), the build tracker (runs scheduled builds) and the garbage collector (removes unused containers and volumes). Since v5.7.0 every component appears in the `components` database table, where its interval can be edited or the component paused.

**TSA** is a custom SSH server, default port `2222`, usually co-located with the ATC. Workers use it to register. Its `forward-worker` command reverse-tunnels the worker's addresses so workers in arbitrary networks can join without being exposed.

**Workers** run Garden (default port `7777`) and Baggageclaim (default port `7788`) servers, and both connections are forwarded over the SSH link to the TSA. Everything runs in containers, so the host holds no important state. Windows and Darwin workers run the same servers but use houdini to fake containers; Windows containers are not supported and Darwin has no native container technology.

## Checked

2026-11-04. All claims confirmed on the Internals page, sections Basic architecture, ATC, TSA and Workers Architecture.

Method: documentation only; no commands were run.

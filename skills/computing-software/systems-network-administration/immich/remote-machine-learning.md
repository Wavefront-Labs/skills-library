---
id: computing-software.systems-network-administration.immich.remote-machine-learning
name: remote-machine-learning
category: computing-software
field: systems-network-administration
product: immich
tags: [remote-ml, port-3003, load-balancing, machine-learning, urls]
level: practitioner
status: docs-checked
description: "Host Immich's machine learning container on a stronger machine, add its URL in settings, understand failover, and place a load balancer in front."
sources:
  - https://docs.immich.app/guides/remote-machine-learning
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: offload Smart Search and Face Detection to a more powerful host, useful for low-memory systems such as a Raspberry Pi.

Facial Recognition does not use the remote service because it works from outputs already saved in the database.

Security: image previews are sent to the remote container, and as an internal service it has no security of its own. Be careful on public computers or paid cloud processors.

On the remote server (Docker installed), use a compose file:

```yaml
name: immich_remote_ml
services:
  immich-machine-learning:
    container_name: immich_machine_learning
    image: ghcr.io/immich-app/immich-machine-learning:${IMMICH_VERSION:-release}
    volumes:
      - model-cache:/cache
    restart: always
    ports:
      - 3003:3003
volumes:
  model-cache:
```

Add one of `-armnn`, `-cuda`, `-rocm`, `-openvino`, `-rknn` to the image tag for acceleration, together with `hwaccel.ml.yml`. Start with `docker compose up -d`.

Then in Machine Learning Settings click Add URL and enter `http://ip:port`.

Keep both hosts on the same Immich version, because mismatches cause bugs.

Adding a URL is preferred to replacing the default `http://immich-machine-learning:3003`: if the remote is down, jobs fall back to the local container. Replacing it means Smart Search and Face Detection jobs fail when the remote is unavailable, which also stalls Duplicate Detection and Facial Recognition.

Several URLs are tried in order, not balanced. For load balancing, put a dedicated load balancer in front and use its URL. One ML container can serve several Immich instances, but mixed models raise peak memory.

## Checked

2026-11-09. Confirmed against the Immich docs (https://docs.immich.app/) by reading guides/remote-machine-learning in full: scope, security warning, compose file, setup steps, forcing remote processing, load balancing.
Removed: nothing.
Method: documentation only; no commands were run.

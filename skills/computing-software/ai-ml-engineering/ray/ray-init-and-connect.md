---
id: computing-software.ai-ml-engineering.ray.ray-init-and-connect
name: ray-init-and-connect
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, ray-init, ray-address, ray-client, cluster-connect]
level: practitioner
status: docs-checked
description: "Start or connect to Ray with ray.init: local instance, address auto, RAY_ADDRESS, ray:// Ray Client, namespaces, resource limits and ray start."
sources:
  - https://docs.ray.io/en/latest/ray-core/starting-ray.html
  - https://docs.ray.io/en/latest/ray-core/api/doc/ray.init.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ray.init and cluster connect

```python
import ray
ray.init()                                   # local: starts head node processes on this machine
ray.init(num_cpus=4, num_gpus=1, object_store_memory=2*10**9)   # cap resources
ray.init(address="auto")                     # connect to an existing instance; RAY_ADDRESS is checked first
ray.init(address="ray://head-host:10001")    # Ray Client (needs pip install "ray[client]"; port 10001 by default)
ray.init(namespace="prod", ignore_reinit_error=True, logging_level="INFO")
print(ray.cluster_resources(), ray.available_resources())
ray.shutdown()
```
CLI cluster:
```bash
ray start --head --port=6379 --dashboard-host=0.0.0.0
ray start --address=HEAD_IP:6379        # on workers
ray status                              # cluster status
ray stop
```

## Gotchas
- Calling `ray.init()` twice raises `RuntimeError` unless `ignore_reinit_error=True` (or you call `ray.shutdown()` first); in library code check `ray.is_initialized()`.
- Since Ray 1.5, Ray calls `ray.init()` automatically the first time you use a remote API, with defaults you did not choose; init explicitly.
- `ray.init()` with no address checks the `address` argument, then (for no address or `"auto"`) `RAY_ADDRESS`, then the latest Ray instance that `ray start` started on the same machine.
- If you connected to an existing cluster, `ray.shutdown()` only disconnects; it does not stop the cluster.
- Ray Client has architectural limitations (it may not work well with Ray Tune or Ray Train) and ends the workload if the connection is lost for more than 30 seconds; the docs recommend the Ray Jobs API for long-running work.
- Anyone with Ray Client access can run arbitrary code on the cluster; never expose it to `0.0.0.0/0`.
- `local_mode` is no longer supported.
- Multi-node clusters are supported only on Linux; Windows and macOS need `RAY_ENABLE_WINDOWS_OR_OSX_CLUSTER=1` at your own risk.

## Verify
`ray.cluster_resources()` shows the expected CPU/GPU totals.

## Checked
2026-11-03: checked against the Ray docs source `core/starting-ray.md`, `cluster/running-applications/job-submission/ray-client.md`, `cluster/getting-started.md` and the `ray.init` docstring and code in `python/ray/_private/worker.py`. Removed the unsourced Ray Client data-transfer claim, `local_mode` tag and the "confirm" markers; added the Linux-only multi-node note.
Method: documentation only; no commands were run.

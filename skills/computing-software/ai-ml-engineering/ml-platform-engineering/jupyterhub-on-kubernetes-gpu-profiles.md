---
id: computing-software.ai-ml-engineering.ml-platform-engineering.jupyterhub-on-kubernetes-gpu-profiles
name: jupyterhub-on-kubernetes-gpu-profiles
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform, self-service, jupyterhub, zero-to-jupyterhub, kubespawner, gpu-profiles, idle-culling]
level: practitioner
status: docs-checked
description: "Run JupyterHub on Kubernetes for ML teams with Zero to JupyterHub: CPU/GPU profile lists via KubeSpawner overrides, per-user profile choices, idle culling and image pre-pulling."
sources:
  - https://z2jh.jupyter.org/en/stable/
  - https://z2jh.jupyter.org/en/stable/jupyterhub/customizing/user-environment.html
  - https://jupyterhub-kubespawner.readthedocs.io/en/latest/spawner.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JupyterHub on Kubernetes with GPU profiles

Zero to JupyterHub (Helm chart) runs JupyterHub on Kubernetes. Pin the chart version and read the changelog before upgrades.

## Profiles
Profiles live under `singleuser.profileList`: a list of profiles, each with `display_name`, `description`, optional `default: true` (one profile only) and `kubespawner_override`. Options in `kubespawner_override` overwrite the defaults for that profile and must use KubeSpawner names in snake_case (for example `lifecycle_hooks`, not `lifecycleHooks`).

```yaml
singleuser:
  image: {name: registry.example.com/ml-notebook, tag: "<tag>"}
  profileList:
    - display_name: "CPU"
      default: true
    - display_name: "1 GPU"
      kubespawner_override:
        extra_resource_limits: {nvidia.com/gpu: "1"}
        node_selector: {<label>: <value>}
        tolerations: [{key: nvidia.com/gpu, operator: Exists, effect: NoSchedule}]
        image: registry.example.com/ml-notebook-cuda:<tag>
```
`extra_resource_limits`, `node_selector`, `tolerations`, `cpu_guarantee`, `mem_guarantee` and `storage_capacity` are all KubeSpawner options (see the KubeSpawner `spawner` reference). Keep client secrets out of git.

## GPU specifics
- GPU nodes need the NVIDIA device plugin / GPU Operator; taint them so CPU notebooks never land there.
- Culling stops servers that are inactive; the default culler is configured for one hour of inactivity. An idle GPU notebook overnight is the biggest waste on most ML platforms, so consider a shorter timeout for GPU users.
- To show different profiles per user, define a custom pre-spawn hook that populates the profile list from user identity (the docs link examples). KubeSpawner `profile_list` also accepts a callable.
- Use ResourceQuotas or Kueue for fairness.

## Images
- Pin image tags. With `prePuller.hook.enabled`, all nodes pull the image before the hub is upgraded; pulling may take several minutes for large images.
- Per-user PVCs for home; shared datasets via read-only mounts or object storage, not copied into homes.

## Verify
- [ ] User picks the GPU profile and `nvidia-smi` works in the notebook.
- [ ] Idle server is culled after the timeout and the GPU node scales down.
- [ ] Users outside the GPU group do not see the GPU profile.

## Checked
2026-11-01. Confirmed on the Zero to JupyterHub "user environment" page and the KubeSpawner reference: `singleuser.profileList`, `display_name`, `description`, `default`, `kubespawner_override`, snake_case rule, culling default of one hour of inactivity, `prePuller.hook.enabled`, user-dependent profiles via a pre-spawn hook, and the KubeSpawner options `extra_resource_limits`, `node_selector`, `tolerations`, `cpu_guarantee`, `mem_guarantee`, `storage_capacity`, `profile_list` (callable). Removed (not on the pages): Helm install flags, OAuth authenticator keys, `cull.timeout`/`every` values, `scheduling.userScheduler`, `quay.io/jupyter` stacks, time-slicing/MIG advice.
Method: documentation only; no commands were run.

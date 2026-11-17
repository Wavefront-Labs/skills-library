---
id: computing-software.devops-ci-cd.tilt.tilt-tutorial-up
name: tilt-tutorial-up
category: computing-software
field: devops-ci-cd
product: tilt
tags: [tutorial-up, tilt, tilt-up, control-loop]
level: intro
status: docs-checked
description: "First tilt up with the Tilt Avatars sample: what the Tiltfile does, how resources and their update and runtime status work, and the control loop."
sources:
  - "https://docs.tilt.dev/tutorial/2-tilt-up.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tutorial: tilt up

Goal: launch a Tilt project and understand Tiltfile, resources and the control loop.

## Launch

`tilt up` starts the Tilt control loop and looks for a file named `Tiltfile` in the current directory. For the tutorial, `tilt demo`:

1. creates a temporary local Kubernetes cluster in Docker,
2. clones the Tilt Avatars sample project (Python API backend plus JavaScript SPA frontend),
3. launches a `tilt up` session against that cluster,
4. cleans up on exit.

Press Spacebar in the terminal to open the Tilt UI. With your own cluster instead:

```bash
git clone https://github.com/tilt-dev/tilt-avatars.git
cd tilt-avatars/
tilt up
```

Run `tilt down` from that directory afterwards to clean up.

## Tiltfile

Written in Starlark. When executed: built-ins such as `k8s_yaml` and `docker_build` register information; Tilt assembles resources to build and deploy; Tilt watches relevant source files to trigger updates. The Tiltfile is itself a resource, so edits take effect without restarting Tilt.

## Resources

A resource is a bundle of work, for example an image build plus Kubernetes YAML, or a locally executed command. Bundling is automatic in most cases; use `k8s_resource` to configure more.

- Update status: Tilt may compile locally, build an image, or apply a modified K8s object or Helm chart. Tilt knows which files correspond to a resource and update action, so it will not rebuild a container just because a Pod label changed. Already running, unchanged services are not redeployed on `tilt up`.
- Runtime status: what happens to the code after deploy, and why it failed.

## Control loop

Tilt watches and reacts continuously:

- source change: sync to running container
- dependency change (`package.json`): sync, then run a command such as `npm install`
- build spec change (`Dockerfile`): rebuild and redeploy
- deployment spec change: reconcile (for example `kubectl apply -f ...`)
- `Tiltfile` change: re-evaluate, creating, modifying or deleting resources

## Checked

2026-11-07. Pages read from the tilt-dev/tilt.build source of docs.tilt.dev. Read tutorial step 2 (Launching and Managing Resources) in full. Confirmed the four `tilt demo` steps, the Tilt Avatars description, the clone-and-`tilt up` alternative with `tilt down`, the Tiltfile execution steps, the Tiltfile-as-a-resource claim, update and runtime status and the five control-loop examples. Not opened: the tilt-avatars repository. Reworded: "only rebuilds what a changed file relates to" to the page's Pod-label example. 

Method: documentation only; no commands were run.

---
id: computing-software.devops-ci-cd.tilt.tilt-faq
name: tilt-faq
category: computing-software
field: devops-ci-cd
product: tilt
tags: [faq, tilt, troubleshooting, tilt-doctor]
level: intro
status: docs-checked
description: "Answers to common Tilt questions: error messages, choosing a cluster, Docker host variables, BuildKit, and dynamic Tiltfile configuration."
sources:
  - "https://docs.tilt.dev/faq.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tilt FAQ

## Error messages

- `tilt version` prints "template engine not found for: version": you are running the Ruby template project also called Tilt. Delete it, use an absolute path, or rename Tilt to `tlt` (it is a static binary).
- "WARNING: Image not used in any deploy config": the Tiltfile has build instructions (`docker_build`) but no run instructions (`k8s_yaml`), like an unused variable. Check for missing YAML or a misspelled image name.
- Push error "unauthorized: You don't have the needed permissions": Tilt thinks you deploy to a remote cluster; check the cluster configuration.
- "Unable to connect to cluster": restart the cluster, or reset its state. Docker for Mac: Preferences, Kubernetes tab to disable/enable, Reset tab to reset. Minikube: `minikube stop` then `minikube start`; `minikube delete` resets.

## Which cluster

Tilt uses the default `kubectl` cluster.

```bash
kubectl config current-context
kubectl config get-contexts
kubectl config use-context docker-desktop
tilt doctor
```

`tilt doctor` prints the detected `Env` (cluster type) and Docker host. Cluster-name prefixes signal type: `docker-`, `gke_`, `kind-`, `minikube` (or `minikube-` for profiles). If detection fails, check the cluster name.

## Images and Docker

- With Docker for Mac, Minikube or MicroK8s, Tilt builds images in-cluster and sets ImageNeverPull, so Kubernetes errors if it tries to pull from a remote server.
- With Minikube or MicroK8s, Tilt connects to the Docker server inside the cluster, so the images are not in your local Docker CLI. `tilt doctor` prints the Docker host: `DOCKER_HOST=tcp://my-url/ docker images`.
- BuildKit is enabled automatically if your Docker supports it (Docker v18.06 with Experimental mode, or v18.09+). Disable with `DOCKER_BUILDKIT=0`.
- Remote Docker builds use the standard variables: `DOCKER_HOST`, `DOCKER_API_VERSION`, `DOCKER_CERT_PATH`, `DOCKER_TLS_VERIFY` (off by default), `DOCKER_DEFAULT_PLATFORM`.

## Dynamic configuration

Tiltfile built-ins: `os.environ.get('ENV_VAR', '')`, `read_file('./path/to/file')`, `read_json(...)`, `read_yaml(...)`, and `local()` for shell commands. Custom `tilt up` flags come from the config API.

## Help

Kubernetes Slack, #tilt channel (slack.k8s.io), or a GitHub issue on tilt-dev/tilt.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/faq.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). Split a conflated bullet: the page says in-cluster builds and ImageNeverPull apply to Docker for Mac, Minikube and MicroK8s, but only Minikube and MicroK8s use the cluster Docker server.

Method: documentation only; no commands were run.

---
id: computing-software.cloud-infrastructure-engineering.kubernetes.image-pull-policy-and-tag-strategy
name: image-pull-policy-and-tag-strategy
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, imagepullpolicy, always-pull, image-tags, image-digest, alwayspullimages, latest-tag]
level: practitioner
status: docs-checked
description: "Pick imagePullPolicy and tag strategy deliberately: defaulting rules, immutable tags vs digests, :latest pitfalls, AlwaysPullImages, and registry-outage impact."
sources: ["https://kubernetes.io/docs/concepts/containers/images/#image-pull-policy", "https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#alwayspullimages", "https://docs.docker.com/docker-hub/usage/pulls/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# imagePullPolicy and tag strategy

## Defaulting (set when the object is created, never updated)
If you omit `imagePullPolicy`, the cluster sets it when a Pod is submitted:
| Image reference | Default policy |
|---|---|
| no tag (and no digest) or `:latest` | `Always` |
| any other tag | `IfNotPresent` |
| digest `@sha256:...` | `IfNotPresent` |

The value is set when the object is first created and is not updated if the tag or digest
later changes: a Deployment created with `app:1.0` and later moved to `app:latest` keeps
`IfNotPresent` until you change it yourself.

## Policies
- `IfNotPresent`: pull only if the image is not already present locally. With a mutable
  tag, different nodes can run different code.
- `Always`: each time the kubelet launches a container, it asks the container runtime to
  pull; the runtime contacts the registry, resolves the tag to a digest and downloads
  only layers not cached. Efficient while the registry is reliably reachable, but it needs
  the registry (or rate limit headroom) to start containers.
- `Never`: the kubelet does not fetch; startup fails unless the image is already on the node
  (pre-pulled images).

## Recommended
- Avoid `:latest` in production: it is harder to track which version runs and to roll back.
  Use a meaningful tag such as `v1.42.0` and/or a digest.
- Pin a digest (`image@sha256:...`) so a change at the registry cannot cause a mix of old and
  new code. With both tag and digest (`name:3.5@sha256:...`) only the digest is used for pulling.
- Third-party admission controllers can rewrite Pods to use digests instead of tags.
- Multi-tenant clusters: the `AlwaysPullImages` admission controller forces the policy to
  `Always` so a pod can only use an already-pulled private image if it has the credentials to
  pull it. Cost: pulls need registry access every start.
- To force a pull: set `imagePullPolicy: Always`, or omit the policy and use `:latest` or no
  tag, or enable `AlwaysPullImages`.

## Checking what is actually running
`kubectl get pod <p> -o jsonpath='{.status.containerStatuses[*].imageID}'` shows the resolved
image ID per container; compare across pods to detect mutable-tag drift.

## Gotchas
- `kubectl rollout restart` with `IfNotPresent` and a mutable tag does not fetch a newly
  pushed image on nodes that already have the old one.
- Docker Hub limits unauthenticated pulls to 100 per 6 hours per IPv4 address or IPv6 /64
  subnet; shared NAT addresses share the allowance, so mirror upstream images or authenticate.

## Verify
- [ ] No `:latest` or untagged images in production workloads.
- [ ] All pods of a Deployment report the same `imageID`.

## Checked
Date: 2026-10-27. Documentation: Kubernetes website "Images" (pull policy, defaulting, required
image pull), "Admission Controllers" (AlwaysPullImages), and Docker Hub "Usage and limits for
pulls" (latest Kubernetes release v1.37.1). Confirmed: defaulting rules and their one-time
setting, the three policies, `:latest` guidance, digest behaviour, AlwaysPullImages purpose,
the Docker Hub unauthenticated limit. Removed unconfirmed claims (registry tag immutability
setting, Kustomize and Renovate digest management, a named Kyverno policy, the shell grep
one-liner, "outage amplifier" wording).
Method: documentation only; no commands were run.

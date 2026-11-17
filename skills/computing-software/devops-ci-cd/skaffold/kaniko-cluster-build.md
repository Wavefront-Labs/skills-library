---
id: computing-software.devops-ci-cd.skaffold.kaniko-cluster-build
name: kaniko-cluster-build
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [kaniko, cluster, in-cluster, pullsecretname]
level: advanced
status: docs-checked
description: "Build images inside the cluster with Kaniko, with the artifact and cluster options that control caching, secrets and scheduling."
sources:
  - "https://skaffold.dev/docs/builders/build-environments/in-cluster/"
  - "https://skaffold.dev/docs/builders/builder-types/docker/"
  - "https://skaffold.dev/docs/references/yaml/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Setting `build.cluster` runs builds in Kubernetes. Skaffold supports Kaniko or a custom build script in cluster. Each Kaniko artifact uses the `kaniko` builder block:

```yaml
build:
  artifacts:
  - image: my-registry/app
    kaniko:
      cache: {}
      reproducible: false
  cluster:
    namespace: build
    pullSecretName: kaniko-secret
    timeout: 20m
```

Kaniko builds directly to a registry, so it needs active cluster credentials and Kaniko must push the result.

Artifact options (`KanikoArtifact`) include `dockerfile` (default `Dockerfile`), `target`, `buildArgs`, `cache`, `cleanup`, `insecure`, `skipTLS`, `reproducible`, `singleSnapshot`, `registryMirror`, `volumeMounts`, `image` (the Kaniko executor image) and `initImage`.

Cluster options (`ClusterDetails`):

- `pullSecretName` (default `kaniko-secret`): the Kubernetes secret for pulling base images and pushing the result; it must contain the Google Cloud service account key under the key `kaniko-secret`. Alternatively `pullSecretPath` points to a service account key file. `randomPullSecret` adds a random suffix to the name for parallel builds.
- `dockerConfig` (`path` or `secretName`) for pushing to a Docker registry. The Kubernetes secret must be an opaque secret with the key `config.json`, not a `kubernetes.io/dockerconfigjson` secret.
- `namespace` (defaults to the current namespace), `serviceAccount` (default `default`), `tolerations`, `nodeSelector`, `resources`, `labels`, `annotations`, `volumes`, `runAsUser`.
- `timeout`: how long a build may run, default 20 minutes (`20m`).
- `concurrency`: default 0, meaning no limit. For in-cluster builds all artifacts build in parallel by default; set `1` to build sequentially, and lower it if the cluster is small. Logs still print in sequence.
- Context upload: `copyMaxRetries` (default 3), `copyTimeout` (default 5 minutes, `5m`) and `buildContextCompressionLevel` (default 1).

Practical advice: set a generous timeout for large images, and use a dedicated namespace and service account so build credentials stay separate from application workloads.

## Checked

2026-11-04. Read the Skaffold In cluster build page, the Docker Build page (Kaniko section) and the `KanikoArtifact` and `ClusterDetails` definitions in the v4beta14 schema. Confirmed all options, defaults, the secret key rules and the concurrency behaviour. Replaced the dead `/cluster/` source with `/in-cluster/`. Removed: the "keep `.dockerignore` tight" advice and the resource-request scheduling advice (not on the pages).
Method: documentation only; no commands were run.

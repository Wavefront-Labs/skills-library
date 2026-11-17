---
id: computing-software.software-engineering.quarkus.quarkus-kubernetes-manifest-tuning
name: quarkus-kubernetes-manifest-tuning
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, kubernetes, manifests, env-vars, deployment, openshift]
level: advanced
status: docs-checked
description: "Generate and tune Kubernetes manifests with the Quarkus Kubernetes extension: image names, idempotent output, env vars, volumes, probes, deployment targets, deploy flag."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/deploying-to-kubernetes.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus Kubernetes manifest tuning

With `quarkus-kubernetes` (plus a container-image extension such as `quarkus-container-image-jib`) each build writes `kubernetes.json` and `kubernetes.yml` in `target/kubernetes/` (a `Deployment` and a `Service`). Apply with `kubectl apply -f target/kubernetes/kubernetes.json`; the namespace is omitted by default, so use `-n=test` or set `quarkus.kubernetes.namespace`.

## Image and output

```properties
quarkus.container-image.group=quarkus
quarkus.container-image.name=demo-app
quarkus.container-image.tag=1.0
quarkus.container-image.registry=my.docker-registry.net
quarkus.kubernetes.idempotent=true
quarkus.kubernetes.output-directory=target/kubernetes-with-idempotent
```

The image becomes `my.docker-registry.net/quarkus/demo-app:1.0`. `idempotent=true` stops commit-id and build-timestamp changes that trigger Git-Ops redeploys. For registry credentials set `quarkus.container-image.username/password` and `quarkus.kubernetes.generate-image-pull-secret=true`.

## Kind, labels, replicas

`quarkus.kubernetes.deployment-kind` takes `StatefulSet`, `Job` or `CronJob` (CronJob requires `quarkus.kubernetes.cron-job.schedule`, otherwise the build fails; Picocli defaults to Job). Also `quarkus.kubernetes.replicas=3`, `quarkus.kubernetes.labels.foo=bar`, `quarkus.kubernetes.annotations."app.quarkus/id"=42`, `quarkus.kubernetes.name/version/part-of`.

## Environment and volumes

```properties
quarkus.kubernetes.env.vars.my-env-var=foobar
quarkus.kubernetes.env.secrets=my-secret
quarkus.kubernetes.env.configmaps=my-config-map
quarkus.kubernetes.env.mapping.foo.from-secret=my-secret
quarkus.kubernetes.env.mapping.foo.with-key=keyName
quarkus.kubernetes.env.fields.foo=metadata.name
quarkus.kubernetes.mounts.my-volume.path=/where/to/mount
quarkus.kubernetes.secret-volumes.my-volume.secret-name=my-secret
quarkus.kubernetes.config-map-volumes.my-volume.config-map-name=my-config-map
quarkus.kubernetes.app-config-map=<config map name>
```

`my-env-var` becomes `MY_ENV_VAR`. Conflicting definitions fail the build; duplicates only warn. `app-secret`/`app-config-map` replace the manual volume, mount and `SMALLRYE_CONFIG_LOCATIONS` environment variable steps; the generated manifests contain everything required, with volumes at `/mnt/app-secret` and `/mnt/app-config-map`.

## Probes, resources, ingress

Adding `quarkus-smallrye-health` generates readiness and liveness probes; tune with `quarkus.kubernetes.readiness-probe.initial-delay=20s`. Resources: `quarkus.kubernetes.resources.requests.memory=64Mi` (also `requests.cpu`, `limits.memory`, `limits.cpu`). Ingress: `quarkus.kubernetes.ingress.expose=true`, with `ingress.host` and `ports.http.path`.

## Targets and deploying

`quarkus.kubernetes.deployment-target=kubernetes,openshift,knative`: all are generated but only the first is applied on deploy. Setting `-Dquarkus.kubernetes.deploy=true` (off by default, ignored in tests and dev mode) builds the image and applies manifests using the `.kube/config` cluster of `kubectl`. Extensions `quarkus-minikube` and `quarkus-kind` generate dev-only manifests; do not use them in production. Extra resources in `src/main/kubernetes/<target>.yml` (or `common.yml`) are merged with generated ones by file name.

## Checked

2026-11-07. Read in full: deploying-to-kubernetes.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: the unconfirmed statement that `app-secret`/`app-config-map` themselves wire `SMALLRYE_CONFIG_LOCATIONS`; the wording now follows the page (generated manifests contain everything required).

Method: documentation only; no commands were run.

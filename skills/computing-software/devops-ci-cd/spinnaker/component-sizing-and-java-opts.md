---
id: computing-software.devops-ci-cd.spinnaker.component-sizing-and-java-opts
name: component-sizing-and-java-opts
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [sizing, kubernetes, resources, java-opts, halconfig, customsizing, service-settings]
level: advanced
status: docs-checked
description: "Set Kubernetes CPU and memory requests/limits per Spinnaker service with deploymentEnvironment.customSizing, choosing container or service names, and tune JAVA_OPTS heap."
sources:
  - https://spinnaker.io/docs/reference/halyard/component-sizing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The page is headed "Halyard is deprecated": it says Halyard is no longer supported, the page is kept for historical purposes, and documentation should move to native configuration files. Custom sizing is supported **only for distributed deployments on Kubernetes** (`hal config deploy edit --type distributed --account-name my-k8s-cluster`). Edit the `deploymentEnvironment.customSizing` section of the halconfig by hand or use the Halyard component sizing commands.

**Two key styles:**
- By **container name** (recommended), e.g. `echo:`, which sizes only that container in the `spin-echo` pod, not sidecars such as the monitoring daemon.
- By **service name**, e.g. `spin-clouddriver:`, which sizes the Clouddriver container and every sidecar in that service's pod.

```yaml
deploymentEnvironment:
  customSizing:
    echo:
      limits: {cpu: 250m, memory: 512Mi}
      requests: {cpu: 100m, memory: 128Mi}
    spin-clouddriver:
      limits: {cpu: 1000m, memory: 1Gi}
      requests: {cpu: 250m, memory: 512Mi}
```

Values follow Kubernetes conventions.

**JVM heap.** All JVM-based services default to `JAVA_OPTS=-XX:MaxRAMPercentage=50.0`, i.e. half the container memory. Override with the `env` key in service-settings. As a starting point set `-Xms` to 80-90% of the memory request and `-Xmx` to 80-90% of the limit; for the Clouddriver example above the page uses `env: JAVA_OPTS: "-Xms410m -Xmx819m"`.

**Recommendations from the page:** do not apply limits and requests to the bootstrapping pods (they can be scaled to 0 after `hal deploy apply` and relaunch on the next apply). Optimal sizes depend on the environment, but clouddriver and orca generally need to be larger than the rest, and echo may need more if using event hooks.

**Replicas:** `customSizing` accepts `spin-<component>: replicas: 2`. If unset, Halyard keeps the previous deployment's replica count, and the initial deployment defaults every pod to 1. Echo and igor must each run exactly one pod to avoid duplicate triggering.

## Checked

2026-11-04. Kubernetes-only restriction, both key styles, the example, the default JAVA_OPTS and the 80-90% starting point were confirmed on the Component Sizing page; the Recommendations and Replicas sections were confirmed on the same page.

Method: documentation only; no commands were run.

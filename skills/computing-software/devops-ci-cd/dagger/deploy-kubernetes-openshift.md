---
id: computing-software.devops-ci-cd.dagger.deploy-kubernetes-openshift
name: deploy-kubernetes-openshift
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, kubernetes, openshift, helm, daemonset, self-hosted-ci, deployment]
level: practitioner
status: docs-checked
description: "Deploy the Dagger Engine on Kubernetes or OpenShift as a Helm-installed DaemonSet and point the CLI at an engine pod with kube-pod://."
sources: [https://docs.dagger.io/0.21/reference/deployment/kubernetes, https://docs.dagger.io/0.21/reference/deployment/openshift, https://docs.dagger.io/0.21/reference/best-practices/adopting]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Deploying Dagger on Kubernetes and OpenShift

Goal: self-host engines for CI. Dagger 0.21 docs.

## Architecture guidance

Base pattern: persistent runner nodes, ephemeral CI runners, a runner controller and cert manager on support nodes, one Dagger Engine per runner node (a DaemonSet). Each CI runner only sees the cache of its local engine. Adding a node auto-scaler cuts cost but loses engine cache when nodes go away; consider persistent volumes. Recommendations: runner nodes with moderate to large NVMe drives (fast, cheap, usually ephemeral), and at least 2 vCPU and 8 GB RAM as a starting size. Tested: Helm chart on K3s (e2e), EKS at scale, SUSE RKE2 and Rancher Desktop (RKE2 recommendation: SLE Micro 6.1 with 100 GB storage per node minimum).

## Kubernetes steps

Prerequisites: cluster with a configured `kubectl`, and Helm.

```shell
helm upgrade --install --namespace=dagger --create-namespace \
    dagger oci://registry.dagger.io/dagger-helm

kubectl wait --for condition=Ready --timeout=60s pod \
    --selector=name=dagger-dagger-helm-engine --namespace=dagger

DAGGER_ENGINE_POD_NAME="$(kubectl get pod \
    --selector=name=dagger-dagger-helm-engine --namespace=dagger \
    --output=jsonpath='{.items[0].metadata.name}')"
export DAGGER_ENGINE_POD_NAME
_EXPERIMENTAL_DAGGER_RUNNER_HOST="kube-pod://$DAGGER_ENGINE_POD_NAME?namespace=dagger"
export _EXPERIMENTAL_DAGGER_RUNNER_HOST
```

Test with a `dagger query` that runs `uname -a` in `alpine` (reports the node kernel). Inspect with `kubectl describe daemonset/dagger-dagger-helm-engine --namespace=dagger`.

## OpenShift steps

Prerequisites: working cluster, Helm, `oc`. Create `values.yaml` (from the docs snippet) that sets the engine image (tag `latest` in the docs example) and uses a label-based toleration and node affinity:

```yaml
engine:
  image:
    repository: registry.dagger.io/engine
    tag: latest
  tolerations:
    - effect: NoSchedule
      key: dagger-node
      operator: Exists
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: dagger-node
            operator: Exists
```

Then for each engine node: `oc adm taint nodes NODE-NAME dagger-node=true:NoSchedule`; install: `helm upgrade --create-namespace --install --namespace dagger dagger oci://registry.dagger.io/dagger-helm -f values.yaml`; grant permissions: `oc adm policy add-scc-to-user privileged -z default -n dagger`.

## Gotchas

- Skipping the SCC step makes pod creation fail (privileged containers with fixed user IDs and host path mounts need it).
- Dagger workflows are not distributed: one `dagger call` runs on one engine.
- Runner connection formats: computing-software.devops-ci-cd.dagger.custom-runner-and-runtimes.

## Checked

2026-11-07

Read in full from the docs source: reference/deployment/kubernetes.mdx, openshift.mdx and the openshift.yaml snippet, plus reference/best-practices/adopting. Added the adopting page as a source for the "workflows are not distributed" gotcha. Reworded "pins the engine image" to "sets the engine image (tag latest in the docs example)".

Method: documentation only; no commands were run.

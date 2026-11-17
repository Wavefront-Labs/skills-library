---
id: computing-software.cloud-infrastructure-engineering.kubernetes.private-registry-auth-and-credential-providers
name: private-registry-auth-and-credential-providers
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, imagepullsecrets, credential-provider, private-registry-auth, ecr, acr, gar, kubelet-image-credential-provider, serviceaccount-imagepullsecrets]
level: practitioner
status: docs-checked
description: "Pull from private registries: imagePullSecrets on pods or ServiceAccounts, kubelet image credential provider plugins for ECR/GAR/ACR, and fixing 'pull access denied'."
sources: ["https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/", "https://kubernetes.io/docs/tasks/administer-cluster/kubelet-credential-provider/", "https://kubernetes.io/docs/concepts/containers/images/#ensureimagepullcredentialverification", "https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Private registry auth: imagePullSecrets and credential providers

## imagePullSecrets
```bash
kubectl create secret docker-registry regcred -n app \
  --docker-server=registry.example.com --docker-username=robot\$ci --docker-password="$TOKEN"
```
Attach per pod (`spec.imagePullSecrets: [{name: regcred}]`) or, better, to the ServiceAccount
so every pod using it inherits it:
```bash
kubectl patch sa default -n app -p '{"imagePullSecrets":[{"name":"regcred"}]}'
```
The secret must be in the **pod's namespace**. Copy it per namespace (External Secrets,
a namespace provisioning template, or another copy mechanism).

## Kubelet credential providers (no secrets in namespaces)
The kubelet execs a plugin to obtain short-lived registry creds for matching images.
```yaml
# /etc/kubernetes/credential-provider-config.yaml
apiVersion: kubelet.config.k8s.io/v1
kind: CredentialProviderConfig
providers:
- name: ecr-credential-provider
  matchImages: ["*.dkr.ecr.*.amazonaws.com", "*.dkr.ecr.*.amazonaws.com.cn"]
  defaultCacheDuration: 12h
  apiVersion: credentialprovider.kubelet.k8s.io/v1
```
kubelet flags: `--image-credential-provider-config=<file> --image-credential-provider-bin-dir=<directory containing the plugin binaries>`.
The ECR plugin is `ecr-credential-provider` from cloud-provider-aws; the plugins for Artifact
Registry and ACR come from their cloud providers, so follow their docs. Plugins use the **node's** cloud
identity by default, so every pod on the node can pull what the node can. The
`KubeletServiceAccountTokenForCredentialProviders` feature gate (alpha in 1.33, beta and on by
default from 1.34) lets the kubelet pass the pod's ServiceAccount token to the plugin when
`tokenAttributes` is set in the `CredentialProviderConfig`, giving a per-workload pull identity.

## The shared-image caveat
With `IfNotPresent`, a pod **without** credentials can run an image another pod already
pulled onto that node. Kubernetes lists these fixes: `imagePullPolicy: Always`, the
`AlwaysPullImages` admission controller (without it, all pods potentially have access to all images
on a node), or the `KubeletEnsureSecretPulledImages` feature gate, which verifies pull credentials even
for images already present on the node (alpha in 1.33 and 1.34, beta and on by default from 1.35).

## Debug `ErrImagePull` auth failures
```bash
kubectl describe pod <p> | grep -A3 "Failed to pull"
# "pull access denied ... may require 'docker login'" / "401 Unauthorized" / "403"
kubectl get secret regcred -n app -o jsonpath='{.data.\.dockerconfigjson}' | base64 -d | jq
```
Check: the server string matches the image host exactly (including any port), the credential has
not expired, and the ServiceAccount was actually patched.

## Verify
- [ ] Pods in a fresh namespace pull private images with no manual step.
- [ ] No long-lived registry passwords in git; robot accounts are pull-only.

## Checked

2026-10-27. Release: Kubernetes v1.37 docs (kubernetes/website main), October 2026
- Confirmed `CredentialProviderConfig` (`kubelet.config.k8s.io/v1`), provider `apiVersion: credentialprovider.kubelet.k8s.io/v1`, required `matchImages` and `defaultCacheDuration` (example `12h`), the `--image-credential-provider-config` and `--image-credential-provider-bin-dir` flags, and the `ecr-credential-provider` example in the credential provider page.
- Corrected feature stages from the feature-gate pages: `KubeletServiceAccountTokenForCredentialProviders` is alpha 1.33 and beta (default on) from 1.34; `KubeletEnsureSecretPulledImages` is alpha 1.33-1.34 and beta (default on) from 1.35. The old text called both alpha.
- Confirmed the `AlwaysPullImages` and `imagePullPolicy: Always` guidance and the ServiceAccount `imagePullSecrets` approach in the Kubernetes images page. Removed the GCP and Azure plugin binary names, the plugin directory path, the ECR 12-hour token claim, the Docker Hub index URL claim and the `crictl pull --creds` command, none of which were confirmed.

Method: documentation only; no commands were run.

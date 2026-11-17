---
id: computing-software.cloud-infrastructure-engineering.kubernetes.imagepolicywebhook-admission
name: imagepolicywebhook-admission
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, admission-controllers, imagepolicywebhook, image-security, admissionconfiguration]
level: practitioner
status: docs-checked
description: "Configure the ImagePolicyWebhook admission plugin: AdmissionConfiguration file, kubeconfig to the backend, defaultAllow, TTLs and apiserver manifest mounts."
sources: ["https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#imagepolicywebhook", "https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ImagePolicyWebhook

Built-in admission plugin that asks an external service whether each pod's images are allowed
(a validating plugin, disabled by default). Modern setups usually use Kyverno/Gatekeeper/ValidatingAdmissionPolicy,
but this is built in and needs no in-cluster dependency (only a reachable HTTPS backend).

## Files on the control-plane node
`/etc/kubernetes/admission/admission-config.yaml`:
```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: AdmissionConfiguration
plugins:
- name: ImagePolicyWebhook
  configuration:
    imagePolicy:
      kubeConfigFile: /etc/kubernetes/admission/imagepolicy.kubeconfig
      allowTTL: 50
      denyTTL: 50
      retryBackoff: 500
      defaultAllow: false        # fail closed if the backend is unreachable
```
`imagepolicy.kubeconfig`: `clusters[].cluster.server` = backend URL with its CA, `users[]` =
client cert for the apiserver.

## kube-apiserver manifest
```yaml
- --enable-admission-plugins=NodeRestriction,ImagePolicyWebhook
- --admission-control-config-file=/etc/kubernetes/admission/admission-config.yaml
- --runtime-config=imagepolicy.k8s.io/v1alpha1=true
volumeMounts:
- {name: admission, mountPath: /etc/kubernetes/admission, readOnly: true}
volumes:
- {name: admission, hostPath: {path: /etc/kubernetes/admission, type: DirectoryOrCreate}}
```
The config file and the kubeconfig it references must be readable inside the apiserver container,
so mount the directory (a missing mount stops the apiserver from loading the plugin configuration).
The backend must be reached over TLS (`server` must be an `https` URL).

## Backend contract
The apiserver POSTs an `ImageReview` (`imagepolicy.k8s.io/v1alpha1`, which the apiserver must
enable with the `--runtime-config` flag above) describing the containers being admitted, the
namespace, and pod annotations that match `*.image-policy.k8s.io/*`; the backend replies with
`status.allowed` (true or false) and, when denying, a `status.reason` string.

## Verify
```bash
sudo crictl ps | grep kube-apiserver          # running after edit
kubectl run t --image=docker.io/library/nginx:latest   # denied with the backend's reason when disallowed
```
`defaultAllow: false` plus backend down blocks all pod creation, including system pods; have a
break-glass plan.

## Checked
Checked 2026-10-23 against the kubernetes/website docs (current release 1.37) and kubernetes/kubernetes source.
Confirmed: plugin disabled by default; config keys `kubeConfigFile`, `allowTTL` (seconds), `denyTTL` (seconds), `retryBackoff`
(milliseconds), `defaultAllow` (behaviour when the backend fails); embedded `configuration:` form and `--admission-control-config-file`;
kubeconfig layout (`https` server, CA, client cert); `ImageReview` `imagepolicy.k8s.io/v1alpha1` and the `--runtime-config` requirement;
annotation filter `*.image-policy.k8s.io/*`; `status.allowed` and `reason`. Wrong in the original: the runtime-config requirement was
missing and the annotation pattern was described as "ending in". Removed the unconfirmed crash-message claim.
Method: documentation only; no commands were run.

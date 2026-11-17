---
id: computing-software.cloud-infrastructure-engineering.calico.calico-apiserver-kubectl-management
name: calico-apiserver-kubectl-management
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [apiserver, kubectl, calicoctl, aggregation-api, openssl, tigerastatus, v3-api]
level: practitioner
status: docs-checked
description: "Enable kubectl to manage projectcalico.org/v3 resources via the Calico API server: operator APIServer resource or manifest with openssl certs, and what calicoctl still does."
sources:
  - https://docs.tigera.io/calico/latest/operations/install-apiserver
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Calico API server lets you manage `projectcalico.org/v3` resources with `kubectl`, doing the defaulting and validation server-side that calicoctl used to do. Native v3 CRDs are the successor and are the default for new installs; this page covers the aggregation server.

calicoctl is still required for `calicoctl node`, `calicoctl ipam` and `calicoctl version`.

**Operator install.** Create the resource, then check it:

```bash
kubectl create -f - <<EOF
apiVersion: operator.tigera.io/v1
kind: APIServer
metadata:
  name: default
spec: {}
EOF
kubectl get tigerastatus apiserver
```

**Manifest install.** Apply `manifests/apiserver.yaml` (deployment in `calico-apiserver`); the pod waits in `ContainerCreating` for credentials. Generate a certificate (needs openssl 1.1.1 or above for `-addext`):

```
openssl req -x509 -nodes -newkey rsa:4096 -keyout apiserver.key -out apiserver.crt -days 365 -subj "/" -addext "subjectAltName = DNS:calico-api.calico-apiserver.svc"
```

Store it as secret `calico-apiserver-certs` in `calico-apiserver` from both files, then patch `apiservice v3.projectcalico.org` so `spec.caBundle` is the secret's `apiserver.crt` value.

Check with `kubectl api-resources | grep '\sprojectcalico.org'`. kubectl may keep preferring `crd.projectcalico.org` from its local cache; delete the cluster's cache directory under the kube cache to force a refresh.

To use API-server mode on a new install, apply the v1 CRDs before the operator. Uninstall with `kubectl delete apiserver default`; afterwards use calicoctl unless on native CRDs.

## Checked

2026-11-08. The Enable kubectl to manage Calico APIs page was read in full. Steps, certificate command, resource list check, cache note, calicoctl subcommands and uninstall were confirmed.

Method: documentation only; no commands were run.

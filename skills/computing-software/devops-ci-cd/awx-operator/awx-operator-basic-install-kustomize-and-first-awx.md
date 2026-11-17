---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-basic-install-kustomize-and-first-awx
name: awx-operator-basic-install-kustomize-and-first-awx
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, install, kustomize, awx-cr, nodeport, make-deploy, admin-password]
level: intro
status: docs-checked
description: "Install the AWX Operator with Kustomize at a pinned tag, create an AWX custom resource and fetch the generated admin password."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/installation/basic-install.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator basic install kustomize and first awx

Pick a release tag first (`git clone` the repo, `git tag`, `git checkout tags/2.7.2`). If you work from a fork with changes since the tag, `export VERSION=<tag>` or the operator ends up in ImagePullBackOff.

Deploy the operator with `make deploy` (a custom image: `IMG=quay.io/$YOURNAMESPACE/awx-operator:$YOURTAG make deploy`) or with a `kustomization.yaml`:

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - github.com/ansible/awx-operator/config/default?ref=<tag>
images:
  - name: quay.io/ansible/awx-operator
    newTag: <tag>
namespace: awx
```

`kubectl apply -k .` creates the namespace, CRDs (awxs, awxbackups, awxrestores), service account, roles, the metrics service and the `awx-operator-controller-manager` deployment. Set the namespace for kubectl: `kubectl config set-context --current --namespace=awx`.

Then add `awx-demo.yml` to `resources` and apply again:

```yaml
apiVersion: awx.ansible.com/v1beta1
kind: AWX
metadata:
  name: awx-demo
spec:
  service_type: nodeport
```

`metadata.name` names the deployment (use unique names if several AWX instances share a namespace). On OpenShift use `service_type: clusterip` with `ingress_type: Route`. Watch with `kubectl get pods -l "app.kubernetes.io/managed-by=awx-operator"` and `kubectl logs -f deployments/awx-operator-controller-manager -c awx-manager`. The admin user is `admin`; its password is in the `<resourcename>-admin-password` secret.

## Checked

2026-11-09. Confirmed tag selection, the VERSION note, make deploy and IMG, the kustomization contents, created resources, namespace command, AWX resource examples, OpenShift route settings, watch commands and admin secret against the AWX Operator basic install page (read in full).

Method: docs-checked 2026-11-09 against the AWX Operator docs page docs/installation/basic-install.md

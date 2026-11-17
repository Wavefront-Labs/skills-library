---
id: computing-software.cloud-infrastructure-engineering.ansible.awx-dev-install-on-minikube-or-kind
name: awx-dev-install-on-minikube-or-kind
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, awx, awx-operator, minikube-awx, awx-dev-install, kind, kustomize, local-lab, controller-install]
level: practitioner
status: docs-checked
description: "Stand up a disposable AWX on a laptop with the AWX Operator on minikube or kind: kustomize install, NodePort access, admin password, resource sizing and teardown."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/installation/basic-install.md", "https://github.com/ansible/awx-operator/blob/devel/docs/installation/kind-install.md", "https://kind.sigs.k8s.io/docs/user/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWX dev install on minikube or kind

Goal: a throwaway AWX for testing job templates, configuration-as-code and collection changes,
without touching shared clusters.

## Size the cluster
AWX runs web, task, Redis, Postgres and an EE per job, so give the cluster generous CPU and memory (the operator docs give no minimum; start high and watch for OOM kills). Without a cluster, the operator docs point to minikube for testing; see the minikube documentation for its `start` flags.

kind, with a host port mapped to the NodePort you will use:
```yaml
# kind-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
    extraPortMappings:
      - {containerPort: 32000, hostPort: 32000}
```
`kind create cluster --config=kind-config.yaml` (the operator's kind guide also installs the NGINX ingress controller for kind).

## Install the operator and an AWX instance (kustomize)
Pick a released operator tag from the awx-operator releases page and use it twice (the `ref` and the image `newTag`; a mismatch leaves the operator in ImagePullBackOff):
```yaml
# kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - github.com/ansible/awx-operator/config/default?ref=<OPERATOR_TAG>
  - awx-demo.yml
images:
  - name: quay.io/ansible/awx-operator
    newTag: <OPERATOR_TAG>
namespace: awx
```
```yaml
# awx-demo.yml
apiVersion: awx.ansible.com/v1beta1
kind: AWX
metadata: {name: awx-demo}
spec:
  service_type: nodeport
  nodeport_port: 32000        # matches the kind mapping; optional on minikube
```
```bash
kubectl apply -k .
kubectl -n awx logs -f deployment/awx-operator-controller-manager -c awx-manager   # watch reconciliation
kubectl -n awx get pods       # wait for the awx-demo pods and the awx-demo postgres pod to be Running
```

## Log in
```bash
kubectl -n awx get secret awx-demo-admin-password -o jsonpath='{.data.password}' | base64 --decode; echo
kubectl -n awx get svc awx-demo-service            # NodePort assigned (80:<port>)
# kind: http://localhost:32000
```
User `admin`. Create a token for CLI or collection testing.

## Teardown
`kind delete cluster` removes everything (the operator docs' cleanup step); delete a minikube cluster with its own command.

## Gotchas
- Docker Desktop/WSL2 memory limits below what the cluster requests can cause pods to be OOM-killed in a loop; raise the VM memory first.
- The first job pulls the default EE image; expect a slow first run.
- Use unique `metadata.name` values if you deploy more than one AWX in a namespace.
- This is a lab: no TLS, no backups, the default admin password lives in a secret. Never point it at production credentials.
- AWX upstream versions differ from AAP controller in UI and some APIs; test AAP-specific behaviour on AAP.

## Verify
- [ ] The AWX login page loads at the NodePort URL and `admin` can sign in.
- [ ] A job template run succeeds (proves the EE pull and job pod creation work).

## Checked
2026-10-28. Confirmed in the AWX Operator basic-install and kind-install guides and the kind configuration reference: kustomize layout with `ref` and `newTag` set to the same tag, ImagePullBackOff on mismatch, `kubectl apply -k .`, AWX CR with `service_type: nodeport` and `nodeport_port`, kind `extraPortMappings` for 32000, the `<name>-admin-password` secret and `admin` user, operator log command, `kind delete cluster`. Removed because not confirmed: CPU and memory sizing and minikube flags, example pod names, the EE image size, install duration, `minikube service` and `minikube stop`/`delete` commands, the Demo Job Template and the ping check.
Method: documentation only; no commands were run.

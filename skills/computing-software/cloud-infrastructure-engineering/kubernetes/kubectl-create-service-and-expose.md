---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubectl-create-service-and-expose
name: kubectl-create-service-and-expose
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, services, kubectl-create-service, kubectl-expose, ckad, imperative-commands]
level: practitioner
status: docs-checked
description: "Create Services imperatively with kubectl create service and kubectl expose, get ports and selectors right, and generate YAML for later edits."
sources: ["https://kubernetes.io/docs/reference/kubectl/generated/kubectl_create/kubectl_create_service/", "https://kubernetes.io/docs/reference/kubectl/generated/kubectl_expose/", "https://github.com/kubernetes/kubectl/blob/master/pkg/cmd/create/create_service.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# kubectl create service and kubectl expose

## expose: copies the selector from an existing object
```bash
kubectl expose deploy web --port=80 --target-port=8080 --name=web
kubectl expose deploy web --port=80 --target-port=http --type=NodePort --name=web-np
kubectl expose pod debug --port=5432 --name=debug-db
kubectl expose deploy web --port=80 --target-port=8080 --dry-run=client -o yaml > svc.yaml
```
`expose` looks up a deployment, service, replica set, replication controller or pod by name and
uses its selector for the new Service. A deployment or replica set is exposed only if its selector
is convertible to one a Service supports, that is, it contains only `matchLabels`. `--port` is
copied from the resource if unspecified, `--target-port` takes a number or a name, `--type` is
`ClusterIP` (default), `NodePort`, `LoadBalancer` or `ExternalName`, and `--selector` overrides the
inferred selector (equality-based only). Without `--name` the new Service takes a default name
derived from the object.

## create service: you get selector app=<name>
```bash
kubectl create service clusterip web --tcp=80:8080            # selector app=web
kubectl create service nodeport web --tcp=80:8080 --node-port=30080
kubectl create service loadbalancer web --tcp=443:8443
kubectl create service clusterip db --clusterip="None"         # headless
kubectl create service externalname ext-db --external-name=db.example.com
```
`create service` always sets the selector to `app=<name>`; there is no selector flag. If your pods
are not labelled that way, generate YAML with `--dry-run=client -o yaml`, fix the selector, then
apply, or use `kubectl expose`.

## Check it worked
```bash
kubectl get svc web -o wide                     # SELECTOR column
kubectl get endpointslices -l kubernetes.io/service-name=web
```
Empty endpoints mean the selector does not match pod labels or the pods are not Ready.

## Gotchas
- `--tcp=<port>:<targetPort>` uses the Service port first; for `expose`, `--port` is the Service
  port and `--target-port` the container port.
- `--tcp` takes a comma-separated list for several port pairs; for named ports edit the YAML.

## Checked

2026-10-23, Kubernetes documentation (kubernetes/website main, v1.36 docs) and kubernetes/kubernetes source. Confirmed against the kubectl source (create_service.go: the clusterip, nodeport, loadbalancer and externalname subcommands, their flags, the app=<name> selector; expose.go: supported kinds, matchLabels-only rule, flags and defaults). Removed the busybox test command, the claim that mixing up the ports always gives connection refused, and the advice to name each port.

Method: documentation only; no commands were run.

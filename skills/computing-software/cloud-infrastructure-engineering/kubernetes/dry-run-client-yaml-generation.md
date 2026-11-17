---
id: computing-software.cloud-infrastructure-engineering.kubernetes.dry-run-client-yaml-generation
name: dry-run-client-yaml-generation
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubectl, dry-run-client, kubectl-create, imperative, kubectl-run]
level: practitioner
status: docs-checked
description: "Generate manifests fast with --dry-run=client -o yaml for pods, deployments, services, jobs, cronjobs, configmaps and RBAC, then edit and apply: the exam workflow."
sources: ["https://kubernetes.io/docs/reference/kubectl/conventions/", "https://kubernetes.io/docs/reference/kubectl/generated/kubectl_create/", "https://github.com/kubernetes/kubernetes/tree/master/staging/src/k8s.io/kubectl/pkg/cmd/run", "https://kubernetes.io/docs/reference/using-api/api-concepts/#dry-run"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generating YAML with --dry-run=client

```bash
export do="--dry-run=client -o yaml"
kubectl run web --image=nginx --port=80 --labels=app=web $do > pod.yaml
kubectl run tmp --image=busybox --restart=Never --command $do -- sleep 3600
kubectl create deployment web --image=nginx --replicas=3 --port=80 $do > deploy.yaml
kubectl expose deployment web --port=80 --target-port=8080 --type=ClusterIP $do > svc.yaml
kubectl create job pi --image=perl $do -- perl -Mbignum=bpi -wle 'print bpi(200)'
kubectl create cronjob backup --image=busybox --schedule='0 2 * * *' $do -- sh -c 'date'
kubectl create configmap app --from-literal=LOG=debug --from-file=app.conf $do
kubectl create secret generic db --from-literal=password=x $do
kubectl create serviceaccount ci $do
kubectl create role r --verb=get --resource=pods $do
kubectl create ingress web --rule='a.example.com/*=web:80' $do
kubectl create pdb web --selector=app=web --max-unavailable=1 $do
```
Then edit (add resources, probes, volumes) and `kubectl apply -f`.

## client vs server
- `--dry-run=client`: previews the object that would be sent to the cluster without submitting it.
- `--dry-run=server`: the request goes to the API server, which guarantees nothing is persisted and no other side effects; admission controllers that support dry-run run (all built-in plugins do, webhooks must declare support).

## Trimming output
For existing objects, export with `kubectl get deploy web -o yaml` and remove server-populated fields such as `status` before reusing the manifest.

## Gotchas
- `kubectl run` creates a Pod.
- Arguments after `--` go to the container; `--command` makes them the command instead of args.

## Checked
Checked 2026-10-24 against the kubectl run, create deployment, create job, create cronjob and expose source (main), the kubectl conventions page and the API concepts dry-run section (v1.37): flags `--image`, `--port`, `--labels`, `--restart`, `--command`, `--replicas`, `--schedule`, `--target-port`, `--type`; arguments after `--`; client versus server dry-run semantics; the Job `perl -Mbignum=bpi` example appears in the Job docs. Removed pinned image tags, the output-trimming remarks and the kubectl neat plugin.
Method: documentation only; no commands were run.

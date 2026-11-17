---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubectl-output-formatting-jsonpath-and-custom-columns
name: kubectl-output-formatting-jsonpath-and-custom-columns
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubectl, jsonpath, custom-columns, go-template, sort-by, output-formatting, cka, ckad]
level: practitioner
status: docs-checked
description: "Extract exactly what you need from kubectl: jsonpath with filters and ranges, custom-columns, go-template, --sort-by, and when to pipe to jq instead."
sources: ["https://kubernetes.io/docs/reference/kubectl/jsonpath/", "https://kubernetes.io/docs/reference/kubectl/quick-reference/#formatting-output"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubectl output: jsonpath, custom-columns, go-template

## jsonpath
```bash
kubectl get pod web-1 -o jsonpath='{.status.podIP}'
kubectl get pods -o jsonpath='{.items[*].metadata.name}'
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.nodeName}{"\n"}{end}'
kubectl get nodes -o jsonpath='{.items[*].status.addresses[?(@.type=="InternalIP")].address}'
kubectl get pod web-1 -o jsonpath='{.status.containerStatuses[?(@.name=="app")].restartCount}'
kubectl get secret db -o jsonpath='{.data.password}' | base64 -d
kubectl get cm kube-root-ca.crt -o jsonpath='{.data.ca\.crt}'        # escape dots in keys
kubectl get deploy -o jsonpath='{.items[*].spec.template.spec.containers[*].image}' | tr ' ' '\n' | sort -u
```
Rules: wrap in single quotes; `{range}...{end}` to iterate; `?(@.field=="x")` filter; `..` for
recursive descent (`{..image}`). Regular expressions are not supported in JSONPath; use jq.
On Windows, double-quote templates that contain spaces and use single quotes or escaped
double quotes for literals inside.

## custom-columns
```bash
kubectl get pods -o custom-columns=NAME:.metadata.name,NODE:.spec.nodeName,IP:.status.podIP,RESTARTS:.status.containerStatuses[0].restartCount
kubectl get pods -A -o custom-columns='NS:.metadata.namespace,POD:.metadata.name,QOS:.status.qosClass' --no-headers
kubectl get nodes -o custom-columns-file=cols.txt
```

## Sorting
```bash
kubectl get pods --sort-by=.metadata.creationTimestamp
kubectl get pods -A --sort-by='.status.containerStatuses[0].restartCount'
kubectl get events -A --sort-by=.metadata.creationTimestamp
kubectl get pv --sort-by=.spec.capacity.storage
```

## go-template (conditionals)
```bash
kubectl get pods -o go-template='{{range .items}}{{if ne .status.phase "Running"}}{{.metadata.name}} {{.status.phase}}{{"\n"}}{{end}}{{end}}'
kubectl get secret db -o go-template='{{range $k,$v := .data}}{{$k}}={{$v | base64decode}}{{"\n"}}{{end}}'
```

## When to use jq/yq
Aggregations, regex, joins:
```bash
kubectl get pods -A -o json | jq -r '.items[] | select(.status.containerStatuses[]?.restartCount > 5) | "\(.metadata.namespace)/\(.metadata.name)"'
```
Other outputs: `-o wide`, `-o name` (print only the resource name), `-o yaml`, `--show-labels`, `-o go-template-file=<file>`.

## Verify
- [ ] Scripts use `-o jsonpath`/`-o json | jq`, never parsing the human table output.

## Checked
Date: 2026-10-27. Documentation: Kubernetes website "JSONPath Support" and kubectl "Quick
Reference" (current docs; latest release v1.37.1). Confirmed: `range`/`end`, filter
expressions, `..` recursive descent, no regex, escaped dots in keys, Windows quoting;
`--sort-by` forms, `custom-columns`, `custom-columns-file`, `go-template` with `base64decode`,
`-o name`, `--show-labels`, `--no-headers`. Replaced the `.lastTimestamp` event sort with the
documented `.metadata.creationTimestamp`; removed the unconfirmed `-L` flag and the
"columns change between versions" and "no arithmetic" claims.
Method: documentation only; no commands were run.

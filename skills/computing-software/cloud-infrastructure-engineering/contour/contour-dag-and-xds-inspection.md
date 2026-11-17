---
id: computing-software.cloud-infrastructure-engineering.contour.contour-dag-and-xds-inspection
name: contour-dag-and-xds-inspection
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [dag, graphviz, debug-dag, contour-cli, lds, rds, cds, eds, xds]
level: advanced
status: docs-checked
description: "Visualising Contour's internal DAG via /debug/dag with graphviz, and streaming xDS resources with contour cli lds/rds/cds/eds from inside the Contour pod."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/troubleshooting/contour-graph.md", "https://github.com/projectcontour/contour/blob/main/site/content/docs/main/troubleshooting/contour-xds-resources.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Inspecting the DAG and xDS resources

Object graph: Contour models configuration as a directed acyclic graph. The debug endpoint prints it in DOT format; graphviz is needed to render it.

```bash
CONTOUR_POD=$(kubectl -n projectcontour get pod -l app=contour -o name | head -1)
kubectl -n projectcontour port-forward $CONTOUR_POD 6060
curl localhost:6060/debug/dag | dot -T png > contour-dag.png
```

The sample maps `http://echo.local:80/` to the `echo` Service in `default`. Use it to confirm an HTTPProxy, its includes, Secrets and Services are linked as expected.

xDS data: `contour cli` shows exactly what Contour sends Envoy. Because xDS is secured by cluster Secrets, run it inside the pod:

```bash
CONTOUR_POD=$(kubectl -n projectcontour get pod -l app=contour -o jsonpath='{.items[0].metadata.name}')
kubectl -n projectcontour exec $CONTOUR_POD -c contour -- \
  contour cli lds --cafile=/certs/ca.crt --cert-file=/certs/tls.crt --key-file=/certs/tls.key
```

This streams updates to your terminal. Subcommands: `lds` (listeners), `rds` (routes), `cds` (clusters), `eds` (endpoints).

## Checked

2026-11-04. Confirmed against the Contour DAG and xDS resources troubleshooting pages: the fields, defaults, flags and behaviours stated above. Removed: the advice to compare with Envoy /config_dump (not on the pages).

Method: documentation only; no commands were run.

---
id: computing-software.cloud-infrastructure-engineering.kubernetes.curl-pod-service-testing
name: curl-pod-service-testing
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, troubleshooting, curl-pod, netshoot, services, dns]
level: practitioner
status: docs-checked
description: "Test Services, DNS and network policies from inside the cluster with throwaway curl or netshoot pods placed in the right namespace, node and labels."
sources: ["https://kubernetes.io/docs/tasks/debug/debug-application/debug-service/", "https://github.com/nicolaka/netshoot", "https://kubernetes.io/docs/concepts/security/pod-security-standards/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing Services from a throwaway pod

## Quick one-shot
```bash
kubectl run curl -n shop --rm -it --image=curlimages/curl --restart=Never -- \
  curl -sv -m 5 http://web.shop.svc.cluster.local:80/healthz
```
Use the same namespace as the real client: NetworkPolicies select by namespace and labels.
Pin an image tag you have verified in your registry for repeatable runs.

## With the client's labels (to test policy as that client)
```bash
kubectl run curl -n shop --rm -it --image=curlimages/curl --restart=Never \
  --labels=app=frontend -- curl -s -m 5 http://payments:8080/
```

## Full toolbox
```bash
kubectl run netshoot -n shop --rm -it --image=nicolaka/netshoot --restart=Never -- bash
# dig web.shop.svc.cluster.local ; curl -v http://web ; nc -zv db 5432 ; mtr 10.0.0.1 ; tcpdump -i eth0
```
The netshoot README lists tcpdump, mtr, dig, curl, nc/netcat, nmap and iperf among its tools.
On a specific node (to test node-local paths): add
`--overrides='{"spec":{"nodeName":"<node>"}}'`.

## Reading results
Follow the Service debugging page in order: it has a step for each row.
| What you see | Where to look (heading in the debug-service page) |
|---|---|
| DNS fails (`could not resolve host`) | "Does the Service work by DNS name?" (CoreDNS, or egress-to-DNS policy) |
| Resolves, but the connection fails | "Does the Service have any EndpointSlices?", "Is the Service defined correctly?" (`targetPort`), "Are the Pods working?" |
| Resolves, hangs | "Any Network Policy Ingress rules affecting the target Pods?", then "Is the kube-proxy working?" |
| Works by pod IP, not by Service IP | "Does the Service work by IP?" and the kube-proxy sections |

## Gotchas
- A namespace that enforces the Pod Security `restricted` level rejects the pod unless it
  sets `runAsNonRoot: true`, `allowPrivilegeEscalation: false`, drops all capabilities and
  sets a seccomp profile. Add them with `--overrides`, or use a namespace you control with
  the same labels.
- `kubectl run --rm` is only valid when attached to the container (`--attach` or
  `-i/--stdin`). For scripts, run with `--restart=Never`, then `kubectl logs`, then delete
  the pod.

## Checked
2026-10-27. Documentation: Kubernetes website main (v1.38 dev tree; latest release v1.37.1), kubectl `run` source at v1.37.1, netshoot README.
Confirmed: `--rm`, `--labels`, `--restart` flag semantics (`--rm` needs attach or stdin); Pod Security `restricted` requirements; the debug-service page headings used above; netshoot tool list.
Method: documentation only; no commands were run.

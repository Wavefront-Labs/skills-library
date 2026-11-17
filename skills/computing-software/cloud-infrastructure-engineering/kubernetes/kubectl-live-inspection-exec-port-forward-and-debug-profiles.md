---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubectl-live-inspection-exec-port-forward-and-debug-profiles
name: kubectl-live-inspection-exec-port-forward-and-debug-profiles
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubectl-exec, port-forward, kubectl-debug, debug-profile, netadmin, sysadmin, troubleshooting, ckad, debug-custom-profile]
level: practitioner
status: docs-checked
description: "Inspect running workloads live: kubectl exec patterns, port-forward to pods and Services, and kubectl debug --profile (baseline, restricted, netadmin, sysadmin)."
sources: ["https://kubernetes.io/docs/reference/kubectl/generated/kubectl_exec/", "https://kubernetes.io/docs/reference/kubectl/generated/kubectl_port-forward/", "https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/", "https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/#debugging-profiles", "https://kubernetes.io/docs/reference/kubectl/generated/kubectl_debug/", "https://kubernetes.io/docs/concepts/workloads/pods/ephemeral-containers/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Live inspection: exec, port-forward, debug profiles

## kubectl exec
```bash
kubectl exec -it deploy/web -c app -- sh               # first pod of the deployment
kubectl exec web-7c9 -- env | sort
kubectl exec web-7c9 -- cat /proc/1/status | grep -E 'VmRSS|Threads'
kubectl exec -i web-7c9 -- psql -U app < query.sql     # -i without -t for piping stdin
```
`--` separates kubectl flags from the command. Exec needs a shell/binary in the image —
distroless images → use `kubectl debug` with an ephemeral container instead.
RBAC: access to the `pods/exec` subresource. Never make "temporary prod fixes" via exec.

## kubectl port-forward
```bash
kubectl port-forward pod/web-7c9 8080:8080
kubectl port-forward svc/web 8080:80                   # picks ONE backing pod, not load-balanced
kubectl port-forward deploy/web :8080                  # random local port
kubectl port-forward --address 0.0.0.0 svc/grafana 3000:80 -n monitoring   # all addresses (default localhost; careful)
```
TCP only (UDP is not implemented). The forward is bound to the selected pod; if that pod goes
away, start it again.

## kubectl debug profiles (`--profile`)
The current `kubectl debug` reference defaults `--profile` to `general` and lists only the five
profiles below; older kubectl defaulted to `legacy` (1.22 behaviour). Pass one explicitly.

| Profile | Docs description | Typical use |
|---|---|---|
| `general` | reasonable generic properties for each debugging journey | general |
| `baseline` | compatible with Pod Security Standard baseline | baseline namespaces |
| `restricted` | compatible with Pod Security Standard restricted | restricted namespaces |
| `netadmin` | includes network administrator privileges | tcpdump, iptables, ip route |
| `sysadmin` | includes system administrator (root) privileges | strace, privileged node work |

```bash
kubectl debug -it web-7c9 --image=nicolaka/netshoot --target=app --profile=netadmin -- tcpdump -i any port 5432
kubectl debug node/worker-3 -it --image=busybox --profile=sysadmin -- chroot /host
kubectl debug -it web-7c9 --image=busybox --target=app --profile=general --custom=custom-profile.yaml
```
`--custom` (stable since v1.32) applies a partial container spec in YAML or JSON; it cannot
change `name`, `image`, `command`, `lifecycle` or volume devices.
`--target` shares the app container's process namespace. Node debug pods are named after the
node, run in the host IPC, network and PID namespaces, mount the host root at `/host`, and are
not privileged unless you use `--profile=sysadmin`; delete them afterwards.

## Gotchas
- Pick a profile the namespace's Pod Security level admits (`baseline`/`restricted`).
- An ephemeral container cannot be changed or removed once added to a Pod.

## Verify
- [ ] Node debug pods deleted; pods carrying ephemeral debug containers replaced when convenient.

## Checked
2026-10-27, against kubernetes/website main (v1.38 dev tree): `kubectl exec`, `kubectl port-forward` and `kubectl debug` references, "Use Port Forwarding", "Debug Running Pods" and "Ephemeral Containers". Confirmed: exec on `deploy/` picks the first pod; port-forward picks one pod for a resource, `--address` default localhost, `:port` for a random local port, TCP only; profile names and descriptions, `--profile` default `general` in the current reference (the task page still mentions the old `legacy` default); `--custom` stable in v1.32 and its limits; node debug pod namespaces, `/host` mount and `sysadmin` for privilege; ephemeral containers cannot be removed.
Method: documentation only; no commands were run.

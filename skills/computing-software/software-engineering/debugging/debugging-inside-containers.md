---
id: computing-software.software-engineering.debugging.debugging-inside-containers
name: debugging-inside-containers
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, production-debugging, kubectl-debug, ephemeral-containers, nsenter, distroless, kubernetes]
level: practitioner
status: draft
description: "Debug running containers, including distroless ones: kubectl debug ephemeral containers, pod copies, node debugging, nsenter into namespaces, and safe production etiquette."
sources:
  - https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/
  - https://kubernetes.io/docs/concepts/workloads/pods/ephemeral-containers/
  - https://man7.org/linux/man-pages/man1/nsenter.1.html
  - https://docs.docker.com/reference/cli/docker/debug/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Debugging inside containers

Minimal and distroless images have no shell, no curl, no ps. Bring tools to the container instead of baking them into the image.

## First look (no exec needed)
```bash
kubectl describe pod web-7d9 -n shop            # events: OOMKilled, probe failures, image pull, scheduling
kubectl logs web-7d9 -c app --previous          # logs of the crashed previous instance
kubectl get pod web-7d9 -o jsonpath='{.status.containerStatuses[*].lastState}'
kubectl top pod web-7d9 --containers
```

## Ephemeral debug container (Kubernetes 1.25+ stable)
```bash
kubectl debug -it web-7d9 -n shop --image=nicolaka/netshoot --target=app -- bash
```
- `--target=app` shares the target container's **process namespace**, so `ps aux` shows the app's processes and `/proc/<pid>/root` exposes its filesystem: `ls /proc/1/root/app/config`.
- Tools in netshoot: `curl`, `dig`, `tcpdump`, `ss`, `strace` (needs `SYS_PTRACE`; use `--profile=sysadmin` on kubectl 1.27+ or a custom profile).
- Ephemeral containers cannot be removed once added (they stop when you exit); they are not restarted and have no ports/probes.

## Copy of the pod (when you need to change things)
```bash
kubectl debug web-7d9 -it --copy-to=web-debug --container=app --image=myapp:debug -- sh
kubectl debug web-7d9 --copy-to=web-debug --share-processes --set-image=app=busybox
```
Use to override the command of a crash-looping container (`-- sleep infinity`) and inspect it without probes killing it. Delete the copy afterwards; label it so it is not mistaken for production traffic.

## Node-level debugging
```bash
kubectl debug node/ip-10-0-1-23 -it --image=ubuntu    # host filesystem mounted at /host
chroot /host
crictl ps | grep web ; crictl inspect <id> | grep -m1 '"pid"'
nsenter -t <pid> -n ss -tanp          # enter only the network namespace, use host tools
nsenter -t <pid> -m -p -- ls /app     # mount + pid namespaces
```
`nsenter -t PID -n` is the key trick: host binaries, container's network view (iptables, DNS, sockets).

## Docker (non-Kubernetes)
- `docker debug <container>` (Docker Desktop / Pro) attaches a toolbox shell to slim containers.
- `docker run -it --rm --pid=container:<id> --network=container:<id> --cap-add SYS_PTRACE nicolaka/netshoot`.
- `docker cp <id>:/app/logs ./logs`; `docker inspect` for env, mounts, health.

## Language runtimes inside containers
JVM: `jcmd 1 Thread.print`, `jcmd 1 GC.heap_dump /tmp/h.hprof` via a debug container sharing PID namespace (same user/uid required). Python: `py-spy dump --pid 1`. .NET: `dotnet-dump collect -p 1` (needs shared `/tmp` for the diagnostic socket). Go: expose `net/http/pprof` on a localhost-only port and `kubectl port-forward`.

## Etiquette
- Read-only first; record what you ran in the incident channel.
- Do not edit files in a live pod as a fix; changes vanish on restart and diverge from git.
- Restrict `pods/ephemeralcontainers` and `nodes/proxy` RBAC to on-call roles; audit logs record who debugged what.

## Verify
- [ ] On-call runbook contains the debug image name and the exact `kubectl debug` commands for each service.
- [ ] RBAC allows on-call to create ephemeral containers in production namespaces; others cannot.

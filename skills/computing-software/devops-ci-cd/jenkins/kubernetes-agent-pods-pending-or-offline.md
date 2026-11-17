---
id: computing-software.devops-ci-cd.jenkins.kubernetes-agent-pods-pending-or-offline
name: kubernetes-agent-pods-pending-or-offline
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, pod-pending-agent-offline, kubernetes-plugin, podtemplate]
level: advanced
status: docs-checked
description: "Troubleshoot Jenkins Kubernetes plugin agents: pods stuck Pending, jnlp container failing to connect, \"Waiting for next available executor\" and pod template errors."
sources: ["https://plugins.jenkins.io/kubernetes/", "https://github.com/jenkinsci/kubernetes-plugin#troubleshooting"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubernetes agent pods pending or not connecting

## Build log says "Still waiting to schedule task / Waiting for next available executor"
```bash
kubectl -n jenkins-agents get pods
kubectl -n jenkins-agents describe pod <pod>      # Events tell the story
```
| Event / status | Cause | Fix |
|---|---|---|
| `FailedScheduling: Insufficient cpu/memory` | requests too big / no nodes | lower requests, cluster autoscaler |
| `ImagePullBackOff` | image name or registry creds | `imagePullSecrets` in the pod template |
| Pod `Running` but agent offline, jnlp logs `Connection refused` | `jenkinsUrl`/`jenkinsTunnel` wrong from inside cluster | set the cloud Jenkins URL to the in-cluster service, set the tunnel, or use WebSocket |
| Pod deleted immediately | container exited (command missing) | build containers need `command: [sleep] args: [infinity]` or `cat` with `tty: true` |
| `Forbidden: pods is forbidden` in controller log | service account RBAC | grant the controller's service account the pod permissions the plugin README / Helm chart list, in the agent namespace |

## Controller-side logs
Manage Jenkins > System Log > add a log recorder for `org.csanchez.jenkins.plugins.kubernetes` at ALL level (per the plugin README).

## Keep failed pods for inspection
```groovy
podTemplate(podRetention: onFailure(), ...)     // or idleMinutes: 5
```
Remove afterwards: retained pods count against quotas.

## Timeouts
`slaveConnectTimeout` (seconds for an agent to come online; the README gives a default of 1000 s) and the `PodTemplate.connectionTimeout` system property bound slow-starting pods; raise for big images.

## Verify
- [ ] A trivial `podTemplate { node(POD_LABEL) { sh 'hostname' } }` completes.

## Checked
2026-11-02. Confirmed against the Kubernetes plugin README: podRetention onFailure(), idleMinutes, slaveConnectTimeout and connection timeout defaults (1000 s), log recorder at ALL level, imagePullSecrets, WebSocket mode, sleep command for build containers, POD_LABEL idiom. Corrected: connect timeout default was stated as 100 s. Removed: pod label selector, SEVERE log line, container cap message, explicit RBAC resource list, one-minute timing.
Method: documentation only; no commands were run.

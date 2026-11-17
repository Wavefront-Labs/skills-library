---
id: computing-software.devops-ci-cd.jenkins.kubernetes-workspace-volumes
name: kubernetes-workspace-volumes
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, kubernetes-plugin, workspace-volume, emptydir, dynamic-pvc, persistent-volume-claim, generic-ephemeral-volume, hostpath, workspace-cache, maven-cache, disk-pressure]
level: advanced
status: docs-checked
description: "Choose the workspace volume for Jenkins Kubernetes agents: emptyDir (memory or disk), dynamic PVC, ephemeral volumes or PVC, plus separate cache volumes for Maven/npm."
sources: ["https://plugins.jenkins.io/kubernetes/", "https://github.com/jenkinsci/kubernetes-plugin/blob/master/README.md", "https://kubernetes.io/docs/concepts/storage/ephemeral-volumes/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workspace volumes for Kubernetes agents

Choose the agent pod's workspace volume with `workspaceVolume`. The plugin README lists these types:

| Option | Meaning | Use |
|---|---|---|
| `emptyDirWorkspaceVolume()` (default) | an empty dir allocated on the host machine | normal builds |
| `dynamicPVC(...)` | a persistent volume claim managed dynamically, deleted at the same time as the pod | big workspaces that exceed node ephemeral storage |
| `persistentVolumeClaimWorkspaceVolume(...)` | an existing persistent volume claim by name | warm workspace reuse |
| `hostPathWorkspaceVolume(...)` | a host path volume | avoid unless you control the node |
| `nfsWorkspaceVolume(...)` | an NFS volume | shared storage |

See the plugin README for each type's arguments.

```groovy
agent {
  kubernetes {
    workspaceVolume dynamicPVC(/* see the plugin README for arguments */)
    yaml '''
spec:
  containers:
  - name: maven
    image: maven:3.9-eclipse-temurin-21
    command: [sleep]
    args: [infinity]
    volumeMounts:
    - { name: m2, mountPath: /root/.m2/repository }
  volumes:
  - name: m2
    persistentVolumeClaim: { claimName: maven-cache }
'''
  }
}
```

## Design notes
- Keep the **workspace ephemeral** and put **dependency caches** on a separate shared volume or a pull-through proxy
  (Nexus/Artifactory). Reusing workspaces reintroduces stale-state bugs.
- emptyDir is local ephemeral storage managed by the kubelet on each node (Kubernetes ephemeral volumes docs), so large
  workspaces compete for node disk; dynamic PVCs avoid that at the cost of provisioning.

## Verify
`sh 'df -h $WORKSPACE'` shows the expected volume; `kubectl get pvc -n <namespace>` lists a dynamic PVC during the build.

## Checked

2026-10-28. Confirmed in the Jenkins Kubernetes plugin README and the Kubernetes ephemeral volumes page: workspaceVolume types dynamicPVC (deleted with the pod), emptyDirWorkspaceVolume (default, on the host machine), hostPathWorkspaceVolume, nfsWorkspaceVolume, persistentVolumeClaimWorkspaceVolume, and emptyDir as kubelet-managed local ephemeral storage. Removed: genericEphemeralVolume and memory options and all argument names, the agent home path, eviction message, provisioning latency figures, and RWX/Maven claims.
Method: documentation only; no commands were run.

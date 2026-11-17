---
id: computing-software.devops-ci-cd.jenkins.kubernetes-plugin-container-step
name: kubernetes-plugin-container-step
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, kubernetes-plugin, container-step, podtemplate, multi-container-pod, defaultcontainer, jnlp, sh-in-container, shell-override, kubernetes-agent, declarative-kubernetes-agent]
level: practitioner
status: docs-checked
description: "Run Jenkins steps inside a chosen container of a Kubernetes agent pod with container(): defaultContainer, shared workspace, shell overrides, and why sh hangs in distroless images."
sources: ["https://plugins.jenkins.io/kubernetes/", "https://github.com/jenkinsci/kubernetes-plugin/blob/master/README.md", "https://www.jenkins.io/doc/pipeline/steps/kubernetes/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The `container` step

A Kubernetes plugin agent is a pod: the `jnlp` container runs the agent (remoting) and
your tool containers sit beside it sharing the workspace volume. Steps run in `jnlp`
unless you switch with `container('name')`.

## Declarative
```groovy
pipeline {
  agent {
    kubernetes {
      defaultContainer 'maven'           // every step runs here unless overridden
      yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: maven
    image: maven:3.9-eclipse-temurin-21
    command: [sleep]
    args: [infinity]
  - name: kaniko
    image: gcr.io/kaniko-project/executor:debug
    command: [sleep]
    args: [infinity]
'''
    }
  }
  stages {
    stage('Build') { steps { sh 'mvn -B package' } }
    stage('Image') {
      steps {
        container('kaniko') {
          sh '/kaniko/executor --context "$WORKSPACE" --destination registry.example.com/app:$GIT_COMMIT'
        }
      }
    }
  }
}
```
Scripted: `podTemplate(yaml: ...) { node(POD_LABEL) { container('maven') { sh '...' } } }`.

## Rules that bite
- Tool containers must stay alive: `command: [sleep] args: [infinity]` (or `cat` with
  `tty: true`). An image whose entrypoint exits makes the pod fail / restart.
- `container()` runs the shell steps in that container through a shell that defaults to
  `sh` (must be in `$PATH`; `cmd` on Windows pods). Images without a shell cannot be
  used; override with the `shell` parameter of `container` if the shell lives elsewhere.
- Workspace: containers of the pod share the workspace volume. The README warns that
  containers running as different UIDs can hit problems; use the same uid across the
  containers of a pod (`runAsUser` on the pod or container).


## Debugging
- `kubectl get pods` / `kubectl describe pod` in the agents namespace while the build runs.
- The name passed to `container()` must match a container name in the pod spec.
- For `Permission denied` on the `@tmp` durable-task files, see the plugin README
  troubleshooting section (set `HOME`/volume ownership).

## Verify
`sh 'cat /etc/os-release; id; pwd'` inside each `container()` block shows the expected
image and UID.

## Checked
2026-11-02. Confirmed against the Kubernetes plugin README and the kubernetes step reference: container step, defaultContainer, POD_LABEL, command sleep for tool containers, ttyEnabled/tty, shell parameter default sh in PATH, different-uid warning, permission-denied troubleshooting. Removed: workspace-volume name, runAsUser 1000/fsGroup advice, PATH behaviour, per-call overhead, stdin hang advice, pod label selector.
Method: documentation only; no commands were run.

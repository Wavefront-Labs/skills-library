---
id: computing-software.devops-ci-cd.jenkins.sizing-the-jnlp-container
name: sizing-the-jnlp-container
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, kubernetes-plugin, jnlp-container-resources, jnlp, inbound-agent, agent-resources, resource-requests, oomkilled, remoting, jvm-heap, java-opts, jenkins-agent-image]
level: advanced
status: docs-checked
description: "Size and pin the jnlp (inbound-agent) container of Jenkins Kubernetes pods: requests/limits, JVM heap flags, image version matching the controller, and OOMKilled agents."
sources: ["https://plugins.jenkins.io/kubernetes/", "https://github.com/jenkinsci/docker-agent", "https://www.jenkins.io/doc/book/managing/nodes/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sizing the jnlp container

The plugin adds a container named `jnlp` (image `jenkins/inbound-agent`) to every agent
pod unless you define one yourself. It runs the Jenkins agent (remoting JVM) for the pod.
Undersized, it can be OOMKilled and the agent goes offline mid-build.

## Override it in the pod YAML
```yaml
spec:
  containers:
  - name: jnlp
    image: jenkins/inbound-agent:<remoting-version>-jdk21   # pin an exact tag; track controller LTS
    resources:
      requests: { cpu: 250m, memory: 512Mi }
      limits:   { memory: 1Gi }          # no CPU limit: avoids throttling remoting
```
Or cloud-wide: *Clouds -> kubernetes -> Pod Templates -> Container Template named
`jnlp`*, or the cloud's *Defaults Provider Template* so every template inherits it.

## Rules of thumb
- Size requests from observed usage; give the jnlp container more when it does work
  itself (large `archiveArtifacts`/`stash`, big test-report parsing, steps in the default container).
- Set a memory **limit**; CPU limits can throttle the JVM, so many teams omit them.
- Prefer a percentage-based heap setting over a fixed `-Xmx` so heap follows the limit.
- Keep the agent image's Java version supported by the controller (see the Jenkins Java
  support policy page).
- Private registry / air gap: mirror the image and set it explicitly in the container
  template.

## Diagnosing
- `kubectl describe pod <agent>`: an OOMKilled last state on the `jnlp` container.
- Build log: agent went offline during the build; check CPU throttling on the jnlp container.

## Verify
After changes, `kubectl get pod <agent> -o jsonpath='{.spec.containers[?(@.name=="jnlp")].resources}'`
shows the new values, and a large `archiveArtifacts` run completes without agent loss.

## Checked
2026-11-02. Confirmed against the Kubernetes plugin README and jenkinsci/docker-agent: the container named jnlp defaults to the inbound-agent image and can be overridden in the pod template or YAML; jdk-suffixed image variants exist. Removed: memory and CPU figures, JAVA_OPTS example, log message strings, Docker Hub rate limit claim, metric name.
Method: documentation only; no commands were run.

---
id: computing-software.devops-ci-cd.jenkins.agent-and-executor-management
name: agent-and-executor-management
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, agents, executors, build-agents, nodes, labels, label-expressions, kubernetes-plugin, podtemplate, pod-template-yaml, inbound-agent, jnlp, websocket, ssh-build-agents, ec2-plugin, cloud-agents, retention-strategy, idle-termination, executor-starvation, queue, built-in-node, controller-isolation, workspace-cleanup, ws-cleanup, lockable-resources, throttle-concurrent-builds, agent-to-controller-security, jcasc]
level: advanced
status: docs-checked
description: "Size and run Jenkins agents and executors: label design, Kubernetes pod templates, inbound vs SSH vs cloud agents, retention, queue starvation, workspace cleanup and locking."
sources: ["https://www.jenkins.io/doc/book/managing/nodes/", "https://github.com/jenkinsci/kubernetes-plugin", "https://github.com/jenkinsci/lockable-resources-plugin", "https://www.jenkins.io/doc/book/security/controller-isolation/", "https://github.com/jenkinsci/remoting/blob/master/docs/inbound-agent.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Agent and executor management

**Goal:** builds start within seconds, agents are disposable or at least clean, and no
pipeline can starve the queue or run on the controller.

## 1. Mental model
- **Node** = a machine/pod Jenkins can run on; **executor** = one build slot on it;
  **label** = a tag used to pick nodes. The controller itself is the "Built-In Node" — set
  its executors to 0 (controller isolation).
- Size executors per static VM to the CPU and RAM one build needs; more executors than
  resources means slower builds, not more throughput.
- Each `node`/`agent` block, each parallel branch and each matrix cell takes **one executor**
  for its duration. Lightweight Pipeline steps (outside `node`) run on a flyweight
  executor on the controller; steps that run a process (`sh`, `bat`) must be inside a `node`.

## 2. Label design
- Labels describe **capabilities**, not hostnames: `linux`, `arm64`, `docker`, `jdk21`, `gpu`.
- Label expressions: `agent { label 'linux && docker && !arm64' }`, `||` for alternatives.
- Pin to a hostname only for licensed/hardware-bound tools — and then you have a single
  point of failure; document it.

## 3. Kubernetes plugin (the usual default)
```groovy
pipeline {
  agent {
    kubernetes {
      yamlFile 'ci/pod.yaml'          // kept in the repo, reviewed like code
      defaultContainer 'build'
      // inheritFrom 'base'           // reuse a controller-defined template
    }
  }
  stages { stage('Build') { steps { sh 'make' } } }
}
```
```yaml
# ci/pod.yaml
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: build
      image: eclipse-temurin:21
      command: [sleep]
      args: [infinity]
      resources:
        requests: { cpu: "1", memory: 2Gi }
        limits:   { memory: 4Gi }
```
- The plugin adds the `jnlp` (inbound agent) container automatically; your containers need a
  long-running command (`sleep infinity`) or the pod exits.
- Set **Container Cap** on the cloud configuration, and `podRetention` (`never()` normally,
  `onFailure()` while debugging) on the pod template; without a cap one runaway job can flood
  the cluster.
- Pod stuck Pending → requests too big for any node or quota hit; check `kubectl describe pod`.
- Container caches: mount a PVC or use a registry mirror; pods start cold otherwise.

## 4. Static and cloud VM agents
- **SSH agents** (SSH Build Agents plugin): controller connects out; simplest for Linux VMs.
  Verify host keys (*Known hosts file* or *Manually trusted* strategy, not *Non verifying*).
- **Inbound agents** (`java -jar agent.jar -url <JENKINS_URL> -secret <SECRET> -name <node> -webSocket`):
  agent connects in; good behind NAT/firewalls. With `-webSocket` only a single HTTP(S)
  connection is needed.
- **Cloud plugins** (EC2, Azure VM, GCE): set an idle-termination period and an instance cap,
  and use an on-demand availability setting (option names differ per plugin; see its docs).
- Treat agents as cattle: bake images (Packer), configure clouds and nodes via JCasC.

## 5. Queue health and starvation
- Symptom: "Waiting for next available executor on ‘label’". Check *Build Queue* hover text:
  it names the label/expression that can't be satisfied. A label typo waits forever.
- Pipelines that `input` or `sleep` inside a `node` hold executors idle — move waits outside agents.
- Nested `node` inside `node` (or a parallel inside an agent stage that also allocates
  agents) can deadlock when executors are scarce.
- Cap concurrency of heavy jobs with **Throttle Concurrent Builds** or `disableConcurrentBuilds()`.

## 6. Shared resources and workspaces
- **Lockable Resources**: `lock(resource: 'staging-db') { sh './migrate.sh' }` or
  `lock(label: 'device-farm', quantity: 1)` — serialize access across jobs without dedicated agents.
- Static agents accumulate workspaces: `cleanWs()` in `post { cleanup { } }` (Workspace
  Cleanup plugin), or `options { skipDefaultCheckout() }` + fresh checkout; prune
  `@tmp`/`@libs` dirs periodically.

## 7. Security
- Agent → controller access control is always enabled in current Jenkins; don't weaken it.
- Agents should hold only the credentials their label needs; deploy agents in a separate
  label/cloud with restricted job access (folder-scoped credentials + Job/Agent restrictions plugins).

## Verify
- [ ] Built-In Node has 0 executors.
- [ ] Every label used in Jenkinsfiles matches at least one online node/cloud template.
- [ ] Kubernetes cloud has a container cap; pod specs have requests/limits and live in the repo.
- [ ] Cloud VM agents terminate when idle; instance cap set.
- [ ] Median queue wait tracked (e.g. Prometheus plugin) and within target.
- [ ] Shared environments guarded by `lock`; static agents clean workspaces.

## Checked
2026-10-25, Jenkins documentation (jenkins.io source repo, latest commit 2026-10-21) and plugin READMEs on GitHub. Confirmed: Built-In Node executors set to 0 and agent-to-controller access control always enabled (controller-isolation page); Kubernetes plugin `yamlFile`, `defaultContainer`, `inheritFrom`, `jnlp` container, `podRetention` values `never()`/`onFailure()`/`always()` and Container Cap (plugin README); inbound agent `-webSocket` option (jenkinsci/remoting docs/inbound-agent.md); SSH host-key strategies Known hosts file, Manually trusted key, Non verifying (ssh-agents-plugin CONFIGURE.md); `lock` with `resource`, `label` and `quantity` (lockable-resources README). Removed unconfirmed sizing formula, idle-minute figures and workspace-suffix claim.
Method: documentation only; no commands were run.

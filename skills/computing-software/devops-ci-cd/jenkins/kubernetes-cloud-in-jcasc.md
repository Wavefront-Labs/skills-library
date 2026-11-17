---
id: computing-software.devops-ci-cd.jenkins.kubernetes-cloud-in-jcasc
name: kubernetes-cloud-in-jcasc
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, kubernetes-plugin, kubernetes-cloud-jcasc, jcasc, configuration-as-code, clouds, pod-templates, container-cap, jenkins-helm-chart, jenkins-tunnel, websocket, service-account]
level: advanced
status: docs-checked
description: "Define the Jenkins Kubernetes cloud and pod templates in JCasC: in-cluster vs remote API, jenkinsUrl/tunnel or WebSocket, capacity caps, namespaces and Helm chart wiring."
sources: ["https://plugins.jenkins.io/kubernetes/", "https://github.com/jenkinsci/configuration-as-code-plugin/tree/master/demos/kubernetes", "https://github.com/jenkinsci/helm-charts/blob/main/charts/jenkins/VALUES.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubernetes cloud in JCasC

```yaml
jenkins:
  clouds:
    - kubernetes:
        name: "kubernetes"
        serverUrl: ""                     # empty = in-cluster service account
        namespace: "jenkins-agents"
        jenkinsUrl: "http://jenkins.jenkins.svc.cluster.local:8080"
        jenkinsTunnel: "jenkins-agent.jenkins.svc.cluster.local:50000"
        # webSocket: true                 # instead of tunnel: agents connect over HTTP(S)
        containerCapStr: "50"             # max concurrent agent pods for this cloud
        maxRequestsPerHostStr: "32"
        connectTimeout: 10
        readTimeout: 30
        templates:
          - name: "base"
            label: "k8s"
            nodeUsageMode: EXCLUSIVE      # only builds asking for the label
            serviceAccount: "jenkins-agent"
            imagePullSecrets: [{ name: "regcred" }]
            yamlMergeStrategy: "merge"      # default is override
            yaml: |
              spec:
                nodeSelector: { workload: ci }
                containers:
                - name: jnlp
                  resources: { requests: { cpu: 250m, memory: 512Mi }, limits: { memory: 1Gi } }
```

## Remote cluster
Set `serverUrl: https://<api>`, `skipTlsVerify: false`, `serverCertificate` (CA PEM) and
`credentialsId` pointing at a *Secret text* (token) or kubeconfig *Secret file*
credential (other types are listed in the plugin README).

## RBAC the controller needs in the agents namespace
Take the exact rules from the Kubernetes plugin README / Helm chart RBAC templates. The
Helm chart's `rbac.create` (default true) creates RBAC resources; agents in another
namespace need their own RoleBinding there.

## Helm chart
The jenkinsci chart renders this cloud from `agent.*` values and extra templates from
`agent.podTemplates`; `controller.JCasC.configScripts` adds other YAML. Don't define a
second cloud with the same `name` in your own JCasC: they overwrite each other.

## Gotchas
- Agents that never connect: check `jenkinsUrl`/`jenkinsTunnel` are reachable from the
  agent namespace and the agent port is exposed; `webSocket: true` makes agents connect
  over HTTP(S) instead (useful when the controller is outside the cluster).
- `containerCapStr` too low keeps builds queued; check *Manage Jenkins -> Nodes*.

## Verify
The cloud's *Test Connection* button reports success; a pipeline with `agent { label 'k8s' }` spins a pod in
`jenkins-agents`.

## Checked
2026-11-02. Confirmed against the Kubernetes plugin README, the JCasC kubernetes demo and the Jenkins Helm chart VALUES: serverUrl, jenkinsUrl, jenkinsTunnel, containerCapStr, maxRequestsPerHostStr, connectTimeout, readTimeout, nodeUsageMode EXCLUSIVE, imagePullSecrets, serviceAccount, serverCertificate, skipTlsVerify, credentialsId types, WebSocket, yamlMergeStrategy (default override), agent.podTemplates, controller.JCasC.configScripts, rbac.create. Removed: podRetention value, RBAC rule list, token-expiry advice, log strings, reload behaviour.
Method: documentation only; no commands were run.

---
id: computing-software.devops-ci-cd.jenkins.pod-retention-and-yaml-merge-strategy
name: pod-retention-and-yaml-merge-strategy
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, kubernetes-plugin, pod-retention, yaml-merge-strategy, podretention, on-failure, merge-strategy, override, podtemplate-yaml, debugging-agent-pods, idle-minutes]
level: advanced
status: docs-checked
description: "Keep failed Jenkins Kubernetes agent pods for debugging with podRetention, and control how child pod YAML combines with parents via yamlMergeStrategy merge() vs override()."
sources: ["https://plugins.jenkins.io/kubernetes/", "https://github.com/jenkinsci/kubernetes-plugin/blob/master/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pod retention and YAML merge strategy

## Pod retention
To inspect a failed agent pod:
```groovy
agent {
  kubernetes {
    podRetention onFailure()     // never(), onFailure(), always(), evicted(), default()
    yamlFile 'ci/pod.yaml'
  }
}
```
- `podRetention` controls whether agent pods are kept; if empty, the pod is deleted after `activeDeadlineSeconds` has passed.
- If `podRetention` is `never()` or `onFailure()`, the pod is also deleted after `activeDeadlineSeconds` passes.
- Retained pods keep consuming node resources while they exist; set a deadline, or clean up with kubectl (the plugin README
  shows a `kubectl delete` example selecting pods by label).
- For live debugging: `idleMinutes` keeps the pod active for reuse until that many minutes have passed since the last step,
  or add `sh 'sleep 3600'` in a `post { failure }` block temporarily and `kubectl exec -it <pod> -c <container> -- sh`.

## YAML merge strategy
When a pod template inherits from a parent (`inheritFrom`), `yamlMergeStrategy` controls whether the child's `yaml` overrides or is
merged with the yaml inherited from the parent templates: `merge()` or `override()`, default `override()` (kept for backward compatibility).

```groovy
podTemplate(inheritFrom: 'base', yamlMergeStrategy: merge(), yaml: '''
spec:
  containers:
  - name: node
    image: node:20
    command: [sleep]
    args: [infinity]
''') { node(POD_LABEL) { container('node') { sh 'npm ci' } } }
```
With the default `override()`, settings that only the parent's yaml defines (tolerations, node selectors, service account) are not combined with the child's yaml.

## Verify
- Retention: fail a build, `kubectl get pods -n <namespace>` still lists the agent pod.
- Merge: enable `showRawYaml` (outputs the raw pod manifest) and confirm the parent's settings are present.

## Checked

2026-10-28. Confirmed in the Jenkins Kubernetes plugin README and Helm chart values: podRetention values never(), onFailure(), always(), evicted(), default(), the empty-value default of deleting the pod after activeDeadlineSeconds, activeDeadlineSeconds for never() and onFailure(), idleMinutes, showRawYaml, yamlMergeStrategy merge()/override() default override, inheritFrom, a kubectl delete cleanup example in the README. Corrected the draft: it said never() is the default and that retained pods are never deleted (activeDeadlineSeconds applies), and omitted evicted(). Removed: the UI path for cloud retention, the per-field merge rules, jenkins=agent label, and the one-level inheritance remark.
Method: documentation only; no commands were run.

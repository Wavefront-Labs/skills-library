---
id: computing-software.devops-ci-cd.flagger.flagger-retry-failed-release-faq
name: flagger-retry-failed-release-faq
category: computing-software
field: devops-ci-cd
product: flagger
tags: [faq, retry, annotations, replicas]
level: intro
status: docs-checked
description: "Retry a failed Flagger release or change replica counts without an HPA by changing a pod template annotation to trigger a new analysis."
sources:
  - https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/faq.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An analysis triggers on changes to the Deployment or DaemonSet PodSpec (metadata, image, command, ports, env, resources), or to ConfigMaps and Secrets mounted as volumes or mapped to environment variables.

To retry a failed release, change or add an annotation on the pod template:

```yaml
spec:
  template:
    metadata:
      annotations:
        timestamp: "2020-03-10T14:24:48+0000"
```

To change replicas when not using an HPA, update `spec.replicas` on the canary (target) deployment and also annotate the template to trigger analysis; after it finishes Flagger promotes the replica change to the primary.

```yaml
spec:
  replicas: 4
  template:
    metadata:
      annotations:
        timestamp: "2022-02-10T14:24:48+0000"
```

## Checked

2026-11-03. Confirmed against the Flagger documentation: https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/faq.md.

No wrong claims found; nothing needed removing.

Method: documentation only; no commands were run.

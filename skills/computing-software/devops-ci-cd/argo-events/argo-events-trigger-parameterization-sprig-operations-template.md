---
id: computing-software.devops-ci-cd.argo-events.argo-events-trigger-parameterization-sprig-operations-template
name: argo-events-trigger-parameterization-sprig-operations-template
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, sprig, datatemplate, contexttemplate, operation, append, prepend, template-parameters]
level: advanced
status: docs-checked
description: "Transform event values with sprig templates, append or prepend to destinations, and parameterize the trigger template itself."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/tutorials/02-parameterization.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events trigger parameterization sprig operations template

Sprig templates: `dataTemplate` and `contextTemplate` rewrite event data or context before it is applied. Input is available as `.Input`.

```yaml
parameters:
  - src:
      dependencyName: test-dep
      dataTemplate: "{{ .Input.body.message | title }}"
    dest: spec.arguments.parameters.0.value
  - src:
      dependencyName: test-dep
      contextTemplate: "{{ .Input.subject | title }}"
    dest: spec.arguments.parameters.1.value
  - src:
      dependencyName: test-dep
      dataTemplate: "{{ .Input.body.name | nospace | lower }}-"
    dest: metadata.generateName
    operation: append
```

With body `{"name":"foo bar","message":"hello there!!"}`, the message becomes "Hello There!!" and the Workflow gets a name like `webhook-foobar-xxxxx`.

Operation: `operation` on a parameter can be `append` or `prepend` to the existing value at `dest`; prepending `hey!!` to `hello world` gives `hey!!hello world`.

Trigger template parameterization: parameters applied at the trigger template level (not inside the `k8s` resource block) change the trigger template itself, for example its own `parameters` or the URL of an external source such as S3 or Git. In the tutorial a request body carrying `dependencyName`, `dataKey`, `dest` and `message` rewrites which dependency key populates the workflow parameter. Defaults and operations work there too.

## Checked

2026-11-07: Read in full from a local clone of the argoproj/argo-events docs (master), which is the source of the cited GitHub page: docs/tutorials/02-parameterization.md. Confirmed: dataTemplate/contextTemplate examples, .Input, nospace/lower/title results, append/prepend operation, trigger template level parameters. Removed or changed: the invented path triggers[].parameters and 'source URL and so on', reworded to what the page says. The example manifests the page links to (under examples/) were not opened; only snippets printed on the page were checked.

Method: documentation only; no commands were run.

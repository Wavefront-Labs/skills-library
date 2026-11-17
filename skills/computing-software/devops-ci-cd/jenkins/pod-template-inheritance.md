---
id: computing-software.devops-ci-cd.jenkins.pod-template-inheritance
name: pod-template-inheritance
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, kubernetes-plugin, inherit-from, inheritfrom, pod-template, nested-pod-templates, defaults-provider-template, pod-template-library, shared-libraries, libraryresource]
level: advanced
status: docs-checked
description: "Reuse Jenkins Kubernetes pod templates via inheritFrom, nested podTemplate blocks and the defaults provider template, and know which fields are inherited vs overwritten."
sources: ["https://plugins.jenkins.io/kubernetes/", "https://github.com/jenkinsci/kubernetes-plugin/blob/master/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pod template inheritance

## Three mechanisms
1. **`inheritFrom`**: a pipeline template extends other pod templates (the plugin docs: "List of one or more pod templates to inherit from").
   With several, later items override earlier ones; a referenced template that is not found is ignored.
   ```groovy
   agent { kubernetes { inheritFrom 'mypod'; yaml '...' } }
   ```
2. **Nesting** (scripted): inner `podTemplate` blocks inherit from the enclosing one,
   building one pod with all containers.
   ```groovy
   podTemplate(containers: [containerTemplate(name: 'maven', image: 'maven:3.9', command: 'sleep', args: 'infinity')]) {
     podTemplate(containers: [containerTemplate(name: 'docker', image: 'docker:27-cli', command: 'sleep', args: 'infinity')]) {
       node(POD_LABEL) { container('maven') { sh 'mvn -v' }; container('docker') { sh 'docker version' } }
     }
   }
   ```
   To remove implicit inheritance in a scripted nested template use `inheritFrom ''`; `inheritFrom 'otherParent'` overrides it.
3. **Defaults provider template**: the name of a pod template used to provide default values (Helm chart value `agent.defaultsProviderTemplate`).

## YAML merge
The raw `yaml` of a child is combined with the yaml inherited via `inheritFrom` according to `yamlMergeStrategy`:
`merge()` or `override()`, default `override()` (kept for backward compatibility). See
`computing-software.devops-ci-cd.jenkins.pod-retention-and-yaml-merge-strategy`.

## Pattern: template library in a shared library
Keep pod YAML under the library's `resources/` directory and load it with the `libraryResource` step (external libraries only), for example
`def call(String kinds) { libraryResource("podtemplates/${kinds}.yaml") }`; pipelines then use `yaml podYaml('java21')`.

## Gotchas
- A template name that does not exist in `inheritFrom` is ignored, so a typo silently inherits nothing.

## Verify
Set `showRawYaml` (it enables output of the raw pod manifest) and confirm the containers and volumes from each parent appear.

## Checked

2026-10-28. Confirmed in the Jenkins Kubernetes plugin README and plugin page, the Helm chart values and the shared libraries page: inheritFrom (list, later items override, missing template ignored), nesting of podTemplate blocks with inheritFrom '' to drop inheritance, yamlMergeStrategy merge()/override() default override, showRawYaml, agent.defaultsProviderTemplate, libraryResource loading from resources/ for external libraries. Removed: space-separated multiple names, the per-field merge table, the declarative nested-agent claim, cloud-template timing, and the claim that inheritFrom takes names not labels.
Method: documentation only; no commands were run.

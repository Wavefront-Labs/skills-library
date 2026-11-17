---
id: computing-software.devops-ci-cd.jenkins.jenkins-yaml-structure
name: jenkins-yaml-structure
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, jcasc, configuration-as-code, jcasc-yaml, jenkins-yaml, casc-jenkins-config, root-elements, unclassified, security-realm, authorization-strategy, multiple-config-files, jenkins-helm-chart]
level: practitioner
status: docs-checked
description: "Lay out a Jenkins Configuration-as-Code jenkins.yaml: root keys (jenkins, credentials, security, unclassified, tool, jobs), CASC_JENKINS_CONFIG paths, split files and merge rules."
sources: ["https://github.com/jenkinsci/configuration-as-code-plugin/blob/master/README.md", "https://plugins.jenkins.io/configuration-as-code/", "https://github.com/jenkinsci/configuration-as-code-plugin/blob/master/docs/features/jsonSchema.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# jenkins.yaml structure

## Where Jenkins reads it
`CASC_JENKINS_CONFIG` (env) or the `casc.jenkins.config` Java property holds a comma-separated list of: a folder (traversed
recursively for `.yml`, `.yaml`, `.YAML`, `.YML` files), a full path or `file://` URI, or an HTTP(S) URL. If neither is set the plugin
looks for a single file at `$JENKINS_HOME/jenkins.yaml`. The Configuration as Code page is under *Manage Jenkins -> Configuration as Code*.
Helm chart: `controller.JCasC.configScripts` holds the JCasC scripts.

## Root keys
```yaml
jenkins:                 # core Jenkins settings
  systemMessage: "Managed by JCasC - UI changes are overwritten"
  numExecutors: 0
  nodes:
    - dumb:
        mode: NORMAL
        name: "agent1"
```
Other plugins add their own root elements. The fastest way to find them is the **Documentation** link at the bottom of the
Configuration as Code page: it shows which root element belongs to each plugin, and the repository's demos directory has examples.

## Splitting files
Split by concern (for example `core.yaml`, `security.yaml`, `clouds.yaml`). All discovered files **must be supplementary**: they cannot
overwrite each other's values, a conflict raises a `ConfiguratorException`, and the order of traversal does not matter.

## Gotchas
- `${VAR}` is variable interpolation in every block; escape a literal `${...}` as `^${VAR}`.
- Do not put secrets in plain interpolated fields such as `systemMessage: "${SENSITIVE_VARIABLE}"`: the README warns that this can
  expose the value to all users.

## Verify
The Configuration as Code page is reachable and shows your values.

## Checked

2026-10-28. Confirmed in the JCasC README, plugin page and jsonSchema page: CASC_JENKINS_CONFIG as a comma-separated list of folders, files and URLs, recursive traversal for .yml/.yaml/.YAML/.YML, casc.jenkins.config, default $JENKINS_HOME/jenkins.yaml, the Configuration as Code page, supplementary files and ConfiguratorException, ^${VAR} escape, the secrets warning for systemMessage, the jenkins numExecutors and nodes/dumb example, controller.JCasC.configScripts in the Helm chart. Removed: the long root-key sample (security, credentials, unclassified, tool, jobs, realms), CASC_MERGE_STRATEGY and the conflict message text, the lists-are-replaced and unknown-key claims. Sources: usageScenarios.md returned 404 and was replaced.
Method: documentation only; no commands were run.

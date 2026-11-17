---
id: computing-software.devops-ci-cd.jenkins.troubleshooting-jcasc-load-errors
name: troubleshooting-jcasc-load-errors
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, jcasc-troubleshooting, jcasc, configuration-as-code]
level: practitioner
status: docs-checked
description: "Fix JCasC startup and reload failures: unknown attributes after plugin upgrades, missing plugins, variable resolution, ordering and using the export and schema to correct YAML."
sources: ["https://github.com/jenkinsci/configuration-as-code-plugin/blob/master/README.md", "https://github.com/jenkinsci/configuration-as-code-plugin/blob/master/docs/features/configExport.md", "https://github.com/jenkinsci/configuration-as-code-plugin/blob/master/docs/features/jsonSchema.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting JCasC load errors

A JCasC load problem can raise a `ConfiguratorException` (for example when two files set the same value). Read the
controller log first (`kubectl logs` on Kubernetes).

## Error patterns
| Symptom | Meaning | Fix |
|---|---|---|
| `ConfiguratorException` after adding a second file or folder under `CASC_JENKINS_CONFIG` | Discovered files must be supplementary: they cannot overwrite each other's values | set each value in exactly one file |
| `${...}` text replaced or missing in a script or string | JCasC treats `${VAR}` as variable interpolation in all blocks | escape a literal as `^${VAR}`; see "Handling Secrets" in the plugin README for where variables come from |
| A key for a plugin is not recognised | the root element belongs to a plugin or changed with a version | open the Documentation link at the bottom of the Configuration as Code page; it shows the root element per plugin |

## Workflow
1. Export the current configuration: as an administrator open `/configuration-as-code/` and click **Export configuration**.
   Export may not give a directly usable `jenkins.yaml`; copy the sections you need. It does not export jobs.
2. Validate with the JSON schema at `/configuration-as-code/schema` (beta; needs SYSTEM_READ permission by default).
   It checks root configurators and data types but not deeply nested configuration.
3. Escape literal `${...}` (for example in Groovy) as `^${...}`.

## Prevention
Pin plugin versions; upgrade plugins and JCasC YAML together on a staging controller; keep the export in git to spot drift.

## Verify
- [ ] Jenkins starts and the Configuration as Code page shows your values.

## Checked

2026-10-28. Confirmed in the JCasC README and feature pages: files found via CASC_JENKINS_CONFIG must be supplementary and a conflict raises ConfiguratorException, ${VAR} interpolation and the ^${VAR} escape, the Documentation link on the Configuration as Code page, export from /configuration-as-code/ (not usable as-is, no jobs), schema at /configuration-as-code/schema (beta, SYSTEM_READ, no deep nesting). Removed: the other error messages, plugins.txt, ${VAR:-default}, CASC_MERGE_STRATEGY, the /check endpoint and log messages. Sources: the TROUBLESHOOTING.md link returned 404 and was replaced.
Method: documentation only; no commands were run.

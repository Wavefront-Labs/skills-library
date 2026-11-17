---
id: computing-software.devops-ci-cd.jenkins.jcasc-export-and-schema-validation
name: jcasc-export-and-schema-validation
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, jcasc, configuration-as-code, jcasc-export, jcasc-schema, json-schema, view-configuration, check-configuration, jcasc-reference, ci-validation, yaml-language-server, config-drift]
level: advanced
status: docs-checked
description: "Bootstrap and validate Jenkins JCasC: export the live config, clean it, generate the JSON schema for editor/CI validation, and dry-run check a YAML before applying it."
sources: ["https://github.com/jenkinsci/configuration-as-code-plugin/blob/master/docs/features/configExport.md", "https://github.com/jenkinsci/configuration-as-code-plugin/blob/master/docs/features/jsonSchema.md", "https://github.com/jenkinsci/configuration-as-code-plugin/blob/master/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JCasC export and schema validation

## Export (bootstrap from a hand-configured controller)
- As an administrator open `/configuration-as-code/` and click **Export configuration**.

The export is a **starting point, not a backup**:
- Export may not give a directly usable `jenkins.yaml`; copy the sections you need instead of the entire file.
- It covers system configuration, agents, views, credentials and (with Jenkins' own user database) users. It does **not** export jobs.
- Secrets are exported in encrypted form, readable only on the same instance, so replace them with `${VAR}` references.
- Free-form fields such as view and agent descriptions are not masked.

## Schema
`/configuration-as-code/schema` serves an instance-specific JSON schema (draft-07) built from the installed plugins.
It is a beta feature: it needs SYSTEM_READ permission by default (anonymous access needs
`-Dio.jenkins.plugins.casc.allowAnonymousSchema=true`), it validates root configurators and data types, and it does not yet
validate deeply nested configuration (for example `jenkins.nodes`). Treat a pass as necessary, not sufficient.
```bash
curl -sf -u "$U:$TOKEN" "$JENKINS/configuration-as-code/schema" > jcasc.schema.json
```
Any JSON Schema validator that supports draft-07 can check the YAML (converted to JSON) against it.
Regenerate the schema whenever plugins change.

## Dry-run against a real controller
Start a throwaway controller with the same plugin set and `CASC_JENKINS_CONFIG` pointing at the PR's YAML in CI;
fail the job if the log contains `ConfiguratorException`.

## Detecting drift
Export on a schedule and diff against git; any difference means configuration changed outside the YAML.

## Verify
The throwaway controller boots with the YAML and the Configuration as Code page shows the expected values.

## Checked

2026-10-28. Confirmed in the JCasC configExport and jsonSchema pages: export via /configuration-as-code/ Export configuration, not directly usable, what is and is not exported, encrypted secrets readable only on the same instance, unmasked free-form fields, schema at /configuration-as-code/schema, draft-07, beta status, SYSTEM_READ default and the allowAnonymousSchema property, no deep-nesting validation, ConfiguratorException on conflicting configuration. Removed: the export POST endpoint, check-jsonschema, yaml-language-server comment, checkNewSource endpoint, jenkins-plugin-cli and image names, and the log line claims.
Method: documentation only; no commands were run.

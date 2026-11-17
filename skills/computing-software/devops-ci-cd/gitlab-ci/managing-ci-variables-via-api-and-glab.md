---
id: computing-software.devops-ci-cd.gitlab-ci.managing-ci-variables-via-api-and-glab
name: managing-ci-variables-via-api-and-glab
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, variables-api, glab-variable, masked-hidden-variables, environment-scope-api]
level: practitioner
status: docs-checked
description: "Create, update and audit project, group and instance CI/CD variables with the REST API, including masked, hidden, protected, file, raw and environment-scoped values."
sources: ["https://docs.gitlab.com/api/project_level_variables/", "https://docs.gitlab.com/api/group_level_variables/", "https://docs.gitlab.com/api/instance_level_ci_variables/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managing CI/CD variables via API and glab

## 1. glab
The `glab variable` subcommands were not readable in the sources available for this review;
check `glab variable --help` for your version.

## 2. REST API
```bash
API="$CI_API_V4_URL/projects/$PID/variables"
curl --fail -H "PRIVATE-TOKEN: $T" -X POST "$API" \
  --form key=DB_PASSWORD --form value="$PW" --form masked=true --form protected=true \
  --form environment_scope=production --form raw=true
# update a scoped variable (same key can exist per scope)
curl -H "PRIVATE-TOKEN: $T" -X PUT "$API/DB_PASSWORD" --form value="$NEW" --form "filter[environment_scope]=production"
```
Create fields: `key` (up to 255 characters; A-Z, a-z, 0-9, `_`), `value`, `variable_type`
(`env_var` default, or `file`), `protected`, `masked`, `masked_and_hidden` (create only;
`hidden` and `masked_and_hidden` arrived in GitLab 17.4), `raw`, `environment_scope`
(default `*`), `description`. Group: `/groups/:id/variables`; instance: `/admin/ci/variables`.

## 3. Rules that bite
- `raw` defaults to `true` (value treated as a raw string); with `raw=false`, variables in the value are expanded, so a password containing `$` would change. Keep `raw=true` for secrets.
- A key can exist once per `environment_scope`. Creating a duplicate key in the same scope fails (`has already been taken`). To read, update or delete one of several same-key variables, pass `filter[environment_scope]`.
- `masked_and_hidden` can be set when creating a variable but is not an attribute of the update call.

## Verify
- [ ] `GET /projects/:id/variables` shows the expected flags and scopes; a job on an unprotected branch does not receive a protected variable.

## Checked

2026-10-31. Confirmed against the GitLab project-level, group-level and instance-level CI/CD variables API pages: endpoints, create and update attributes, defaults (`raw` true, `environment_scope` `*`, `variable_type` `env_var`), `filter[environment_scope]`, duplicate-key message, `masked_and_hidden`/`hidden` introduced in 17.4, key rules. Removed: all `glab variable` commands (the glab docs page returned nothing readable), masking length rules and 400/409 claims, the role requirement, and the claim that `raw` defaults to false (the API page says true).

Method: documentation only; no commands were run.

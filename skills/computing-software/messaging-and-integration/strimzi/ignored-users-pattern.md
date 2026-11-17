---
id: computing-software.messaging-and-integration.strimzi.ignored-users-pattern
name: ignored-users-pattern
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [strimzi-ignored-users-pattern, builtin-users, user-operator-ignore]
level: advanced
status: docs-checked
description: "Exclude built-in or externally managed users from the User Operator."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Ignoring specific users

**Goal:** stop the User Operator touching users it should not manage.

Typical exclusions are special built-in users such as `ANONYMOUS` or `*`, and internal users managed by other mechanisms. For ignored users the User Operator skips their ACLs, quotas and SCRAM-SHA credentials.

Set `STRIMZI_IGNORED_USERS_PATTERN` to a regular expression. To ignore `ANONYMOUS` or `*`, use `^\*|ANONYMOUS$`.

In the `Kafka` resource (note the double backslash for escaping):

```yaml
spec:
  entityOperator:
    template:
      userOperatorContainer:
        env:
          - name: STRIMZI_IGNORED_USERS_PATTERN
            value: "^\\*|ANONYMOUS$"
```

For a standalone User Operator, put the same `env` entry on the container named `strimzi-user-operator` in its Deployment.

The related recovery warning also applies: after restoring a deleted cluster, if the User Operator is enabled and users are not recreated, users are deleted from Kafka immediately.

**Checklist**

1. Write a regex that matches only intended principals.
2. Escape backslashes twice in YAML.
3. Apply the variable to the right Deployment or `Kafka` template.

## Checked

2026-11-03. Confirmed in the User Operator section: STRIMZI_IGNORED_USERS_PATTERN, the ANONYMOUS and * pattern, the doubled backslash, the strimzi-user-operator container, and the recovery warning.

Method: documentation only; no commands were run.

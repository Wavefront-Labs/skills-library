---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-auto-upgrade-flag-per-instance
name: awx-operator-auto-upgrade-flag-per-instance
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, auto-upgrade, staged-upgrade, multiple-instances, upgrade]
level: practitioner
status: docs-checked
description: "Control whether an operator upgrade updates each AWX instance by setting auto_upgrade, and upgrade held-back instances later."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/advanced-configuration/auto-upgrade.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator auto upgrade flag per instance

`auto_upgrade` (default true) decides how an operator upgrade affects an instance. True: the operator upgrades the instance directly. False with a running deployment: the operator will not update the AWX instance. This helps when several instances should be upgraded step by step instead of all at once.

```yaml
spec:
  auto_upgrade: false
```

Two ways to upgrade an instance marked `auto_upgrade: false`:
1. Change flags: set `auto_upgrade` to true on the AWX object, wait for that instance's upgrade to finish, then set it back to false.
2. Delete the deployment: `kubectl -n awx delete deployment <yourInstanceName>` and wait until the instance is redeployed.

## Checked

2026-11-04. Confirmed against the AWX Operator "Auto upgrade" page: parameter name and default, both behaviours, the multi-instance use, and both upgrade methods including the kubectl command. Removed the closing paragraph about the upgrade procedure (`DEFAULT_AWX_VERSION`, `make deploy`) and per-object flag claims, which are not on this page.
Method: documentation only; no commands were run.

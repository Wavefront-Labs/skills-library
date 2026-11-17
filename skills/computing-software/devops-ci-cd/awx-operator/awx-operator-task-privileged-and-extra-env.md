---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-task-privileged-and-extra-env
name: awx-operator-task-privileged-and-extra-env
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, extra-env, environment-variables, task-privileged, openshift, scc, rsyslog, ee]
level: practitioner
status: docs-checked
description: "Export custom environment variables into AWX containers and run the task pod privileged, with the OpenShift SCC grant that needs."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/advanced-configuration/exporting-environment-variables-to-containers.md", "https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/advanced-configuration/privileged-tasks.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator task privileged and extra env

Four spec fields add environment variables to containers (default empty string): `task_extra_env` (Task container), `web_extra_env` (Web container), `rsyslog_extra_env` (Rsyslog container) and `ee_extra_env` (EE container).

```yaml
spec:
  task_extra_env:
    - name: MYCUSTOMVAR
      value: foo
  web_extra_env:
    - name: MYCUSTOMVAR
      value: foo
  rsyslog_extra_env:
    - name: MYCUSTOMVAR
      value: foo
  ee_extra_env:
    - name: MYCUSTOMVAR
      value: foo
```

`ee_extra_env` only takes effect for the globally available Execution Environments. For a custom EE, customize the Pod spec.

## Privileged task pod

Some tasks may need the task pod to run as privileged. This can open security concerns, so be aware of them and verify you have the privileges to do it. Enable it:

```yaml
spec:
  task_privileged: true
```

On OpenShift also grant the `awx` ServiceAccount the privileged SCC:

```sh
oc adm policy add-scc-to-user privileged -z awx
```

This is the most relaxed SCC OpenShift provides, so familiarize yourself with the security concerns first.

## Checked

2026-11-04. Confirmed against the AWX Operator pages "Exporting Environment Variables to Containers" and "Privileged Tasks": field names, container mapping, defaults, the ee_extra_env warning, `task_privileged`, and the SCC command. Removed the extra-settings `AWX_TASK_ENV` aside and the `ee_extra_volume_mounts` reference (not on these pages) and changed the example from block scalars to the plain lists the page shows.
Method: documentation only; no commands were run.

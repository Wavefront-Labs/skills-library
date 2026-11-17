---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-extra-settings-and-extra-settings-files
name: awx-operator-extra-settings-and-extra-settings-files
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, extra-settings, settings-py, configmap, secret, conf-d, read-only-settings]
level: advanced
status: docs-checked
description: "Pass custom AWX settings via extra_settings (appended to settings.py) or extra_settings_files from ConfigMaps and Secrets, with the key restrictions."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/advanced-configuration/extra-settings.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator extra settings and extra settings files

Settings set this way become read-only in AWX and cannot be changed in the UI after deployment. Change them in the AWX CR spec (`extra_settings`) or in the ConfigMap or Secret (`extra_settings_files`); after updating a ConfigMap or Secret, restart the AWX pods. If a setting is in both, `extra_settings_files` wins.

`extra_settings` (default `[]`) is appended to `/etc/tower/settings.py`:

```yaml
spec:
  extra_settings:
    - setting: MAX_PAGE_SIZE
      value: "500"
    - setting: LOG_AGGREGATOR_LEVEL
      value: "'DEBUG'"
```

Some values, like `LOG_AGGREGATOR_LEVEL`, need inner quotes.

`extra_settings_files` mounts `*.py` files under `/etc/tower/conf.d`. Create ConfigMaps or Secrets containing the `*.py` settings files (`kubectl create configmap my-custom-settings --from-file <path>`, `kubectl create secret generic my-custom-passwords --from-file <path>`) and reference them:

```yaml
spec:
  extra_settings_files:
    configmaps:
      - name: my-custom-settings
        key: custom_job_settings.py
    secrets:
      - name: my-custom-passwords
        key: custom_passwords.py
```

The page's example files set `AWX_TASK_ENV` (proxy variables), `GALAXY_TASK_ENV`, `REMOTE_HOST_HEADERS` and credentials-type settings. Restrictions: keys must be python filenames ending in `.py` with only alphanumerics, `-`, `_` or `.`; keys are converted to `<instance name>-<KEY>-configmap` (ConfigMaps) or `<instance name>-<KEY>-secret` (Secrets), which must not exceed 63 characters; `credentials.py`, `execution_environments.py` and `ldap.py` are reserved. If the same setting is in several files, which one wins is hard to predict because files load in the arbitrary order glob returns, so do not repeat a key across files.

## Checked

2026-11-04. Confirmed against the AWX Operator "Extra Settings" page: read-only behaviour, precedence, `/etc/tower/settings.py` and `/etc/tower/conf.d` targets, defaults (`[]`, `{}`), example settings, the quoting note, and all key restrictions. Reworded the restart and restriction text to match the page; nothing material removed.
Method: documentation only; no commands were run.

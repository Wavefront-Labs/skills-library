---
id: computing-software.data-engineering.apache-airflow.fernet-key-encryption-and-rotation
name: fernet-key-encryption-and-rotation
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, fernet-key, encryption, rotate-fernet-key, connections, variables, secrets]
level: practitioner
status: docs-checked
description: "Set and rotate Airflow's Fernet key that encrypts connection passwords and variables in the metadata DB, using comma-separated keys and airflow rotate-fernet-key."
sources:
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/security/secrets/fernet.rst
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/howto/set-config.rst
  - https://github.com/apache/airflow/blob/main/chart/values.yaml
  - https://github.com/apache/airflow/blob/main/airflow-core/src/airflow/models/crypto.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fernet key encryption and rotation

**Goal:** connection passwords/extras and variable values stored in the metadata database are encrypted, and the key can be rotated without breaking them.

## Generate and set
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```
```bash
export AIRFLOW__CORE__FERNET_KEY='<key>'          # or [core] fernet_key; the env var overrides airflow.cfg
```
The first time Airflow starts, the generated `airflow.cfg` contains a unique key in `[core] fernet_key`. The `_cmd` and `_secret` suffixes also work for config options. In the Helm chart, `fernetKey` can only be set at `helm install`, and `fernetKeySecretName` names a Secret whose `fernet-key` entry holds the base64-encoded key. Every component that reads connections or variables needs the same key.

## Rotate
1. Generate a new key.
2. Set `fernet_key` to `new_key,old_key` (new first).
3. Re-encrypt existing credentials:
```bash
airflow rotate-fernet-key
```
4. Set `fernet_key` to `new_key` only.

## What is covered
- Connection passwords and extras, Variable values and trigger kwargs are encrypted in the database (the connection and variable tables carry an `is_encrypted` flag).
- Changing the key without the old one in the list makes decryption of existing credentials fail.

## Failure symptoms
- Existing credentials fail to decrypt after a key change: put the old key back in the list after the new one, run `airflow rotate-fernet-key`, then drop the old key.
## Recommendations
- Keep the key in a secured place; it can be supplied through `AIRFLOW__CORE__FERNET_KEY_CMD` or `AIRFLOW__CORE__FERNET_KEY_SECRET` instead of a plain value.
- Rotate per your security policy and document it in the runbook.

## Verify
- [ ] An existing connection still resolves on every component after rotation.
- [ ] `is_encrypted` is true for rows with passwords in the `connection` table.

## Checked

2026-10-25: Airflow documentation source on the apache/airflow main branch (airflow-core/docs, task-sdk and providers/standard), latest commit 2026-10-24. Confirmed: key generation snippet, `[core] fernet_key` and the env var override, the three-step rotation with `airflow rotate-fernet-key`, the `_cmd` and `_secret` config suffixes (set-config.rst), Helm `fernetKey` and `fernetKeySecretName` (chart values.yaml), and that connection, variable and trigger data carry encryption (models source with the `is_encrypted` column). Removed the plain-text-if-unset claim, the restart steps, the InvalidToken symptom text and the list of not-covered stores, which the docs do not state.

Method: documentation only; no commands were run.

---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-admin-user-and-secret-key-secrets
name: awx-operator-admin-user-and-secret-key-secrets
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, admin-user, admin-password-secret, secret-key-secret, encryption, secrets]
level: practitioner
status: docs-checked
description: "Configure the AWX admin account and the symmetric secret key through Kubernetes Secrets, with the operator's default naming and generation."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/admin-user-account-configuration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator admin user and secret key secrets

Admin variables: `admin_user` (default `admin`), `admin_email` (default `test@example.com`) and `admin_password_secret` (a Kubernetes Secret name, never the clear text password).

If `admin_password_secret` is unset, the operator looks for `<resourcename>-admin-password`; if missing it generates a password and creates that Secret. Retrieve it:

```sh
kubectl get secret <resourcename>-admin-password -o jsonpath="{.data.password}" | base64 --decode ; echo
```

Custom Secret shape:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: <resourcename>-admin-password
stringData:
  password: mysuperlongpassword
```

Secret key: `secret_key_secret` names a Secret containing the symmetric key used to encrypt sensitive data in the database (default: generated). It must be a Kubernetes Secret, not the clear value. If unset the operator looks for `<resourcename>-secret-key` and generates it if absent. Do not delete this Secret: it is needed for upgrades and if the pods get scaled down. With a GitOps flow, pass a secret key secret.

```yaml
stringData:
  secret_key: supersecuresecretkey
```

```yaml
spec:
  secret_key_secret: custom-awx-secret-key
```

## Checked

2026-11-04. Confirmed against the AWX Operator "Admin user account configuration" page: variable names and defaults, lookup and generation of `<resourcename>-admin-password` and `<resourcename>-secret-key`, the retrieval command, and both Secret shapes. Removed the claim that the key is needed to recover or restore, and the migration-docs reference (not on this page); added the page's statements about not deleting the key and GitOps.
Method: documentation only; no commands were run.

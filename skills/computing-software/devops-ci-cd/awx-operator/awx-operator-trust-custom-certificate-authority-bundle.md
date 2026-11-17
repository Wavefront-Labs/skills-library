---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-trust-custom-certificate-authority-bundle
name: awx-operator-trust-custom-certificate-authority-bundle
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, custom-ca, bundle-cacert-secret, ldap-cacert-secret, tls, internal-git]
level: practitioner
status: docs-checked
description: "Trust an internal Certificate Authority in AWX through bundle_cacert_secret so projects can clone over HTTPS from internal servers."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/advanced-configuration/trusting-a-custom-certificate-authority.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator trust custom certificate authority bundle

Trusting a custom CA lets AWX access network services with locally issued SSL certificates, such as cloning a project from an internal Git server via HTTPS. A common symptom is the error `unable to verify the first certificate`.

Variables (all default to an empty string): `bundle_cacert_secret` (Certificate Authority secret name), and the deprecated `ldap_cacert_secret` (LDAP CA secret name) and `ldap_password_secret` (LDAP BIND DN password secret name). The operator looks for the data field `bundle-ca.crt` in the secret for `bundle_cacert_secret`, and `ldap-ca.crt` for `ldap_cacert_secret`.

```yaml
spec:
  ldap_cacert_secret: <resourcename>-custom-certs
  ldap_password_secret: <resourcename>-ldap-password
  bundle_cacert_secret: <resourcename>-custom-certs
```

Create the secret with a kustomization.yaml file:

```yaml
secretGenerator:
  - name: <resourcename>-custom-certs
    files:
      - bundle-ca.crt=<path+filename>
    options:
      disableNameSuffixHash: true
```

or with the CLI:

```sh
kubectl create secret generic <resourcename>-custom-certs \
  --from-file=ldap-ca.crt=<PATH/TO/YOUR/CA/PEM/FILE> \
  --from-file=bundle-ca.crt=<PATH/TO/YOUR/CA/PEM/FILE>
kubectl create secret generic <resourcename>-ldap-password \
  --from-literal=ldap-password=<your_ldap_dn_password>
```

## Checked

2026-11-04. Confirmed against the AWX Operator "Trusting a Custom Certificate Authority" page: variable names, defaults, deprecation marks, data field names, the example spec, and both secret-creation methods. Removed the explanation of the name hash suffix and the closing paragraph, which restated the table.
Method: documentation only; no commands were run.

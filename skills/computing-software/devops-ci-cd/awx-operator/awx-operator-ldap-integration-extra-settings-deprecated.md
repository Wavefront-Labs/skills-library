---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-ldap-integration-extra-settings-deprecated
name: awx-operator-ldap-integration-extra-settings-deprecated
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, ldap, django-auth-ldap, extra-settings-files, auth-ldap, deprecated]
level: advanced
status: docs-checked
description: "Configure the deprecated bootstrap LDAP integration through AWX settings supplied as a ConfigMap, Secret or extra_settings values."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/advanced-configuration/enabling-ldap-integration-at-awx-bootstrap.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator ldap integration extra settings deprecated

LDAP at bootstrap is marked deprecated. It uses django-auth-ldap settings, supplied through extra settings.

Via `extra_settings_files`: create a python file (for example `custom_ldap_settings.py`) with settings such as:

```python
AUTH_LDAP_SERVER_URI = "ldaps://ad01.abc.com:636 ldaps://ad02.abc.com:636"
AUTH_LDAP_BIND_DN = "CN=LDAP User,OU=Service Accounts,DC=abc,DC=com"
AUTH_LDAP_USER_SEARCH = LDAPSearch("DC=abc,DC=com", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)")
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()
AUTH_LDAP_REQUIRE_GROUP = "CN=operators,OU=Groups,DC=abc,DC=com"
AUTH_LDAP_USER_FLAGS_BY_GROUP = {"is_superuser": ["CN=admin,OU=Groups,DC=abc,DC=com"]}
```

plus user attribute, group search, organization and team maps. Create a ConfigMap from it and reference it:

```yaml
spec:
  extra_settings_files:
    configmaps:
      - name: custom-ldap-settings
        key: custom_ldap_settings.py
```

If the file holds secrets such as passwords, create a Secret instead and list it under `extra_settings_files.secrets`.

Via `extra_settings`: the values are inserted into a Python file, so quoting matters. Plain strings need inner quotes (`value: >-` with `"ldaps://..."`), while expressions like `LDAPSearch(...)`, `GroupOfNamesType()` and dicts are unquoted.

To trust a custom CA for the LDAP server or pass a bind DN password, use the custom certificate authority secrets.

## Checked

2026-11-09. Confirmed the deprecation, the sample settings, the extra_settings_files ConfigMap and Secret forms, the quoting note for extra_settings and the custom CA tip against the AWX Operator LDAP bootstrap page (read in full).

Method: docs-checked 2026-11-09 against the AWX Operator docs page docs/user-guide/advanced-configuration/enabling-ldap-integration-at-awx-bootstrap.md

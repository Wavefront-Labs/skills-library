---
id: computing-software.systems-network-administration.netbox.ldap-authentication
name: ldap-authentication
category: computing-software
field: systems-network-administration
product: netbox
tags: [ldap, django-auth-ldap, active-directory]
level: advanced
status: docs-checked
description: "Enable the LDAP backend with ldap_config.py, search settings and group mapping."
sources: ["https://netboxlabs.com/docs/netbox/installation/6-ldap/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LDAP authentication

Goal: authenticate users against LDAP or Active Directory.

User authentication falls back to built-in Django users if the server fails.

**Install**
```
sudo apt install -y libldap2-dev libsasl2-dev libssl-dev
source /opt/netbox/venv/bin/activate
pip3 install django-auth-ldap
sudo sh -c "echo 'django-auth-ldap' >> /opt/netbox/local_requirements.txt"
```
For the Python package install use the `netbox[ldap]==X.Y.Z` extra.

**Configure.** In `configuration.py` set `REMOTE_AUTH_BACKEND = 'netbox.authentication.LDAPBackend'` (overwriting `RemoteUserBackend` if set). Create `ldap_config.py` beside `configuration.py`.

**Key settings**

- `AUTH_LDAP_SERVER_URI`, `AUTH_LDAP_BIND_DN`, `AUTH_LDAP_BIND_PASSWORD`.
- Certificates: `LDAP_IGNORE_CERT_ERRORS`, `LDAP_CA_CERT_DIR`, `LDAP_CA_CERT_FILE`. STARTTLS uses `AUTH_LDAP_START_TLS = True` with an `ldap://` URI.
- Active Directory forests: use port 3269 (secure) or 3268 for the Global Catalog.
- Users: `AUTH_LDAP_USER_SEARCH` (for example `sAMAccountName=%(user)s`) or `AUTH_LDAP_USER_DN_TEMPLATE` (set to `None` on Windows Server 2012+), and `AUTH_LDAP_USER_ATTR_MAP`.
- Groups: `AUTH_LDAP_GROUP_SEARCH`, `AUTH_LDAP_GROUP_TYPE` (use `NestedGroupOfNamesType()` for nested AD groups), `AUTH_LDAP_REQUIRE_GROUP`.

Restart the NetBox services after editing `ldap_config.py`. For a Python package install, the file lives in `/opt/netbox/conf/` and should be `chown root:netbox` with mode `640` so the service account can read the bind password.

**Checklist**

1. Backend set.
2. Bind account tested.
3. Group requirement set.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: LDAP installation page: django-auth-ldap packages, LDAPBackend setting, ldap_config.py parameters, STARTTLS, AD ports 3268/3269, NestedGroupOfNamesType, file permissions note. Removed: Nothing.

Method: documentation only; no commands were run.

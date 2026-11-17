---
id: computing-software.cloud-infrastructure-engineering.rancher.auth-openldap-bind-account-and-test
name: auth-openldap-bind-account-and-test
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [openldap, ldap, bind-account, service-account, principal, test-authentication]
level: practitioner
status: docs-checked
description: "Set up Rancher OpenLDAP authentication: read-only bind account, TLS CA in PEM, the Auth Provider form, and the test login mapping."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/authentication-permissions-and-global-configuration/configure-openldap
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rancher needs an LDAP **bind account** (service account) to search and retrieve the users and groups that should have access. The page recommends not using an administrator or personal account: create a dedicated OpenLDAP account with read-only access to users and groups under the search base. If the server's certificate is self-signed or from an unrecognised CA, have the CA certificate, concatenated with any intermediates, in PEM format to paste into the form.

Before starting, read the page's concept section on External Authentication Configuration and Principal Users.

Steps:

1. Open **Users & Authentication > Auth Provider** and choose **OpenLDAP**.
2. Fill in **Configure an OpenLDAP server** (server, groups, users); field-by-field help is in the separate configuration reference page.
3. Click **Enable**.
4. Test authentication with a username and password.

The test step has consequences. The OpenLDAP user whose credentials you enter is **mapped to the local principal account and given administrator privileges** in Rancher, so choose that account deliberately. Authentication with OpenLDAP is enabled implicitly when the test succeeds. The page adds that you will still be able to use the local principal afterwards.

## Checked

2026-11-09. Read the cited Configuring OpenLDAP page in full and checked every claim against it (bind account advice, PEM CA, form steps, test authentication and local principal mapping, local admin fallback). No claims removed.

Method: documentation only; no commands were run.

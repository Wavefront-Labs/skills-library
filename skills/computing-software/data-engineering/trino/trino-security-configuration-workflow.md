---
id: computing-software.data-engineering.trino.trino-security-configuration-workflow
name: trino-security-configuration-workflow
category: computing-software
field: data-engineering
product: trino
tags: [security-overview, security-workflow, hide-inaccessible-columns, authentication-providers, access-control-options]
level: practitioner
status: docs-checked
description: "Trino security checklist in order (TLS, shared secret, authentication, authorization), providers and hiding inaccessible columns."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/security/overview.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino security configuration workflow

A default Trino installation has no security enabled. Security applies to client access, to traffic inside the cluster and to catalogs reaching data sources. The docs prescribe this order and say not to skip or combine steps:
1. Enable TLS/HTTPS, working with your security team, ideally terminating at a load balancer or proxy with a globally trusted certificate. Verify.
2. Configure a shared secret for internal communication. Verify.
3. Enable authentication: start with password file authentication, then move to your real provider such as LDAP. Avoid Kerberos for client authentication if possible. Verify.
4. Enable authorization: start with file-based rules, then another method as needed. Verify.
Change one thing at a time, restart the server after each change and verify before continuing.

All access goes through the coordinator, so securing clients means securing the coordinator across encryption, authentication and access control. Providers: password file, LDAP, Salesforce, OAuth 2.0, certificate, JWT, Kerberos. User mapping (regex rules turning `alice@example.com` into `alice`) applies to all of them; group mapping assigns usernames to groups.

The default access control allows all operations to authenticated users. Alternatives: file-based JSON rules at catalog, schema or table level, Open Policy Agent, Apache Ranger (row filters, column masking, audit logs) or a custom implementation through the system access control API.

When column access is limited, `SELECT *` fails by default if some columns are inaccessible. Set the global property `hide-inaccessible-columns = true` in the Trino config properties to hide them silently. Secrets in catalog files can use secrets management, and each connector has its own data-source security options.

## Checked

2026-11-09: confirmed against the Trino security overview page (docs/src/main/sphinx/security/overview.md): the four-step workflow order and its rule not to skip or combine steps, the list of authentication providers, user and group mapping, the default access control, the file-based, Open Policy Agent and Apache Ranger options, the custom access control API, and the `hide-inaccessible-columns` property. Removed the claim that the property lives in a file literally named config.properties (the page only links it to the config properties section).

Method: documentation only; no commands were run.

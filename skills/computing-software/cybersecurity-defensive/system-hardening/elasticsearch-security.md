---
id: computing-software.cybersecurity-defensive.system-hardening.elasticsearch-security
name: elasticsearch-security
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [elasticsearch-security, opensearch, database-hardening, tls, rbac, api-keys, exposed-database]
level: practitioner
status: docs-checked
description: "Secure Elasticsearch and OpenSearch clusters: security features on, TLS on transport and HTTP, built-in user passwords, roles and API keys, keystore secrets, audit logging."
sources: ["https://www.elastic.co/docs/deploy-manage/security", "https://www.elastic.co/docs/deploy-manage/security/set-up-minimal-security", "https://docs.opensearch.org/latest/security/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Elasticsearch security

Unauthenticated, internet-facing search clusters are a common source of large data leaks. In Elasticsearch 8.0 and
later, security is enabled automatically when Elasticsearch starts for the first time; older clusters and many
OpenSearch deployments need it configured.

## Enable and configure
- Enable the Elasticsearch security features first, then configure them; if you want your own TLS certificates,
  configure security manually.
- Set built-in user passwords with `elasticsearch-reset-password -u elastic` (auto-generated; `-i` for interactive)
  and `elasticsearch-reset-password -u kibana_system`. The `kibana_system` account is not for people to log in with.
- Put sensitive settings (passwords) in the Elasticsearch or Kibana keystore; file permissions alone are not
  enough. For Kibana, `kibana-keystore add elasticsearch.password` stores the `kibana_system` password.
- Multi-node clusters must configure TLS between nodes (transport); production-mode clusters will not start without
  it. Securing the HTTP layer with TLS is highly recommended for every cluster, including single-node ones.
- Elastic Cloud deployment types configure security automatically and do not support disabling it.

## Access control
- Use the `elastic` superuser only to bootstrap (manage spaces, create users, assign roles); give applications and
  people their own users, roles or SSO.
- Use API keys for programmatic access, and manage (revoke) them when unused.
- Kibana: use spaces and roles, and reach it only over HTTPS.

## Logging and monitoring
Security event audit logging gives visibility into authentication attempts, authorization decisions and other
activity; it is configurable on self-managed clusters (check your licence tier). Ship logs off the cluster and alert
on authentication failures.

## OpenSearch
The security plugin encrypts data in transit with TLS for both client-to-node (REST) and node-to-node (transport)
traffic, supports authentication by username/password, JSON web token or TLS certificate, configurable audit and
compliance logging, roles, and Dashboards multi-tenancy. Check the OpenSearch security configuration pages for
file names and for how to replace demo credentials; do not use demo configuration in production.

## Network
Allow the HTTP and transport ports only from application hosts and cluster members, with no public IPs, and review
cloud security groups.

## Verify
An unauthenticated request from outside fails; the app credential shows only its own role; an external scan shows
no cluster ports open.

## Checked
2026-10-31. Confirmed on the Elastic security overview, minimal-security and OpenSearch security pages: auto security
from 8.0, manual configuration for own certificates, `elasticsearch-reset-password` (-u, -i) and `kibana_system`,
keystore use, `kibana-keystore add elasticsearch.password`, transport TLS requirement for multi-node, HTTP TLS
recommendation, Elastic Cloud defaults, API keys, audit logging, OpenSearch TLS layers, authentication types, audit
and multi-tenancy. Removed as not confirmed on those pages: the `xpack.security.*` settings and file names,
`elasticsearch-certutil` usage, port numbers 9200/9300, role JSON and API-key request example, `script.allowed_types`,
`install_demo_configuration.sh` and `internal_users.yml` specifics, and snapshot encryption remarks.
Method: documentation only; no commands were run.

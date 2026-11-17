---
id: computing-software.messaging-and-integration.apache-pulsar.authorization-roles-and-proxy-roles
name: authorization-roles-and-proxy-roles
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [authorization, super-user-roles, proxy-roles, tenants-create, admin-roles, authenticate-original-auth-data]
level: practitioner
status: docs-checked
description: "Turn on Pulsar authorization with superUserRoles, create tenants with admin roles, and authorize both the proxy role and the original principal behind a proxy."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/security-authorization.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control what authenticated roles may do, including requests that arrive through the Pulsar proxy.

Authentication only identifies a role; without authorization any authenticated role can do anything. Enable it in `broker.conf` (or `standalone.conf`):
```conf
authorizationEnabled=true
superUserRoles=broker_client,admin,proxy,<custom-super-user-1>
```
Superusers can create and destroy tenants and have full access to tenant resources. With geo-replication every broker needs rights to publish to the other clusters' topics, so brokers authenticate as a superuser role. Authorization can also be enabled in `proxy.conf`, which adds a check before forwarding.

Tenants: a superuser creates a tenant and assigns an admin role:
```shell
bin/pulsar-admin tenants create my-tenant --admin-roles my-admin-role --allowed-clusters us-west,us-east
```
A client with `my-admin-role` can then manage namespaces and grant permissions in that tenant.

Proxy roles: list them in the broker as `proxyRoles=proxy,<my-proxy-role>`. If a proxy is not configured with a role in `proxyRoles`, its connection is rejected. Both the proxy role and the original principal must be authorized for a resource. Safer approach: grant the proxy role access each time you grant a resource, for example by also naming it as an admin role of the tenant. The other approach makes the proxy role a superuser, with requests still downgraded to the client role.

Credential forwarding: brokers default to `authenticateOriginalAuthData=true` and authenticate forwarded credentials. For replayable credentials such as tokens set `forwardAuthorizationCredentials=true` on the proxy. Gotcha: with TLS client-certificate authentication or SASL through a proxy, set `authenticateOriginalAuthData=false` in broker.conf, since the broker sees the proxy's certificate and SASL cannot be replayed.

Tenant administration through a proxy requires both the proxy role and the original principal to be superuser or tenant admin.

## Checked

2026-11-03. Confirmed against the pulsar-site page security-authorization: superuser and admin-role behaviour, the broker.conf settings, tenant creation command, proxy-role approaches, credential forwarding and proxied tenant administration. Removed the invented Verify step.

Method: documentation only; no commands were run.

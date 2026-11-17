---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.multitenancy
name: multitenancy
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-styles, multitenancy, multi-tenant-saas, tenant-isolation, silo-pool-bridge, row-level-security, noisy-neighbour, tenant-context, saas-architecture]
level: advanced
status: docs-checked
description: "Multitenant SaaS design: what a tenant is, where to find vendor isolation guidance, and PostgreSQL row-level security rules (default deny, owner bypass, BYPASSRLS, FORCE)."
sources: ["https://learn.microsoft.com/azure/architecture/guide/multitenant/overview", "https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/saas-lens.html", "https://www.postgresql.org/docs/current/ddl-rowsecurity.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multitenant SaaS architecture

## Definitions and where the guidance lives
- Microsoft: a multitenant solution is used by multiple customers, or tenants; tenants are distinct from
  users (many users of one organisation form a single tenant). Examples: B2B SaaS, B2C services, and
  shared platforms such as a Kubernetes cluster used by several business units. A Microsoft Entra
  tenant is a different concept from your tenants.
- Microsoft's series has three parts: architectural considerations, architectural approaches (compute,
  networking, storage, data, messaging, identity, deployment, governance, compliance, cost
  management) and service-specific guidance describing the tenancy isolation models per Azure service,
  plus a checklist. Read it with the Azure Well-Architected Framework.
- AWS publishes a SaaS Lens for the Well-Architected Framework (April 2023) in the Well-Architected
  Tool lens catalogue, for designing multi-tenant SaaS workloads.
- The cited landing pages do not define silo, pool or bridge models or give cost-per-tenant methods;
  take those from the service-specific pages before relying on them.

## Data isolation with PostgreSQL row-level security
These facts are from the PostgreSQL documentation (section "Row Security Policies"):
1. Tables have no policies by default; once row security is enabled with
   `ALTER TABLE ... ENABLE ROW LEVEL SECURITY`, all access must be allowed by a policy, and with no
   policy a default-deny policy applies.
2. Superusers and roles with the `BYPASSRLS` attribute always bypass row security. Table owners
   normally bypass it too, unless the table is altered with `FORCE ROW LEVEL SECURITY`. Only the table
   owner can enable row security or add policies.
3. Policies are created with `CREATE POLICY`; a `USING` expression selects visible rows and, absent a
   `WITH CHECK` clause, also constrains modified rows. Permissive policies combine with OR, restrictive
   ones with AND.
4. Referential integrity checks (unique, primary key, foreign key) always bypass row security, so design
   policies and schemas to avoid covert-channel leaks through them. `TRUNCATE` and `REFERENCES` are not subject to row security.

## Verify
- [ ] The application's database role is neither the table owner (or the table uses `FORCE ROW LEVEL SECURITY`)
  nor a `BYPASSRLS` role.
- [ ] A test as a user of tenant A requesting tenant B's rows returns nothing, for every API.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed: the PostgreSQL row security page (all points above), the Microsoft multitenant overview
(definitions and series structure) and the AWS SaaS Lens landing page. Removed as not stated on the cited
pages: the silo/pool/bridge comparison table, token-claim tenant context, DynamoDB leading-key conditions,
session-tag ABAC, per-tenant encryption keys, noisy-neighbour controls, onboarding and offboarding steps,
and cost apportioning.

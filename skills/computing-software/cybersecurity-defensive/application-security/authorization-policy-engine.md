---
id: computing-software.cybersecurity-defensive.application-security.authorization-policy-engine
name: authorization-policy-engine
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [authorization-policy-engine, open-policy-agent, rego, cedar, openfga, rebac, abac, policy-as-code]
level: advanced
status: docs-checked
description: "Externalise app authorisation to a policy engine (OPA/Rego, Cedar, OpenFGA): choose RBAC, ABAC or ReBAC, deny by default, check every request, test the permissions."
sources: ["https://www.openpolicyagent.org/docs/latest/", "https://docs.cedarpolicy.com/", "https://openfga.dev/docs/concepts", "https://raw.githubusercontent.com/OWASP/CheatSheetSeries/master/cheatsheets/Authorization_Cheat_Sheet.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authorisation policy engines

A policy engine separates the decision from the enforcement: your software asks the engine
"is this request authorized?" and acts on the answer.

## Choose a model (OWASP Authorization Cheat Sheet)
- RBAC grants access by role. ABAC decides from attributes of the subject, object and
  environment plus policies written over them (NIST SP 800-162). ReBAC grants access from
  relationships between resources, for example only the creator of a post can edit it.
- The cheat sheet says ABAC and ReBAC should typically be preferred over RBAC for application
  development: finer-grained Boolean logic, fewer missed role checks, no role explosion,
  better multi-tenant and cross-organisation fit, and separation of policy from enforcement.
- Decide early; it affects the whole SDLC.

## Engines
- **Open Policy Agent**: open source, general-purpose, a CNCF graduated project. It decouples
  policy decision from enforcement: software queries OPA with structured data (for example
  JSON) as input, and policies are written in Rego, which is domain-agnostic. Uses named in
  the docs include microservices, Kubernetes, CI/CD pipelines and API gateways. Decisions can
  be arbitrary structured data, not just allow or deny. Run it as a server
  (`opa run --server`), evaluate from the CLI (`opa eval`), or embed it in Go as a library.
- **Cedar**: a language for authorization policies. A policy says who (principal) may do which
  actions on which resources in what context. Entities are the application data Cedar needs,
  supplied with the request together with the policies. A schema defines entity types and
  validates policies when you create or update them; Cedar does not use the schema when
  evaluating a request. It supports RBAC and ABAC use cases. Amazon Verified Permissions is a
  managed service using Cedar.
- **OpenFGA**: answers authorization checks by determining whether a relationship exists
  between a user and an object, from an authorization model plus relationship tuples (user,
  relation, object), for example `user:anne` as `editor` of `document:new-roadmap`. Tuples can
  carry a condition written in CEL. A store holds model versions and tuples; separate stores
  can serve separate environments, and store data cannot be shared across stores.

## Enforcement rules (OWASP Authorization Cheat Sheet)
- Deny by default: the application must always decide to permit or deny, and you should be able
  to justify why each permission was granted. Prefer explicit configuration over framework
  defaults.
- Validate permissions on every request, whatever its origin, with a global application-wide
  mechanism (filters or middleware) instead of per-method checks.
- Handle authorization failures securely and centralise that handling; failures must not leave
  the software in a state that allows bypass.
- Do not depend on a single framework or library for access control; assume any third-party
  component could have an authorization vulnerability, and test its configuration.
- Write tests that validate the permissions mapped out in design, and review periodically for
  privilege creep.
- Ensure lookup IDs cannot be used even when guessed or tampered with.

## Verify
- [ ] Every endpoint maps to an action and resource that the engine is asked about.
- [ ] Tests cover allowed and denied cases for each action.
- [ ] A failed or absent decision results in denial.

## Checked
Confirmed 2026-11-09 against the OPA docs landing page, the Cedar guide home page, the OpenFGA concepts page and the OWASP Authorization Cheat Sheet (raw markdown, design principles and model sections).
Removed as unconfirmed: the Rego, Cedar and FGA policy examples, SpiceDB, PDP sidecar and WASM placement, OPA partial evaluation, ListObjects, bundles and decision logs, the test commands (opa test, fga model test, cedar authorize), CODEOWNERS, and the specific pitfalls list.
Method: docs-checked 2026-11-09 against openpolicyagent.org docs, docs.cedarpolicy.com, openfga.dev concepts and the OWASP Authorization Cheat Sheet on raw.githubusercontent.com

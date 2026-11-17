---
id: computing-software.cybersecurity-defensive.keycloak.organization-domains-and-routing
name: organization-domains-and-routing
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, organizations, domains, idp-routing, email-domain]
level: practitioner
status: docs-checked
description: "Use Keycloak organization domains to match users by email domain, route them to the organization identity provider and block foreign domains."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/organizations/managing-domains.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# organization domains and routing
Domains identify the organizations a user belongs to by email address. Keycloak matches the user's email domain to an organization and can change the authentication flow to meet its requirements. Domains are first-class entities with their own configuration: identity provider routing and auto-redirect. They also let an organization enforce that members use only email domains associated with it, which is useful when identities are federated from the organization's identity provider.

Assignment: open the organization, *Domains* tab, add domains (zero, one or many). With none, members are not validated against domain restrictions and email-based redirection to identity providers is unavailable, though auto-membership through a linked identity provider still works.

Domain types: *Exact* (`example.com` matches `user@example.com` but not `user@sub.example.com`) and *Wildcard* (`*.example.com` matches the base domain and all subdomains at any depth).

Matching: the email domain is lowercased and the most specific match wins, measured by number of domain parts; with equal parts an exact match wins over a wildcard. The same rules decide the `domain` reported in token claims from the organization membership mapper.

Routing (organization > *Domains* > select a domain, *Edit*): *Identity provider* (one linked to the organization, or None, in which case users see the standard login form) and *Auto redirect* (redirect users with a matching email domain straight to the provider; no effect without a provider; users with first-factor credentials such as a password are not auto-redirected but asked to authenticate). The same provider can be the routing target for domains of several organizations; the post-broker membership domain gate only adds a user to organizations whose domains match their email.

Validation rules: a domain cannot be shared across organizations in a realm, domains are stored and compared lowercase, and wildcards need at least 2 parts after `*.` (`*.com` is rejected).

## Checked
2026-11-03. Confirmed against server_admin/topics/organizations/managing-domains.adoc. Removed: the "confirm for your version" wildcard hedge, the claim that changing a domain does not move members, and the invented Verify step.
Method: documentation only; no commands were run.

---
id: computing-software.cybersecurity-defensive.zitadel.oidc-reserved-scopes
name: oidc-reserved-scopes
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, oidc, scopes, audience, roles, organization-scope]
level: advanced
status: docs-checked
description: "Use ZITADEL's reserved scopes to request roles, restrict login to an organization, add audiences, return metadata or jump to an identity provider."
sources:
  - https://zitadel.com/docs/apis/openidoauth/scopes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Besides the standard scopes (`openid` mandatory, `profile`, `email`, `address`, `phone`, and `offline_access` for a refresh token with the code flow), ZITADEL defines reserved scopes.

- `urn:zitadel:iam:org:project:role:{rolekey}`: asserts the claim `urn:zitadel:iam:org:project:roles` for that role when possible.
- `urn:zitadel:iam:org:projects:roles`: asserts `urn:zitadel:iam:org:project:{projectid}:roles` for each requested project.
- `urn:zitadel:iam:org:id:{id}`: enforces that the user belongs to that organization; a missing organization produces a failure.
- `urn:zitadel:iam:org:domain:primary:{domainname}`: enforces membership of the organization and a username suffixed with the domain.
- `urn:zitadel:iam:org:roles:id:{orgID}`: limits returned roles to the given organization IDs; unknown IDs are ignored.
- `urn:zitadel:iam:org:project:id:{projectid}:aud`: adds the project to the access token audience.
- `urn:zitadel:iam:org:project:id:zitadel:aud`: adds the ZITADEL project to the audience, needed to call ZITADEL APIs.
- `urn:zitadel:iam:user:metadata`: includes base64 encoded metadata.
- `urn:zitadel:iam:user:resourceowner`: includes id, name and primary domain of the user's organization.
- `urn:zitadel:iam:org:idp:id:{idp_id}`: sends the user straight to that identity provider.

Combine the IdP scope with the organization domain scope when that organization has a custom login policy.

## Checked

2026-11-08. Confirmed against the Scopes page (source mdx in the zitadel repo): the standard scope table and every reserved scope listed, including role, projects roles, org id, org domain, roles id filter, project audience, ZITADEL audience, metadata base64, resourceowner and IdP scopes with the login policy note. Removed: nothing.

Method: documentation only; no commands were run.

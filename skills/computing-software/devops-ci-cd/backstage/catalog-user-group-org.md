---
id: computing-software.devops-ci-cd.backstage.catalog-user-group-org
name: catalog-user-group-org
category: computing-software
field: devops-ci-cd
product: backstage
tags: [user-kind, group-kind, org-structure, backstage]
level: practitioner
status: docs-checked
description: "Model people and teams with User and Group entities so ownership resolves and sign-in can match users."
sources:
  - https://backstage.io/docs/features/software-catalog/descriptor-format
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Organisational entities give ownership a target. A `Group` has a required `spec.type` and `spec.children`, plus optional `profile`, `parent` and `members`. A `User` has a `spec.memberOf` list and an optional `profile`.

```yaml
apiVersion: backstage.io/v1alpha1
kind: Group
metadata:
  name: artist-relations-team
spec:
  type: team
  profile:
    displayName: Artist Relations
    email: artists@example.com
  parent: engineering
  children: []
---
apiVersion: backstage.io/v1alpha1
kind: User
metadata:
  name: jdoe
spec:
  profile:
    displayName: Jane Doe
    email: jdoe@example.com
  memberOf: [artist-relations-team]
```

Relations produced include `memberOf` and `hasMember`, and `parentOf` and `childOf` for the group tree.

Rules of thumb:

- Import them from your identity source with an org data provider (the auth docs name Entra ID, GitHub and GitLab providers, or a custom entity provider) rather than writing each by hand.
- User entities matter for sign-in: resolvers such as `userIdMatchingUserEntityAnnotation` look up the User entity, and a sign-in fails if none matches.
- The Entity Presentation API shows `spec.profile.displayName` instead of raw references.

## Checked

2026-11-03. Confirmed on the descriptor format page: Group `spec.type` and `spec.children` required (list may be empty), optional `profile`, `parent` and `members`; User `spec.memberOf` required (list may be empty) and optional `profile`; relation pairs memberOf/hasMember and parentOf/childOf. On the sign-in identity resolver page: `userIdMatchingUserEntityAnnotation` and the error when no matching User entity exists, and that org data providers for Entra ID, GitHub, GitLab or a custom entity provider supply Users and Groups. On the Entity Presentation page: `spec.profile.displayName` is used for display. Fixed: LDAP was named as a provider but the auth page lists Entra ID, GitHub and GitLab; removed the stable-names remark.

Method: documentation only; no commands were run.

---
id: computing-software.web-development.appwrite.appwrite-identities-linked-providers
name: appwrite-identities-linked-providers
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, auth, identities, oauth2, account-linking]
level: practitioner
status: docs-checked
description: "Understand how OAuth2 identities link several providers to one Appwrite account and how to list, delete and clean them up."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/auth/identities/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: manage multiple login providers on a single user.

Concept: an identity is another way to refer to a user account. A user can hold several, each tied to a login method; currently identities are mainly used with OAuth2 providers. Logging in through an OAuth2 provider creates an identity linked to the Appwrite account.

Link a new provider:
1. The user is already logged in.
2. Start the OAuth2 flow for the other provider.
3. The new identity is created and attached to the current account automatically.

Manage them through the Account API: list identities (`listIdentities`) and delete one (`deleteIdentity`); users and administrators can do this.

Email uniqueness rule: each email must be unique across all users and identities. If `joe@example.com` links an identity using `other@company.com`, that second address becomes reserved: nobody else can create an account or identity with it. Plan support flows around this.

Cleanup: deleting a user removes associated identities and related targets through a background job. This is asynchronous and may not be immediate because of queue processing. In tests that need instant deletion, manually remove identities (and targets) before deleting the user account.

Best practice per the docs: show users which providers are connected, make identity management straightforward, and test cleanup of test identities and email conflicts.

Implementation details for the OAuth2 flow are in the OAuth2 docs.


## Checked

2026-11-04. Confirmed against the Appwrite docs page Identities (auth/identities): the concept, linking steps, email uniqueness rule and example, the Account API list and delete operations, the asynchronous cleanup and test advice, and the best practices. Removed: the "email taken error may come from another user's identity" gotcha as an error claim and the Verify step.
Method: documentation only; no commands were run.

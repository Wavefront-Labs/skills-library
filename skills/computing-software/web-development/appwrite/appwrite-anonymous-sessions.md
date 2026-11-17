---
id: computing-software.web-development.appwrite.appwrite-anonymous-sessions
name: appwrite-anonymous-sessions
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, auth, anonymous, guest-users]
level: intro
status: docs-checked
description: "Create guest sessions with Appwrite anonymous login and later convert them into full accounts without losing the guest data."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/auth/anonymous/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let visitors use your app before signing up.

Create the session with `account.createAnonymousSession()` (client Web SDK). In GraphQL use the `accountCreateAnonymousSession` mutation, which returns `_id`, `userId`, `provider` and `expire`.

Purpose: guest users can store things like items in a cart or theme preferences before they create an account, which lowers sign-up friction. If the user later creates an account, their information is inherited by the new account.

Attaching an account: to move from an anonymous session to a user account session, create an account with any of these methods: email and password, phone (SMS), Magic URL, or OAuth2.

Limitation: anonymous users cannot sign back in. If the session expires, they move to another computer, or they clear their browser data, they cannot log in again. Prompt the user to create an account before that happens so data is not lost.

Gotcha: do not treat an anonymous user as a recoverable identity; store nothing in it that the person cannot afford to lose.

## Checked

2026-11-04. Confirmed against the Appwrite docs page Anonymous login (auth/anonymous): the `createAnonymousSession` method and GraphQL mutation with its returned fields, guest-user purpose, data inheritance on account creation, the four conversion methods, and the cannot-sign-back-in limitation. Removed: the claim about Console > Auth > Settings method toggles and disabled methods rejecting the endpoint, and the Verify step about `account.get()` and Console views, because that page does not state them.
Method: documentation only; no commands were run.

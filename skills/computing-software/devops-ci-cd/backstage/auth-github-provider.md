---
id: computing-software.devops-ci-cd.backstage.auth-github-provider
name: auth-github-provider
category: computing-software
field: devops-ci-cd
product: backstage
tags: [github-auth, oauth-app, enterprise-instance-url, backstage]
level: practitioner
status: docs-checked
description: "Add GitHub sign-in with an OAuth app, the auth backend module and a sign-in resolver."
sources:
  - https://backstage.io/docs/auth/github/provider
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Create an OAuth App on GitHub (the docs explain the difference between GitHub Apps and OAuth Apps) and set its callback URL to your backend's auth handler. Then configure:

```yaml
auth:
  environment: development
  providers:
    github:
      development:
        clientId: ${AUTH_GITHUB_CLIENT_ID}
        clientSecret: ${AUTH_GITHUB_CLIENT_SECRET}
        # enterpriseInstanceUrl: ${AUTH_GITHUB_ENTERPRISE_INSTANCE_URL}
        # sessionDuration: { hours: 24 }
        signIn:
          resolvers:
            - resolver: userIdMatchingUserEntityAnnotation
```

Install the module in the backend:

```bash
yarn --cwd packages/backend add @backstage/plugin-auth-backend-module-github-provider
```

```ts
backend.add(import('@backstage/plugin-auth-backend'));
backend.add(import('@backstage/plugin-auth-backend-module-github-provider'));
```

- `enterpriseInstanceUrl` is for GitHub Enterprise.
- `sessionDuration` limits the lifespan of the user session; it accepts values such as `{ hours: 24 }`.
- `userIdMatchingUserEntityAnnotation` matches the GitHub user id to a User entity carrying the `github.com/user-id` annotation; other resolvers are listed in the provider page.

Other documented keys: `callbackUrl` (optional, only when Backstage is not the immediate receiver of the OAuth callback). Resolvers are tried in order and skipped only when they throw `NotFoundError`. `usernameMatchingUserEntityName` is deprecated because GitHub usernames can change; prefer `userIdMatchingUserEntityAnnotation`.

Finally add the `githubAuthApi` reference and `SignInPage` to the frontend, as described in the auth overview page.

## Checked

2026-11-03. Confirmed against the Backstage GitHub Authentication Provider page: callback URL for local development, config keys (`clientId`, `clientSecret`, `enterpriseInstanceUrl`, `callbackUrl`, `sessionDuration`, `signIn`), the four resolvers and their annotation, and the backend install lines. Removed: the unsupported advice about ingesting users with the GitHub org module.

Method: documentation only; no commands were run.

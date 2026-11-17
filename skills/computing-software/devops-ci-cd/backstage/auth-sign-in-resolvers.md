---
id: computing-software.devops-ci-cd.backstage.auth-sign-in-resolvers
name: auth-sign-in-resolvers
category: computing-software
field: devops-ci-cd
product: backstage
tags: [sign-in-resolvers, identity-resolver, user-entity-matching, backstage]
level: advanced
status: docs-checked
description: "Map an authenticated account to a Backstage user identity with built-in or custom sign-in resolvers."
sources:
  - https://backstage.io/docs/auth/identity-resolver
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

After a provider authenticates someone, a sign-in resolver decides which Backstage identity they get, usually by finding a `User` entity in the catalog. The resulting identity carries a user entity ref and ownership entity refs.

Use built-in resolvers in config:

```yaml
auth:
  providers:
    github:
      development:
        signIn:
          resolvers:
            - resolver: emailLocalPartMatchingUserEntityName
              allowedDomains:
                - acme.org
```

Resolvers are tried in order and skipped only when they throw `NotFoundError`. With `emailLocalPartMatchingUserEntityName` the docs strongly recommend setting `allowedDomains` so only authorized users can sign in.

For custom logic, write a backend module with `createBackendModule` that uses `authProvidersExtensionPoint` and `createOAuthProviderFactory`:

```ts
const customAuth = createBackendModule({
  pluginId: 'auth',
  moduleId: 'custom-github-provider',
  register(reg) {
    reg.registerInit({
      deps: { providers: authProvidersExtensionPoint },
      async init({ providers }) {
        providers.registerProvider({
          providerId: 'github',
          factory: createOAuthProviderFactory({
            authenticator: githubAuthenticator,
            async signInResolver(info, ctx) {
              // look up or issue an identity
            },
          }),
        });
      },
    });
  },
});
```

Make sure the auth config has no `resolvers` field when you supply a custom resolver, otherwise the configured resolvers take priority. Throwing an error in a resolver rejects the sign-in. A custom resolver can also issue a token for a user who is not in the catalog; use the user itself as the sole ownership reference at minimum.

## Checked

2026-11-03. Confirmed against the Backstage Sign-in Identities and Resolvers page and the GitHub provider page: identity parts, `allowedDomains`, `createBackendModule` with `authProvidersExtensionPoint` and `createOAuthProviderFactory`, resolver ordering. Removed: the claim that the first resolver to succeed wins without the `NotFoundError` rule, and the unsupported advice to ingest users first.

Method: documentation only; no commands were run.

---
id: computing-software.devops-ci-cd.spinnaker.oauth2-authentication
name: oauth2-authentication
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [oauth2, authentication, gate, userinfomapping, redirect-uri, gate-local, oidc]
level: practitioner
status: docs-checked
description: "Configure OAuth 2.0 login in Gate via Spring registration in gate-local.yml: redirect URI behind proxies, userInfoMapping, requirements, GitHub org limit, URI mismatch."
sources:
  - https://spinnaker.io/docs/setup/other_config/security/authentication/oauth/
  - https://spinnaker.io/docs/setup/other_config/security/authentication/oauth/github/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Spinnaker uses the Spring Security standard OAuth 2.0 client configuration in `gate-local.yml` (the page points to Spring's client registration properties). Spinnaker requests your email from the provider. Read the whole provider page, since setting the provider alone may not work. Providers with their own pages: Azure, GitHub Organization, Google/G Suite, Oracle Cloud.

Google example shape from the page:

```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          userInfoMapping:
            email: email
            firstName: given_name
            lastName: family_name
          userInfoRequirements:
            hd: <domain>
          google:
            client-id: <client-id>
            client-secret: <client-secret>
            scope: profile,email
            redirect-uri: https://<your-domain>/login/oauth2/code/<provider id>
        provider:
          google:
            user-info-uri: https://www.googleapis.com/oauth2/v3/userinfo
            authorization-uri: https://accounts.google.com/o/oauth2/v2/auth
            token-uri: https://www.googleapis.com/oauth2/v4/token
```

`userInfoRequirements` is a Spinnaker-specific addition.

**Redirect URI.** Gate guesses its own address when assembling the redirect URI; behind an SSL-terminating load balancer the guess can be wrong. Set `spring.security.oauth2.client.registration.<provider>.redirect-uri`. If proxies must be unwound, add to `gate-local.yml`:

```yaml
server:
  tomcat:
    protocolHeader: X-Forwarded-Proto
    remoteIpHeader: X-Forwarded-For
    internalProxies: .*
```

Older Spinnaker (below v2025.2.0, no longer supported) used `security.authn.oauth2.client.preEstablishedRedirectUri` with a `/login` suffix instead.

**userInfoMapping** maps fields from the user-info response to `email`, `firstName`, `lastName` and `username`.

**userInfoRequirements** is a map of key/value pairs restricting who may log in; values that start and end with `/` are regular expressions. This can limit login to a domain or an attribute.

**GitHub.** Endpoints: authorization `https://github.com/login/oauth/authorize`, token `https://github.com/login/oauth/access_token`, user info `https://api.github.com/user`, scope `user:email`, mapping `username: login`. Register the redirect URI `https://<gate>/login/oauth2/code/github`. The page warns that without restrictions any GitHub user can log in; to restrict to an organization set scope `user:email,read:org` and `provider-requirements: organization: <org>` under the github registration. The org lookup needs the `read:org` scope and, if the org restricts OAuth app access, approval of the app. The page recommends fronting with something like Keycloak rather than GitHub directly.

**Troubleshooting:** for `redirect_uri_mismatch`, the provider's authorized URIs must contain `https://<gate address>/login/oauth2/code/<provider>` with no trailing slash, where provider is one of azure, github, google, oracle, other (below v2025.2.0 it is `https://<gate address>/login`). Use an incognito window.

## Checked

2026-11-04. Rewritten against the current OAuth 2.0 and GitHub Organizations pages. Removed: the Halyard `security.authn.oauth2` schema and `hal config security authn oauth2 edit` command (the page now uses Spring registration properties), the clientAuthenticationScheme/useCurrentUri options and the `provider: GITHUB` value (only in the page's legacy block).

Method: documentation only; no commands were run.

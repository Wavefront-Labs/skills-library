---
id: computing-software.devops-ci-cd.renovate.host-rules
name: host-rules
category: computing-software
field: devops-ci-cd
product: renovate
tags: [host-rules, credentials, private-registry, renovate]
level: practitioner
status: docs-checked
description: "Authenticate Renovate to registries and hosts with hostRules, including precedence, disabling hosts and env-based rules."
sources:
  - https://docs.renovatebot.com/configuration-options/#hostrules
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`hostRules` tells Renovate how to authenticate. The lookup keys are `hostType` and `matchHost`, both optional. Credential and behaviour fields include `token`, `username`, `password`, `timeout`, `enabled` and `insecureRegistry`.

```json
{
  "hostRules": [
    {
      "matchHost": "docker.io",
      "username": "<some-username>",
      "password": "<some-password>"
    }
  ]
}
```

When several rules match, they apply in this order of priority:

1. Rules with only `hostType`.
2. Rules with only `matchHost`, sorted by `matchHost` length.
3. Rules with both, sorted by `matchHost` length.

Disable a host with `"enabled": false`, or use the preset `:disableHost(registry.npmjs.org)`. Add a port to `matchHost` to match a specific port; a `matchHost` with a port or path but no scheme is treated as `https://`, so include `http://` to match plain http.

Disabling a host is only fully effective in self-hosted config, because Renovate checks its cache before connecting, so a host blocked in repository config can still return cached results. Host rules in the administrator's own config are resolved at a higher trust level for `enabled`, so repository config or a preset cannot re-enable or disable that host.

Other `hostRules` fields include `abortOnError` (default `false`), `authType` (default `Bearer`; do not set a username or password with it) and `abortIgnoreStatusCodes`.

## Checked

2026-11-03. Confirmed against the Renovate configuration options page: lookup keys, credential fields, the docker.io example, match priority order, host disabling and the preset, port matching, the self-hosted caveats, `abortOnError`, `authType`. Removed the `detectHostRulesFromEnv` paragraph and the advice on secrets, which are not on that page.

Method: documentation only; no commands were run.

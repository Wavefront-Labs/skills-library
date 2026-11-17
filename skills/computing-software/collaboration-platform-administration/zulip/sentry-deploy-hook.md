---
id: computing-software.collaboration-platform-administration.zulip.sentry-deploy-hook
name: sentry-deploy-hook
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [sentry-release, deploy-hooks, error-tracking]
level: advanced
status: docs-checked
description: "Create Sentry releases automatically on each Zulip upgrade using the zulip::hooks::sentry class, an internal integration token and optional GitHub commit association."
sources: ["https://zulip.readthedocs.io/en/latest/production/deployment.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sentry release deploy hook

This hook creates a Sentry release at each upgrade so errors map to a Zulip version.

Setup in Sentry:

1. Enable Sentry error logging for Zulip first.
2. Create an internal integration named "Release annotator".
3. Give it the "Admin" permission on "Release".

Setup on the Zulip server:

1. Add `, zulip::hooks::sentry` to the `puppet_classes` line of `/etc/zulip/zulip.conf`.
2. Add a section there:

```
[sentry]
organization = your-organization-name
project = your-project-name
```

3. Store the integration's authentication token in `/etc/zulip/zulip-secrets.conf` as `sentry_release_auth_token`.
4. As root run `~zulip/deployments/current/scripts/zulip-puppet-apply`.

If you deploy from Git, Sentry can also link commits to the release. Add the GitHub integration to your Sentry project, configure the `zulip/zulip` GitHub project against your Sentry project (even when you run a private fork), and grant the internal integration "Read & Write" on "Organization" so commits can be associated.

## Checked

Confirmed against the Sentry deploy hook section of the deployment page: the Sentry-side setup, the zulip.conf and secrets entries, zulip-puppet-apply and the extra Git steps. Removed the closing sentences about the token and releases without commit attribution (not stated on the page).

Method: docs-checked 2026-11-09 against docs/production/deployment.md in the zulip/zulip repository (main), the source of the cited page.

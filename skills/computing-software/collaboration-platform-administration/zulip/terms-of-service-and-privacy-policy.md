---
id: computing-software.collaboration-platform-administration.zulip.terms-of-service-and-privacy-policy
name: terms-of-service-and-privacy-policy
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [policies-directory, terms-of-service, privacy-policy]
level: practitioner
status: docs-checked
description: "Publish your own Terms of Service and Privacy Policy pages on a self-hosted Zulip server with POLICIES_DIRECTORY, terms.md, privacy.md and TERMS_OF_SERVICE_VERSION."
sources: ["https://zulip.readthedocs.io/en/latest/production/settings.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Terms of Service and Privacy Policy pages

Zulip can serve your own policy pages for your users. Make your organization's name prominent in every document so people do not confuse them with the policies of Zulip Cloud.

Steps:

1. Choose the policy directory and set `POLICIES_DIRECTORY` in `/etc/zulip/settings.py`. The recommendation is `/etc/zulip/policies`, so policies are backed up along with the rest of the server's configuration.
2. Put Markdown files named `terms.md` and `privacy.md` in that directory.
3. Set `TERMS_OF_SERVICE_VERSION` to `1.0` to enable the feature.
4. Restart the server with the `restart-server` script in the zulip user's `deployments/current/scripts` directory, run as the `zulip` user (for example through `su zulip -c`).

Optional extras in the same directory, for documenting other policies:

- `sidebar_index.md`, a Markdown list of the pages in your policies site, which generates the navigation.
- `missing.md`, custom content shown for 404s inside this directory.

## Checked

Method: docs-checked 2026-11-09 against https://raw.githubusercontent.com/zulip/zulip/main/docs/production/settings.md (policies section read in full).

Removed: the claim that any additional Markdown file automatically becomes a policy page (docs only say extra files may document other policies). Corrected the restart command path to the form shown in the docs.

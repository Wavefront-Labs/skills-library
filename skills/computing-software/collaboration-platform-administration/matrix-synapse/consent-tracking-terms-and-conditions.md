---
id: computing-software.collaboration-platform-administration.matrix-synapse.consent-tracking-terms-and-conditions
name: consent-tracking-terms-and-conditions
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, consent, user-consent, privacy-policy, terms, form-secret, block-events-error, jinja2]
level: advanced
status: docs-checked
description: "Track user agreement to server terms: user_consent templates, form_secret, the consent listener resource, per-user consent URI HMAC, notices and blocking."
sources:
  - https://element-hq.github.io/synapse/latest/consent_tracking.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Synapse can record whether users agreed to your terms (a privacy policy is one use) and block access until they do. Each part is enabled in `homeserver.yaml`.

**Serve the policy.** Create Jinja2 templates on the local filesystem, under a language directory that currently must be `en`, with the policy named by version (for example `1.0.html`) plus a success page. The version a user accepted is stored in the database. Then:

```yaml
user_consent:
  template_dir: privacy_policy_templates
  version: 1.0
```

Also set a top-level `form_secret` (an arbitrary secret; `pwgen -y 30` works), add `consent` next to `client` in the listener `resources` names, and make sure `jinja2` is installed. After restarting, `https://<server>/_matrix/consent` should answer "Missing string query parameter 'u'".

**At registration.** Add `require_at_registration: true` and a `policy_name` under `user_consent`. In templates wrap the accept form in `{% if not public_version %}` so unauthenticated visitors only read the text.

**Consent URI for a user.** Take `/_matrix/consent` and add `u` (full MXID or localpart) and `h`, the hex HMAC-SHA256 of `u` keyed with `form_secret`:

```bash
echo -n '<user>' | openssl sha256 -hmac '<form_secret>'
```

Without `u`, the page is viewed unauthenticated and no `h` is needed.

**Notify.** Add `server_notice_content` under `user_consent` with a body containing `%(consent_uri)s`, which Synapse fills in per user. This needs server notices configured and `public_baseurl` set to the URL clients use.

**Block.** Set `block_events_error` (also using `%(consent_uri)s`) to stop joining rooms and sending messages until the user agrees; joining the server notices room is exempt. `public_baseurl` must also be set here.

## Checked

Method: docs-checked 2026-11-09 against docs/consent_tracking.md (Synapse develop branch, raw markdown, read in full).

---
id: computing-software.cybersecurity-defensive.crowdsec.crowdsec-alert-context
name: crowdsec-alert-context
category: computing-software
field: cybersecurity-defensive
product: crowdsec
tags: [alert-context, contexts, context-yaml, http-base, alert-enrichment]
level: practitioner
status: docs-checked
description: "Attach extra key-value context to CrowdSec alerts using context files, so alerts say which application and request triggered them."
sources: ["https://docs.crowdsec.net/docs/log_processor/alert_context/intro", "https://docs.crowdsec.net/docs/log_processor/collections/format", "https://docs.crowdsec.net/docs/concepts"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When a scenario fires, the alert can carry extra key-value pairs, which helps when many applications share a host. Context files live in the `contexts` directory under the config dir (`/etc/crowdsec/contexts/` on Linux), and collections often ship them. For example installing `crowdsecurity/nginx` adds `http_base`:

```yaml
context:
  target_uri:
  - evt.Meta.http_path
  user_agent:
  - evt.Meta.http_user_agent
  method:
  - evt.Meta.http_verb
  status:
  - evt.Meta.http_status
```

- `context` is the root key.
- Each child key (`target_uri`) is the **name** shown for that context.
- Each list item is an expression evaluated against the event; here the `http_path` field.

You can add your own context file in that directory; the docs link a full guide to creating Alert Context. Alert context is visible in `cscli` and the Console. Collections can also list contexts (a `contexts:` key in a collection file), and `cscli contexts` manages Hub contexts.

## Checked
2026-11-08. Confirmed against the Alert Context intro (format, `http_base` example, contexts directory, key breakdown), the collections file-format page (`contexts:` directive and `cscli contexts`) and the Concepts page (context visible in cscli and Console). Removed: the claim that `cscli contexts` installs/lists/removes (page only says it manages Hub contexts) and the unsupported detail of creating custom files.
Method: documentation only; no commands were run.

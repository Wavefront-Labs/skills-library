---
id: computing-software.networking-hardware-and-wireless.unbound.response-ip-actions
name: response-ip-actions
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, response-ip, respip, response-ip-data, response-ip-tag, ip-filtering]
level: advanced
status: docs-checked
description: "Filter or rewrite answers by the address they contain using response-ip, response-ip-data and response-ip-tag with the respip module."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# response ip actions
These options need the `respip` module in `module-config` (put it first).

- `response-ip: <netblock> <action>` applies an action when an A or AAAA answer falls in the netblock. The actions static, refuse, transparent, typetransparent and nodefault are invalid here; `deny` always drops the query.
- `response-ip-data: <netblock> <RR>` sets redirect data; it must be A, AAAA or CNAME. Only one CNAME per netblock, and not together with other types.
- `response-ip-tag: <netblock> <tags>` tags a response netblock; if the client's `access-control-tag` shares a tag, the matching `access-control-tag-action` applies. It can be set even without a `response-ip` for that netblock, and only the first statement per netblock applies (later ones are silently ignored).

Tag actions may use types that are invalid for `response-ip`. For types that depend on local data, the result is NOERROR/NODATA rather than NXDOMAIN, except for `always_nxdomain`. The result of resolution before a `deny` action is still cached for other queries.

Views accept `response-ip` and `response-ip-data` too, scoped to the view.

For zone-file based policy that includes client IP, nsdname and nsip triggers, use RPZ instead.

## Checked

2026-11-08. Read response-ip, response-ip-data, response-ip-tag and module-config in the unbound.conf manual. Corrected response-ip-tag semantics (it ties to access-control-tag-action, not a plain filter) and added the NODATA versus NXDOMAIN note.

Method: documentation only; no commands were run.

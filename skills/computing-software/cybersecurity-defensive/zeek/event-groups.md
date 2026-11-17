---
id: computing-software.cybersecurity-defensive.zeek.event-groups
name: event-groups
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, event-groups, enable-event-group, module-events, runtime-toggle]
level: advanced
status: docs-checked
description: "Switch Zeek event and hook handlers on and off at runtime with attribute-based &group and module-based event groups, driven by config options and change handlers."
sources: ["https://docs.zeek.org/en/current/reference/zeekscript/event-semantics.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# event groups

Event groups enable and disable event and hook handlers at runtime.

Rules: a handler can be in several groups and is disabled if any of its groups is disabled. All groups start enabled. A handler in no group is always enabled.

**Attribute-based groups** exist when a handler has a `&group` attribute. There is one global namespace for group names, across files and modules.

```
event http_request(c: connection, method: string, original_URI: string, unescaped_URI: string, version: string) &group="http-print-debugging"
    {
    print fmt("HTTP request: %s %s (%s->%s)", method, original_URI, c$id$orig_h, c$id$resp_h);
    }
```

Toggle with `enable_event_group("http-print-debugging")` and `disable_event_group(...)`. The page ties this to the configuration framework: an `option` plus `Option::set_change_handler`, calling `Config::set_value` once in `zeek_init` to trigger the handler.

**Module-based groups** are implicit: every handler belongs to its module's group. Use `enable_module_events(m)` and `disable_module_events(m)`. The page's example toggles packages at runtime: CommunityID uses modules `CommunityID` and `CommunityID::Notice`; JA3 uses `JA3` and `JA3_Server`.

Versus an `if` and early `return` in the handler, disabled handlers are never invoked, so groups are the more performant way to short-circuit.

Caveat: JA3 builds state from `ssl_extension` events. Enabling its handlers mid-handshake can give a hash from a partial extension list.

## Checked

2026-11-04: read against the official Zeek documentation page(s) listed in sources; the claims, names, values and examples in this skill match the page text. Nothing else was added.

Method: documentation only; no commands were run.

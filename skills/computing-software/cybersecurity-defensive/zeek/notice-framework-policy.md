---
id: computing-software.cybersecurity-defensive.zeek.notice-framework-policy
name: notice-framework-policy
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, notice-framework, notice-policy, notice-actions, notice-suppression]
level: practitioner
status: docs-checked
description: "Zeek notices: NOTICE and Notice::Info, actions (log, alarm, email, page), Notice::policy hooks with priorities, and shortcut sets like ignored_types and emailed_types."
sources: ["https://docs.zeek.org/en/current/frameworks/notice.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# notice framework policy

Analysis scripts only flag potentially interesting situations; local policy decides what is actionable. A script calls `NOTICE([$note=..., $msg=..., ...])` with a `Notice::Info` record whose `note` is a `Notice::Type`.

Actions:

- `Notice::ACTION_LOG`: write to the `Notice::LOG` stream.
- `Notice::ACTION_ALARM`: log to `Notice::ALARM_LOG`, rotated hourly and emailed to `email_dest`.
- `Notice::ACTION_EMAIL`: email the notice to `email_dest`.
- `Notice::ACTION_PAGE`: send an email to `email_dest`.

Apply actions with the `Notice::policy` hook:

```
hook Notice::policy(n: Notice::Info)
    {
    if ( n$note == SSH::Password_Guessing && /192\.168\.56\.103/ in n$sub )
        {
        add n$actions[Notice::ACTION_EMAIL];
        n$email_dest = "ssh_alerts@example.net";
        }
    }
```

Hooks accept `&priority` (default 0; higher runs first) and `break` stops lower-priority bodies.

Shortcut variables, keyed by `Notice::Type`:

- `Notice::ignored_types`: ignore entirely, not even logged.
- `Notice::emailed_types`: apply email.
- `Notice::alarmed_types`: apply alarm.
- `Notice::not_suppressed_types`: skip normal suppression; this can multiply notice volume.
- `Notice::type_suppression_intervals`: table of intervals extending suppression per type, instead of setting `$suppress_for`.

## Checked

2026-11-04: read against the official Zeek documentation page(s) listed in sources; the claims, names, values and examples in this skill match the page text. Nothing else was added.

Method: documentation only; no commands were run.

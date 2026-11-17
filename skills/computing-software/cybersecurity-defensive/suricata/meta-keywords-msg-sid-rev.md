---
id: computing-software.cybersecurity-defensive.suricata.meta-keywords-msg-sid-rev
name: meta-keywords-msg-sid-rev
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [msg, sid, rev, gid, classtype, priority]
level: intro
status: docs-checked
description: "Meta keywords that identify and classify a signature: msg, sid, rev, gid, classtype and priority, with conventions for ordering."
sources: ["https://docs.suricata.io/en/latest/rules/meta.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# msg, sid, rev, gid, classtype, priority

Meta keywords do not change inspection but shape alerts.

- `msg:"..."`: put first; start with an uppercase class label; escape `;`, `\` and `"`.
- `sid:123;`: unique number above zero within a gid. Ranges are recorded at sidallocation.org; bundled engine event rules use 2200000 to 2299999. suricata-update considers only the sid.
- `rev:N;`: increment on each change. sid and rev are usually last.
- `gid`: default 1; only appears in alert data. In fast.log `[1:123:1]` is gid:sid:rev.
- `classtype:name;`: defined in classification.config as `config classification: name,Long Name,priority`. Place before sid and rev.
- `priority:1;`: 1 to 255 (1 to 4 common, 1 highest). It overrides the classtype priority; higher priority is examined first.

## Checked

2026-11-08: read in full against the OISF/suricata doc/userguide rst source (rules/meta) read in full; the claims, names, values and examples left in this skill match the page text. Nothing else was removed.

Method: documentation only; no commands were run.

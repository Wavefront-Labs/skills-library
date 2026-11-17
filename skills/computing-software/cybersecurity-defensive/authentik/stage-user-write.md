---
id: computing-software.cybersecurity-defensive.authentik.stage-user-write
name: stage-user-write
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, user-write-stage, user-creation, enrollment, dynamic-groups, user-type]
level: practitioner
status: docs-checked
description: "Configure the authentik User Write stage: creation mode, inactive users, default group, user type, path template, prompt_data key mapping and dynamic groups."
sources:
  - https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/user_write/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: create or update the `pending_user` from the flow context, typically after a Prompt, Identification or Email stage and before User Login.

## Options
- **User creation mode**: never create, create only when required, or always create.
- **Create users as inactive**.
- **Create users group**: add new users to a group.
- **User type**: Internal, External or Service Account.
- **User path template**: defaults apply if blank.

## Key mapping from `prompt_data`
| Key | Result |
| --- | --- |
| `username`, `name`, `email` | built-in fields |
| `password` | sets the password |
| `attributes` | merges a dictionary into user attributes |
| `attributes.<key>` | custom attribute |
| `attributes.<group>.<key>` | nested attribute |

Other keys (for example `department`) are not written; they stay in `prompt_data` for later stages and policies. An Invitation stage adds its properties and custom attributes to `prompt_data`, stored the same way.

## Dynamic groups
Set `groups` in the plan context before the stage, as real `Group` objects (not names):
```python
from authentik.core.models import Group

group, _ = Group.objects.get_or_create(name="some-group")
request.context["flow_plan"].context["groups"] = [group]
return True
```

## Checked
2026-11-03. Every remaining option, endpoint, value and example was read against the authentik documentation page https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/user_write/.
Removed as not confirmed by that page: user_path/user_type context override claim.
Method: documentation only; no commands were run.

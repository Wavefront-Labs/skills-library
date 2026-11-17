---
id: computing-software.cloud-infrastructure-engineering.saltstack.states-name-and-names
name: states-name-and-names
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, states, name, names, state-id, templating, environ]
level: practitioner
status: docs-checked
description: "Shorten Salt state IDs with name, apply one state to many targets with names, and read environment variables or call modules from SLS templates."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/tutorials/states_pt3.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# name and names declarations

- `name` overrides the state ID, so a short readable ID such as `mywebsite` can stand in for a long file path when referenced by requisites.
- `names` applies one state to a list of targets, e.g. creating three users with one `user.present` block; it often removes the need for a loop.

Template helpers from the same tutorial:
- Grains let one file branch by OS (install `httpd` on RedHat, `apache2` on Ubuntu).
- `salt['environ.get']` reads environment variables, so a template can check a variable is set before running states.
- Any loaded execution module can be called through `salt[...]`, for example to look up a group's GID; that group must exist before the template renders.

## Checked

2026-11-04: read the Salt states tutorial part 3 in full. Confirmed the name and names declarations, the grains example, salt['environ.get'] with the error-checking pattern and calling execution modules from templates (group_to_gid must exist before rendering). Nothing removed.

Method: documentation only; no commands were run.


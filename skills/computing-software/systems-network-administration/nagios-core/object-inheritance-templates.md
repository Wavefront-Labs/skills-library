---
id: computing-software.systems-network-administration.nagios-core.object-inheritance-templates
name: object-inheritance-templates
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, templates, object-inheritance, use-directive, register-0, name-directive, multiple-inheritance]
level: practitioner
status: docs-checked
description: "Use Nagios Core templates: name, use and register 0, local override rules, chained and multiple inheritance with first-listed-wins, custom variable inheritance."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/objectinheritance.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Templates and inheritance

Three special variables on every object type:
- `name`: unique template label.
- `use`: template(s) to inherit from (must match another object's `name`).
- `register`: `0` = template only (not a live object); `1` default. NOT inherited, so every template needs its own `register 0`.

```
define host {
    name        generic-linux
    use         generic-host
    register    0
    max_check_attempts 5
}
define host {
    use         generic-linux
    host_name   web01
    address     192.0.2.10
}
```

## Rules
- Local values override inherited ones.
- Chains may be several levels deep; the docs advise only a few.
- Incomplete definitions are fine as templates; editing the template updates all dependents.
- Custom variables (`_name`) inherit like standard ones.
- `use a,b`: for a conflicting variable the FIRST listed template wins. Nested chains get complicated; test.

Special values are in `computing-software.systems-network-administration.nagios-core.additive-null-inheritance`.

Self-check: with several templates, test the resulting values; the page says testing is the way to learn precedence.

## Checked

2026-11-04. Read the Object Inheritance page as raw HTML (the stripped copy was truncated): name, use and register, register not inherited, local values override, chaining, incomplete definitions recommended as templates, custom variables inherit, and first-listed template wins with nested chains hard to predict. Replaced the unconfirmed config CGI self-check.

Method: documentation only; no commands were run.

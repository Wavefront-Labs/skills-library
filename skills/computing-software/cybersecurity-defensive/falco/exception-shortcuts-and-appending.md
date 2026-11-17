---
id: computing-software.cybersecurity-defensive.falco.exception-shortcuts-and-appending
name: exception-shortcuts-and-appending
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [exception-shortcuts, override-exceptions, append, in-operator, rule-override]
level: advanced
status: docs-checked
description: "Use optional values, single-field exceptions and default comps, and append exception values from a local rules file."
sources:
  - https://falco.org/docs/concepts/rules/exceptions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Full form: `fields` is a list, `comps` an equal-length list, and `values` a list of equal-length tuples. Shortcuts:

- **Values optional.** A rule may define `fields` and `comps` but no `values`, so a later override adds them: `name: cmdline_writer`, `fields: [proc.cmdline, fd.directory]`, `comps: [startswith, =]`.
- **Single field.** `fields` can be one field and `comps` one operator, which must be `in`, `pmatch` or `intersects`. Then `values` is a plain list rather than tuples: `fields: fd.filename`, `comps: in` equals `and not (fd.filename in (...))`.
- **Comps optional.** With a list of `fields`, `comps` defaults to a list of `=`. With a single field it defaults to `in`.

Appending values from a later rules file (typically the local rules file):

```yaml
- rule: Write below binary dir
  exceptions:
  - name: proc_writer
    values:
    - [apk, /usr/lib/alpine]
  - name: proc_filenames
    values:
    - [apt, [apt_files]]
  override:
    exceptions: append
```

Values are appended to those of the base rule, matched by `name`, and then the `fields`/`comps`/`values` become part of the effective condition. Lists such as `apt_files` can sit inside value tuples.

To replace rather than extend, use `override: exceptions: replace`; the values for the named exceptions are then replaced (or initialized) with the supplied lists.

Gotcha: the override file must load after the file defining the rule. Order rules files with repeated `-r` options, `rules_files` in `falco.yaml`, or the Helm value `falco.rules_files`.

## Checked

2026-11-08. Read the cited exceptions page in full and corrected the shortcut and append details to match it.

Method: documentation only; no commands were run.

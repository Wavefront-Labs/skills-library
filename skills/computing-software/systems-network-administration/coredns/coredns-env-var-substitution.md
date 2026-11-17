---
id: computing-software.systems-network-administration.coredns.coredns-env-var-substitution
name: coredns-env-var-substitution
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, environment-variables, corefile, configuration]
level: intro
status: docs-checked
description: "Substitute environment variables into a Corefile with the dollar-brace or percent syntax during parsing."
sources:
  - https://coredns.io/manual/configuration/
  - https://coredns.io/plugins/template/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: inject values from the process environment into the Corefile.

CoreDNS supports environment variable substitution anywhere in the Corefile. Two syntaxes are accepted:
- `{$ENV_VAR}`
- `{%ENV_VAR%}` (the more Windows-like form)

CoreDNS substitutes the contents of the variable while it parses the Corefile.

Example:

```
. {
    forward . {$UPSTREAM_DNS}
}
```

Related trap from the template plugin docs: Go template expressions such as `{{$var}}` are interpreted as an environment variable reference by CoreDNS (and Caddy), while `{{ $var }}` with spaces works. Write template variables with spaces inside the braces.

The manual says variables can be used anywhere in the Corefile. The docs do not describe what happens when a variable is unset, so check the resulting configuration at startup before relying on it.

## Checked

2026-11-08. Read the configuration manual page in full and the template plugin README only through its Templates section (the cited WARNING about double-brace variables is there). Removed unsupported claims about load-time fixing and reload.

Method: documentation only; no commands were run.

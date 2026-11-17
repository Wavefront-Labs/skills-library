---
id: computing-software.systems-network-administration.nagios-core.macro-sanitization-environment
name: macro-sanitization-environment
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, illegal-macro-output-chars, enable-environment-macros, nagios-env-prefix, macro-security, shell-injection, sanitize]
level: advanced
status: docs-checked
description: "Stop shell injection through Nagios Core macros with illegal_macro_output_chars, and understand which macros reach scripts as NAGIOS_ environment variables."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/macros.html
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/security.html
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/configmain.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Macro cleansing and environment variables

## Cleansing
`illegal_macro_output_chars` (main config) lists characters stripped from output-derived macros before substitution: HOSTOUTPUT, LONGHOSTOUTPUT, HOSTPERFDATA, HOSTACKAUTHOR, HOSTACKCOMMENT and the SERVICE equivalents, plus any macro containing a custom variable. Backticks are the docs' example of a character the shell interprets, which can lead to security problems; the docs recommend not skipping the stripping.

## Environment
- Most standard macros are exported to scripts as `NAGIOS_<NAME>` (HOSTNAME to `NAGIOS_HOSTNAME`).
- `$USERn$` and on-demand macros are never exported.
- `enable_environment_macros` (default 1) costs CPU and memory on big installs; set 0 if scripts take macros as arguments.
- `use_large_installation_tweaks` also stops summary and group-member macros being exported.

## Related hardening
Put credentials in `$USERn$` resource files (mode 600/660) and use full paths in commands.

## Checked

2026-11-04. Confirmed against the Macros page (Macro Cleansing list, custom variable macros stripped, NAGIOS_ prefix, $USERn$ and on-demand macros not exported) and the main configuration page (illegal_macro_output_chars, enable_environment_macros default 1 with its memory and CPU cost). Removed an unconfirmed attacker-influence claim and the self-check.

Method: documentation only; no commands were run.

---
id: computing-software.systems-network-administration.nagios-core.regexp-matching
name: regexp-matching
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, regexp, use-regexp-matching, use-true-regexp-matching, regular-expressions, object-names]
level: advanced
status: docs-checked
description: "Enable regular expression matching in Nagios Core object directives with use_regexp_matching and use_true_regexp_matching, and what triggers regex handling."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/objecttricks.html
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/configmain.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Regex in object directives

Main config options (both default 0):
- `use_regexp_matching=1`: certain object directives are treated as regex, but only for values containing `*`, `?`, `+` or `\.`.
- `use_true_regexp_matching=1`: regex applied to ALL appropriate directives (only meaningful with the first enabled).

Applies to name fields of hosts, hostgroups, services, servicegroups (e.g. `host_name`, `hostgroup_name`, `service_description`, `servicegroup_name`).

## Caution
- Directives you did not intend as regex may be misread; re-verify the config after enabling.
- The plain wildcard examples in `computing-software.systems-network-administration.nagios-core.wildcards-and-exclusion` assume regex matching is DISABLED.

## Self-check
`nagios -v` still passes; the page says problems from unintended regex matches should become evident when the configuration is verified.

## Checked

2026-11-04. Confirmed on the Object Tricks page (standard examples require use_regexp_matching disabled, regex used by default only for names containing *, ?, + or \., applies to host, hostgroup, service and servicegroup names, warning about unintended interpretation) and the main configuration page (both options default 0, use_true_regexp_matching treats all appropriate directives as regex). Replaced the unconfirmed config CGI check.

Method: documentation only; no commands were run.

---
id: computing-software.cybersecurity-defensive.zeek.config-framework-options
name: config-framework-options
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, config-framework, option-keyword, config-files, config-log]
level: practitioner
status: docs-checked
description: "Change Zeek settings at runtime: option keyword, Config::config_files, config file value formats, Config::set_value for tables, and config.log."
sources: ["https://docs.zeek.org/en/current/frameworks/configuration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# config framework options

Constants and `redef` only change at startup, and restarting loses connection state. Options can change at runtime.

```
module Test;
export {
    option my_networks: set[subnet] = {};
    option enable_feature = F;
    option timeout_after = 1min;
}
```

Options cannot be declared inside functions, hooks or events, must be initialised, and cannot take normal assignments. `redef` works without `&redef`.

Register files, each line `[option name][tab or spaces][new value]`, with `#` comments:

```
redef Config::config_files += { "/path/to/config.dat" };
```

```
Test::enable_feature T
```

In a cluster only the manager watches the files and relays updates. No header lines are needed.

Value formats differ from script syntax: addr `1.2.3.4` (no netmask); bool `T`/`1` or `F`/`0`; interval and time as epoch seconds without a unit; pattern `/(foo|bar)/`; port `42/tcp` (missing protocol means `/unknown`); set and vector as comma-separated values (empty means nothing after the name); string unquoted, with no backslash handling. Tables and records are unsupported in files; use `Config::set_value("Test::host_port", t)` instead. Bad values are ignored with a `reporter.log` warning, as are unknown option names. The last entry wins.

Every change is logged to `config.log` (`Config::Info`: ts, id, old_value, new_value, location).

## Checked

2026-11-08. Read the Configuration Framework page in full; every claim confirmed.

Method: documentation only; no commands were run.

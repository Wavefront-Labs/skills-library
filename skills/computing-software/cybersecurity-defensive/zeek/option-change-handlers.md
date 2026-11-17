---
id: computing-software.cybersecurity-defensive.zeek.option-change-handlers
name: option-change-handlers
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, option-change-handler, set-change-handler, config-set-value]
level: advanced
status: docs-checked
description: "Validate or react to runtime option changes with Option::set_change_handler: chaining by priority, location argument, rejecting a value."
sources: ["https://docs.zeek.org/en/current/frameworks/configuration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# option change handlers

A change handler is a function Zeek calls immediately before it changes an option's value. Its return value becomes the value Zeek assigns, so returning the original value rejects the change.

```
module Test;
export {
    option testaddr = 127.0.0.1;
}

function change_addr(id: string, new_value: addr): addr
    {
    print fmt("Value of %s changed from %s to %s", id, testaddr, new_value);
    return new_value;
    }

event zeek_init()
    {
    Option::set_change_handler("Test::testaddr", change_addr);
    }
```

The second parameter and return type must match the option's type. `Option::set_change_handler` takes the option name as a string including the module name, even when called inside that module.

Several handlers may be registered for one option. They chain: the value returned by the first is the new value seen by the next. An optional third argument to `Option::set_change_handler` sets the priority.

A handler may take an optional third parameter of type string. For a change from a config file it is the file's pathname; for `Config::set_value` it is that function's optional third argument.

The framework itself uses change handlers to write changes to `config.log`. Changes can come from config files (via the input framework) or from calls to `Config::set_value`, which in a cluster only needs to run on the manager.

## Checked

2026-11-08. Read the Configuration Framework page in full; every claim confirmed.

Method: documentation only; no commands were run.

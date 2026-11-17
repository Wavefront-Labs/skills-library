---
id: computing-software.cybersecurity-defensive.zeek.script-load-and-conditional-directives
name: script-load-and-conditional-directives
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, directives, at-load, at-if, zeekpath]
level: practitioner
status: docs-checked
description: "Zeek script directives: @load and __load__.zeek directory loading, ZEEKPATH, @unload, @load-sigs, @load-plugin, @prefixes, and @if, @ifdef, @ifndef, @else, @endif conditionals."
sources: ["https://docs.zeek.org/en/current/reference/zeekscript/directives.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# script load and conditional directives

Directives are evaluated before script execution begins.

**@load** takes a path relative to the file search path (changed with the `ZEEKPATH` environment variable). The `.zeek` extension is optional and the name cannot contain whitespace.

```
@load policy/misc/capture-loss
@load tuning/defaults
```

Naming a directory loads its `__load__.zeek`, which holds further `@load` lines. Loading a script twice is not an error; repeats are ignored.

- **@unload** stops a not-yet-loaded script from loading later; it has no effect if already loaded.
- **@load-sigs** loads a signature file (`.sig` optional), for example `@load-sigs base/protocols/ssl/dpd`.
- **@load-plugin** activates a dynamic plugin: `@load-plugin Demo::Rot13`. Outside bare mode (`zeek -b`) Zeek activates all plugins in `ZEEK_PLUGIN_PATH`; in bare mode use the directive, the plugin name on the command line, or `ZEEK_PLUGIN_ACTIVATE`.
- **@prefixes** `= cluster` replaces prefixes, `+= cluster-manager` adds one. For each loaded script Zeek strips the search-path part, turns `/` into `.`, prepends the prefix and loads a matching file if found, so prefix `test` with `local.zeek` finds `test.local.zeek`. The `-p` option does the same.
- **@DIR** and **@FILENAME** expand to the script's directory and filename. **@deprecated** marks a script, optionally with a message.

Conditionals take a `bool` expression, and `@endif` is required:

```
@ifdef ( pi )
    print "pi is defined";
@else
    print "pi is not defined";
@endif
```

`@ifndef` is the inverse of `@ifdef`.

## Checked

2026-11-04: read against the official Zeek documentation page(s) listed in sources; the claims, names, values and examples in this skill match the page text. Nothing else was added.

Method: documentation only; no commands were run.

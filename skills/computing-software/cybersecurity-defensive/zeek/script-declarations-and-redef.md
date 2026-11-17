---
id: computing-software.cybersecurity-defensive.zeek.script-declarations-and-redef
name: script-declarations-and-redef
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, redef, module-export, option-declaration, extend-record]
level: practitioner
status: docs-checked
description: "Zeek declarations: module, export, :: operator, global, const, option and type, and every use of redef including records, enums and &log."
sources: ["https://docs.zeek.org/en/current/reference/zeekscript/statements.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# declarations and redef

Declarations cannot appear inside a function, hook or event handler, and come before statements in the concatenation of all loaded scripts. The kinds are `module`, `export`, `global`, `const`, `option`, `type`, `redef` and callables.

- `module mymodule;` sets scope for later globals until the script ends or another `module`. The name `GLOBAL` switches to the global namespace (the notice framework uses it for `NOTICE()`).
- `export { ... }` holds declarations only (no statements) and makes them visible elsewhere through `::`.
- An `option` cannot be changed by assignment, only through `Config::set_value` or a file in `Config::config_files`. It cannot use `local`, `global` or `const`.
- `type mytype: table[count] of table[addr, port] of string;`

`redef` forms:

```
redef pi = 3.14;
redef set_of_ports += { 22/tcp, 53/udp };
redef enum color += { Blue, Red };
redef record MyRecord += { n2:int &optional; s2:string &optional; };
redef record Notice::Info$email_dest -= { &log }
redef event myevent(s:string) { print "Redefined", s; }
```

- Initial values need `&redef` on `global` or `const`; an `option` can be redefined without it.
- Tables, sets, vectors and patterns accept `+=`; `-=` removes from sets and tables.
- Extending records or enums needs `+=`, and new record fields need `&optional` or `&default`.
- Changing a field's attributes (page marks added in 5.1) works for `&log` only.
- `redef event` replaces all bodies defined before it.

## Checked

2026-11-08. Read the Declarations and Statements page in full; every claim confirmed.

Method: documentation only; no commands were run.

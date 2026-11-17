---
id: computing-software.systems-network-administration.varnish-cache.vcl-language-basics
name: vcl-language-basics
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [vcl-syntax, vcl-version, include-import, vcl-subroutines]
level: intro
status: docs-checked
description: "Write valid VCL: the vcl 4.x version line, identifiers, operators, comments, include and import, user subroutines with call, and how same-named built-in subs concatenate."
sources:
  - https://www.varnish.org/docs/reference/vcl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# vcl language basics

VCL is a small domain-specific language for request handling and caching policy. When a configuration is loaded, the management process translates the VCL to C, compiles it to a shared object and loads that into the server process. Each file must start by declaring its version with `vcl X.Y;`; this Varnish version supports syntax 4.0 and 4.1.

- Identifiers: ASCII, starting with an alphabetic character, then letters, digits, `-` or `_` (`e1xam_p-le` is valid, `1try` is not). Strings can hold any bytes except NUL.
- Operators: `=`, `+ - * / %`, `+= -= *= /=` (`+=` appends for strings), `== != < > <= >=`, `~ !~` (regex or ACL match), `!`, `&& ||`.
- `if` and `else`; nested logic with `elseif` (`elsif`, `elif`, `else if` are equivalent). There are no loops or iterators.
- Variables are examined with `set` and `unset`; the compiler detects impossible operations such as `unset req.url`.
- Comments: `//`, `#`, `/* ... */`.
- Strings: `"..."` (no newlines) or long form `{"..."}` or `"""..."""`.
- `include "foo.vcl";`: an absolute path starts with `/`, `./` is relative to the including file, otherwise it is searched in the `vcl_path` directories. `include +glob "/etc/varnish/example.org/*.vcl";` works only with absolute or `./` paths.
- `import std;` loads a VMOD.
- Subroutines take no arguments and return nothing: `sub pipe_if_local { ... }` and `call pipe_if_local;`. Built-in subroutine names begin with `vcl_`, which is reserved. A bare `return;` exits a custom sub; `return (action)` ends a `vcl_*` sub.
- Several subs with a built-in name are concatenated in source order, and the built-in VCL is concatenated implicitly at compile time.
- Objects are created with `new` in `vcl_init` only: `new b = directors.round_robin();`.
- Declared but unused backends, probes, ACLs and subs give compile errors; mark intentional ones with `unused name;` or set `-p vcc_feature=-err_unref` on varnishd (global warning instead).
- Versioning: the version at the top of the `-f` file is a hard limit. You cannot include `vcl 9.1;` from `vcl 8.7;`. Included files need not declare a version; one that does applies to that file and its includes.

## Checked
2026-11-08. Read in full: the VCL reference page. The Users Guide VCL syntax page was not read and is dropped. Removed: the `varnishd -C -f` verification command (varnishd manual not read) and the invented `./conf/*.vcl` include example.
Method: documentation only; no commands were run.

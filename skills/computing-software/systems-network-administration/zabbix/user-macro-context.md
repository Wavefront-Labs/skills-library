---
id: computing-software.systems-network-administration.zabbix.user-macro-context
name: user-macro-context
category: computing-software
field: systems-network-administration
product: zabbix
tags: [macro-context, regex-context, lld-macros, thresholds, low-space-limit, macro, context, regex]
level: advanced
status: draft
description: "Override macro values per context, including regex contexts, to give discovered entities different thresholds."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/macros/usermacros_context
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Append a context to override a default: {$MACRO:"static text"} or {$MACRO:regex:"expression"}. Quotes are optional unless the context contains } or starts with a quote. A regex context can be defined only in macro configuration; elsewhere regex: is treated as static text.

Docs example for file system space:
{$LOW_SPACE_LIMIT} = 10
{$LOW_SPACE_LIMIT:/home} = 20
{$LOW_SPACE_LIMIT:regex:"^/[a-z]+$"} = 30
Trigger prototype: last(/host/vfs.fs.size[{#FSNAME},pfree])<{$LOW_SPACE_LIMIT:"{#FSNAME}"}
Result: /home alerts under 20 percent free, paths like /etc, /tmp, /var under 30, everything else under 10.

Rules:
- Simple contexts are matched first, then regex contexts in undefined order. Do not create different context macros that match the same string.
- If the macro with context is not found on host, templates or globally, the macro without context is used.
- Only low-level discovery macros are supported inside the context. Other macros are plain text.
- Context is not split on commas. Leading spaces are ignored, trailing spaces count: {$MACRO:A} equals {$MACRO: A} but not {$MACRO:A }.
- A quoted context cannot end with a backslash.
- {$MACRO:A}, {$MACRO: A} and {$MACRO:"A"} are all the same macro.

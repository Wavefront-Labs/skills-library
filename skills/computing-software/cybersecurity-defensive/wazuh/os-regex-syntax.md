---
id: computing-software.cybersecurity-defensive.wazuh.os-regex-syntax
name: os-regex-syntax
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [os-regex, osregex, sregex, escapes, regex-limitations]
level: advanced
status: docs-checked
description: "Wazuh OS_Regex syntax and its limits: anchors, escapes, modifiers only on escapes, no alternation in groups, inverted dot, plus PCRE2 notes."
sources:
  - https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
OS_Regex is one of three regex types in Wazuh rules, alongside sregex (OS_Match) and PCRE2.

Special characters: `^` start of text, `$` end of text, `|` alternation between patterns.

Modifiers `+` (one or more) and `*` (zero or more) apply only to backslash expressions.

Escapes:
- `\w` letters, digits, `-`, `@`, `_`
- `\d` digit; `\s` ASCII space; `\t` tab
- `\p` punctuation and symbols, including `*` and `+`
- uppercase `\W`, `\D`, `\S` match the inverse
- `\.` matches any character

To use `$ ( ) \ | <` literally, escape them with a backslash.

Limitations and traps:
- `*` and `+` cannot follow bare characters: `0+` is invalid, `\d+` works.
- Alternation inside groups such as `(foo|bar)` is not permitted.
- Complex backtracking is unsupported.
- `.` matches a literal dot and `\.` matches any character, the reverse of common regex.
- `\s` matches only a space, not a tab.
- There is no syntax for a literal `^`, `*` or `+`.

PCRE2 is the third type and supports features such as recursive patterns, look-ahead and look-behind and non-greedy quantifiers. It is case-sensitive by default; use `(?i)` for case-insensitive matching. Rules and decoders are XML and the parser does not decode entities, so to match a literal `<` or `>` in a PCRE2 expression write `\x3C` or `\x3E`, for example `<regex type="pcre2">from=\x3C(.*?@(.*?))\x3E</regex>`.

## Checked

2026-11-08: confirmed against the Wazuh docs page Regular Expression Syntax (read in full): the three regex types, OS_Regex escapes, modifiers, special characters, escaping list, all six limitations, and the PCRE2 case-sensitivity and \x3C/\x3E guidance. Replaced the unsupported advice to switch to pcre2 with the documented PCRE2 features.
Method: documentation only; no commands were run.

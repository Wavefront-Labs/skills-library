---
id: computing-software.cybersecurity-defensive.application-security.redos-prevention
name: redos-prevention
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [redos, regular-expression-dos, catastrophic-backtracking, re2, regex-timeout, cwe-1333]
level: practitioner
status: docs-checked
description: "Prevent ReDoS: spot catastrophic backtracking patterns, avoid untrusted regexes, bound input length, set backtracking limits, and use non-backtracking engines."
sources: ["https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service_-_ReDoS", "https://cwe.mitre.org/data/definitions/1333.html", "https://github.com/google/re2/wiki/Syntax"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ReDoS prevention

Most regular expression engines use a backtracking algorithm that can take time exponential in the input size on
certain patterns. When the engine cannot match, it returns to earlier positions and tries other paths until all are
explored. A crafted input then hangs the code (a WAF, a web server, a browser) for a very long time.

## Evil regex shape
A pattern is an "evil regex" if it can get stuck on crafted input. OWASP's marker: a repeated group that contains
either a repetition or an alternation with overlap. Examples from OWASP: `(a+)+$`, `([a-zA-Z]+)*$`, `(a|aa)+$`,
`(a|a?)+$`, all vulnerable to `aaaaaaaaaaaaaaaaaaaaaaaa!`. For `^(a+)+$` the number of paths doubles with each extra
`a` (65,536 paths for sixteen `a` followed by `X`). CWE-1333 also lists `(\w+\s?)*$`.

## Defences (CWE-1333 mitigations)
1. **Use expressions that do not backtrack** (high effectiveness), for example by removing nested quantifiers. This is
   one of the few effective solutions when users supply the regular expressions.
2. **Do not run regular expressions on untrusted input**; if you must, avoid backtracking in the expression (high).
3. **Limit the length of the input** the regex processes (moderate).
4. **Set backtracking limits** in the engine configuration, such as PHP `pcre.backtrack_limit`, and limit execution
   time of the process (moderate).
5. **Regex injection**: never build a pattern from user input on a backtracking engine. OWASP shows a password check
   that compiles the user name as a regex, which hangs on an attacker-chosen name.
6. **Client-side validation does not protect the server.** An attacker can assume the same evil regex runs on the
   server.

## Engine choice
RE2 syntax documents what it will not run: backreferences, lookahead and lookbehind (`(?=re)`, `(?!re)`,
`(?<=re)`), possessive repetitions and atomic groups (`(?>re)`) are all marked NOT SUPPORTED. If a pattern needs none
of these, a non-backtracking engine such as RE2 is a way to remove the ReDoS risk entirely. Check that the pattern
compiles in RE2 syntax before relying on it.

## Checked
Method: docs-checked 2026-11-09 against the OWASP ReDoS page (read in full), the CWE-1333 page (mitigations section
and examples) and the RE2 Syntax wiki page (searched for unsupported constructs). Removed unconfirmed claims: named
incidents (Stack Overflow, Cloudflare), per-language engine behaviour (Ruby, Python, Node.js, Java, .NET options),
.NET and Java timeout APIs, RE2 bindings, the static-analyser and CodeQL rule names, library CVE names, and the
timing test. The Microsoft Learn regex best-practices page was not readable and was not used.

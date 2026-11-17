---
id: computing-software.cybersecurity-defensive.application-security.os-command-injection-prevention
name: os-command-injection-prevention
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [input-validation, command-injection, os-command-injection, argument-injection, subprocess, shell-false, cwe-78]
level: practitioner
status: docs-checked
description: "Prevent OS command injection: use library APIs instead of shells, separate arguments, allowlists, the argument-injection trap (--), and least privilege."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html", "https://cwe.mitre.org/data/definitions/78.html", "https://cwe.mitre.org/data/definitions/88.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OS command injection prevention

## Order of preference
1. **Do not call OS commands**: built-in library functions cannot be manipulated into other tasks (the cheat sheet's
   example: `mkdir()` instead of `system("mkdir /dir_name")`). Use the language library whenever one exists.
2. **If a command cannot be avoided, use two layers**: parameterization (structured mechanisms that keep data and
   command separate) plus input validation.
   - Java: `ProcessBuilder` with the program and each argument as separate elements (or `Runtime.exec(String[])`).
     `Runtime.exec(String)` is deprecated since Java 18 because it splits on whitespace only, which is how untrusted
     input adds extra arguments. `new ProcessBuilder("C:\\DoStuff.exe -arg1 -arg2")` is one list element, not a
     program with two arguments.
   - .NET: a fixed, fully qualified executable in `FileName`, `UseShellExecute = false`, and each argument added
     through `ProcessStartInfo.ArgumentList` (.NET Framework has no `ArgumentList`; avoid building `Arguments` from
     untrusted input). Never pass untrusted input to `cmd.exe`, `powershell.exe` or `sh -c`.
3. **Validate**: the command itself against a list of allowed commands; arguments by allowlist, for example an
   allowlist regular expression with a length limit such as `^[a-z0-9]{3,10}$` that excludes whitespace and the
   metacharacters `& | ; $ > < ` \ ! ' " ( )`.
4. **Escaping is a weaker fallback.** PHP: `escapeshellarg()` makes the input a single argument; `escapeshellcmd()`
   still lets an attacker add parameters, so prefer `escapeshellarg()`. Even then the attacker can still pass one
   argument. Hardcode the executable and its required flags; never let the user choose them.

## Argument injection (CWE-88)
Every OS command injection is also an argument injection: no shell does not mean safe.
- Input such as `--help` passed through an escape function still becomes an option of the command (the cheat sheet
  shows `curl --help`); the impact ranges from information disclosure to remote code execution.
- For commands that support it, use `--` to end option parsing. CWE-88 suggests this too: `ls -l --` makes a leading
  `-` part of a filename. For `curl`, later arguments are still URL operands, so `--` does not stop extra transfers;
  pass exactly one validated URL and add `--globoff`. Argument separation does not validate the destination, so also
  apply SSRF protections.
- Argument separation does not replace validating each argument against what the called program allows.

## Defence in depth
Run with the lowest privileges needed, ideally an isolated account used for a single task, so a successful injection
does little damage.

## Test
Try payloads containing the metacharacters above and values beginning with `-`, in a test environment, and assert in
unit tests that malicious input fails validation or reaches the program as one literal argument.

## Checked
Method: docs-checked 2026-11-09 against the OWASP OS Command Injection Defense Cheat Sheet (read in full) and the
MITRE CWE-88 page (argument-injection and `--` mitigation sections); CWE-78 was fetched and used only for the
terminology. Removed unconfirmed claims: Python, Node and Go call forms, `shlex.quote`, specific `git`, `tar`, `ssh`
and `find` option exploits, Semgrep and CodeQL rule names, and the hostname regex.

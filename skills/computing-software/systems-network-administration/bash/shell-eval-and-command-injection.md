---
id: computing-software.systems-network-administration.bash.shell-eval-and-command-injection
name: shell-eval-and-command-injection
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, sh-eval, command-injection, safe-argument-passing, ssh-quoting]
level: advanced
status: docs-checked
description: "Avoid command injection in shell scripts: no eval on untrusted input, arrays for arguments, printf %q and ${var@Q} quoting."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Injection in shell

- `eval`, `bash -c "$string"`, `sh -c "...$var..."` and `ssh host "cmd $var"` all re-parse text as code. A value such as `; rm -rf ~` or `$(cmd)` in a filename, branch name or HTTP header executes if it reaches that text unquoted. The bash manual defines `eval` as reading its arguments, joining them into one command and executing it.
- Pass data as arguments, not code: `sh -c 'cmd "$1"' _ "$var"`; `find ... -exec cmd {} +`; arrays `cmd "${args[@]}"`.
- To shell-quote a value for re-use as input: `printf '%q' "$arg"` (bash `printf` format `%q` outputs the argument in a form that can be reused as shell input) or `${var@Q}` (the `Q` transformation quotes the value in a format that can be reused as input). Example for a remote shell: `ssh host "cmd $(printf '%q' "$arg")"`.
- Indirect variables: use a nameref (`declare -n ref=name`, which makes `ref` refer to the variable whose name it holds) or `printf -v "$name" '%s' "$value"` (`-v` assigns the output to a variable) after validating `$name` against `^[A-Za-z_][A-Za-z0-9_]*$`, instead of `eval "$name=$value"`.
- Validate input with an allowlist, for example `[[ $x =~ ^[a-z0-9_-]+$ ]]` (`=~` uses POSIX extended regular expressions), and refuse a leading `-` or pass `--` where the command supports it.
- Treat anything that is evaluated as code, including values later fed to `$(( ))`, as untrusted until validated as an integer.
- Run privileged scripts with a fixed, known `PATH` and do not source or `eval` files other users can write.

## Checked
2026-11-09. Confirmed in the bash manual: `eval`, `printf` `%q` and `-v`, `${parameter@Q}`, `declare -n` nameref, `=~` as POSIX ERE. Removed: the "bash 4.4+" version tag, the specific claims about arithmetic contexts running embedded command substitutions (`a[$(cmd)]`), `declare -i`, `[[ -eq ]]`, `env -i`, and the sudoers NOPASSWD advice, none of which the cited pages state; the POSIX root URL (a stub page) was dropped from sources.
Method: documentation only; no commands were run.

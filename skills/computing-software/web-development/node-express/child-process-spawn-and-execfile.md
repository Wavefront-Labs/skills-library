---
id: computing-software.web-development.node-express.child-process-spawn-and-execfile
name: child-process-spawn-and-execfile
category: computing-software
field: web-development
product: node-express
tags: [node, child-process, execfile, spawn, command-injection, abortsignal, subprocess, web-development]
level: practitioner
status: verified
description: "Running external commands from Node safely: execFile and spawn over exec, argument arrays, timeouts and AbortSignal, output limits, exit codes and Windows quirks."
sources:
  - https://nodejs.org/api/child_process.html
  - https://nodejs.org/en/blog/vulnerability/april-2024-security-releases-2
  - https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# child_process: spawn and execFile

**Goal:** call ffmpeg/git/imagemagick and the like without shell injection, hangs, or memory blowups.

## 1. Choose the API
| API | Shell | Output | Use |
|---|---|---|---|
| `execFile(file, args)` | no | buffered | short commands, small output |
| `spawn(cmd, args)` | no (default) | streams | long-running, large output, interactive |
| `exec("cmd string")` | yes | buffered | avoid with any external input |
| `fork(module)` | no | IPC channel | Node worker processes |

## 2. execFile with promises
```js
import { execFile } from "node:child_process";
import { promisify } from "node:util";
const run = promisify(execFile);

const { stdout } = await run("git", ["log", "-1", "--format=%H", "--", file], {
  cwd: repoDir, timeout: 10_000, maxBuffer: 10 * 1024 * 1024, encoding: "utf8",
});
```
Arguments are passed as an array directly to the program - `file = "x; rm -rf /"` is just a weird filename. Still guard against **argument injection**: a value starting with `-` can become an option; put `--` before user-provided operands.
Rejection errors carry `code` (exit code), `signal`, `stdout`, `stderr`. `maxBuffer` default is 1 MiB; exceeding it kills the child.

## 3. spawn for streams
```js
import { spawn } from "node:child_process";
const ac = new AbortController();
const p = spawn("ffmpeg", ["-i", "pipe:0", "-f", "mp3", "pipe:1"], { stdio: ["pipe", "pipe", "inherit"], signal: ac.signal });
await pipeline(input, p.stdin);  // and pipe p.stdout onward
const [code] = await once(p, "close");
if (code !== 0) throw new Error(`ffmpeg exited ${code}`);
```
Always consume stdout/stderr (or set `"ignore"`) - on POSIX a full pipe buffer (64 KiB on Linux) blocks the child forever. On Windows 20 MB written to an unread pipe did not block (the child exited and `close` fired), so do not rely on that behaviour either way. Listen for `error` (ENOENT when the binary is missing; checked) as well as `close`.

## 4. Timeouts and killing
`timeout` + `killSignal` options, or `signal: AbortSignal.timeout(ms)`. Kill a whole process tree: spawn with `detached: true` and `process.kill(-p.pid, "SIGTERM")` on POSIX only (on Windows it fails with `ESRCH`; use `taskkill /pid <pid> /T /F`). `timeout` kills with SIGTERM and rejects with `killed: true`; an aborted `signal` emits an `AbortError` on the child.

## 5. Windows
- `.bat`/`.cmd` can't run without a shell; since the April 2024 security release, spawning them with `shell: false` throws `EINVAL` (BatBadBut fix). The error is thrown synchronously from `spawn()` (not an `error` event), so wrap the call in try/catch. Avoid batch files with untrusted args.
- `windowsHide: true` stops console windows popping up.
- `npm`/`npx` are `.cmd` shims on Windows: `execFile("npm", ...)` fails with `ENOENT` and `execFile("npm.cmd", ...)` with `EINVAL` (tested on Node 20 and 24). Use `shell: true` with fixed strings only, or run `node <path-to>/npm-cli.js` directly.

## 6. Environment
Pass a minimal `env` rather than inheriting secrets: `env: { PATH: process.env.PATH }`. On Windows the system still adds variables such as SYSTEMROOT, USERPROFILE and TEMP to the child.

## Verify
- [ ] `grep -rn "exec(" src` - no `exec` with interpolated input.
- [ ] Passing `"; touch /tmp/pwned"` and `"--help"` as input has no effect.
- [ ] A hung child is killed at the timeout and the request fails cleanly.

## Checked
Node 24.22.0 and 20.20.2 on Windows: `execFile` returns stdout and rejects with `code`, `signal`, `stdout`, `stderr`; output beyond the 1 MiB default `maxBuffer` (or a small explicit one) kills the child with `ERR_CHILD_PROCESS_STDIO_MAXBUFFER` and keeps 1,048,576 bytes; array arguments such as `; touch /tmp/pwned` and `--help` arrive as plain arguments while `exec` with interpolation runs the second command; a missing binary emits `error` with `ENOENT` on `spawn`; `timeout` kills with `SIGTERM` (`killed: true`) and `AbortSignal.timeout` produces an `AbortError`; consumed or `ignore`d stdout lets the child exit 0; a `.cmd` file with `spawn`/`execFile` and no shell throws `EINVAL`, works with `shell: true`; `npm` alone is `ENOENT` and `npm.cmd` without a shell is `EINVAL`; `windowsHide` is accepted; a minimal `env` hides inherited variables. The April 2024 Node security notice documents the `EINVAL` change. Process-group kill with `detached` is POSIX-only and not run.
Also run (Node 20.20.2, Windows): `spawn()` throws EINVAL synchronously (not an `error` event) for `.cmd`; `process.kill(-pid)` gives ESRCH on Windows; an unread stdout of 20 MB did not block the child on Windows (pipe-stall claim is POSIX-only and not run on Linux).
- Node 24.22.0 and 20.20.2 on Windows: `execFile` returns stdout and rejects with `code`, `signal`, `stdout`, `stderr`; output beyond the 1 MiB default `maxBuffer` (or a small explicit one) kills the child with `ERR_CHILD_PROCESS_STDIO_MAXBUFFER` and keeps 1,048,576 bytes; array arguments such as `; touch /tmp/pwned` and `--help` arrive as plain arguments while `exec` with interpolation runs the second command; a missing binary emits `error` with `ENOENT` on `spawn`; `timeout` kills with `SIGTERM` (`killed: true`) and `AbortSignal.timeout` produces an `AbortError`; consumed or `ignore`d stdout lets the child exit 0; a `.cmd` file with `spawn`/`execFile` and no shell throws `EINVAL`, works with `shell: true`; `npm` alone is `ENOENT` and `npm.cmd` without a shell is `EINVAL`; `windowsHide` is accepted; a minimal `env` hides inherited variables. The April 2024 Node security notice documents the `EINVAL` change. Process-group kill with `detached` is POSIX-only and not run.
Linux pass (Node 20.20.2 musl, busybox distro): an unread stdout pipe DOES block the child (1 MB and 20 MB writers were still running after 1.5 s, neither `exit` nor `close` fired), so the pipe-stall rule is real on POSIX; `process.kill(-pid, "SIGTERM")` on a detached child succeeds; `timeout` and `AbortSignal.timeout` behave as on Windows; `.cmd` is an ordinary missing file there.

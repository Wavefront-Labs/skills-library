---
id: computing-software.software-engineering.typescript.node-child-processes
name: node-child-processes
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, child-process, spawn, execfile, command-injection, nodejs, subprocess]
level: practitioner
status: gated
description: "Run external commands from Node safely: spawn vs execFile vs exec, avoiding shell injection, streaming output, exit codes and signals, timeouts and AbortSignal, Windows quirks."
sources: ["https://nodejs.org/api/child_process.html", "https://nodejs.org/api/child_process.html#spawning-bat-and-cmd-files-on-windows", "https://nodejs.org/api/util.html#utilpromisifyoriginal"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node child processes

**Goal:** call git, ffmpeg or any CLI from Node without shell injection, hung processes
or lost errors.

## Choose the function
| Function | Shell | Output | Use |
|---|---|---|---|
| `execFile(file, args)` | no | buffered (maxBuffer 1 MB default; tested: 2 MB of stdout rejects with `ERR_CHILD_PROCESS_STDIO_MAXBUFFER`) | short commands with small output |
| `spawn(cmd, args)` | no (unless `shell: true`) | streams | long-running, large output, interactive |
| `exec(cmdString)` | yes | buffered | avoid with any dynamic input |
| `fork(module)` | no | IPC channel | Node workers needing message passing |

## Safe, promisified execFile
```ts
import { execFile } from "node:child_process";
import { promisify } from "node:util";
const run = promisify(execFile);

const { stdout } = await run("git", ["log", "-1", "--format=%H", "--", userPath], {
  cwd: repoDir,
  timeout: 10_000,                // kills with killSignal (SIGTERM) after 10 s (tested: error has killed=true, signal=SIGTERM)
  maxBuffer: 10 * 1024 * 1024,
});
```
Arguments are passed as an array, never parsed by a shell, so `userPath = "; rm -rf /"` is just a
weird filename. Still guard against option injection: put `--` before user-supplied positional
args.

## Streaming with spawn
```ts
import { spawn } from "node:child_process";
import { once } from "node:events";
const ac = new AbortController();
const child = spawn("ffmpeg", ["-i", input, "-f", "mp4", output], { signal: ac.signal, stdio: ["ignore", "pipe", "pipe"] });
child.stderr.on("data", (d) => log.debug(d.toString()));
const [code, signal] = await once(child, "close");
if (code !== 0) throw new Error(`ffmpeg failed: code=${code} signal=${signal}`);
```
- Always consume or ignore stdout/stderr; a full pipe buffer blocks the child forever.
- `error` event fires when the command cannot start (ENOENT, tested); `close`/`exit` carry code/signal. An `AbortSignal` abort emits `error` (`AbortError`) and then `close` with signal SIGTERM (tested).
- `stdio: "inherit"` for CLIs that should show the child's output directly.

## Process lifecycle
- `child.kill("SIGTERM")`; escalate to `SIGKILL` after a grace period.
- Kill the whole tree: `detached: true` then `process.kill(-child.pid)` (POSIX process group) (gated: unconfirmed, source is paywalled or blocked; no POSIX shell with process groups was available to run it).
- On parent exit, children keep running unless you clean up; track and kill them in shutdown handlers.

## Windows quirks
- `.cmd`/`.bat` (e.g. `npm`, `npx`) cannot be spawned without a shell: use `shell: true` with
  fully controlled arguments, or call `node` with the script path. Tested on Node 24: `spawn("npm.cmd", ["-v"])` throws `EINVAL`; with `shell: true` it runs but emits deprecation warning DEP0190 because args are concatenated, not escaped (CVE-2024-27980 fix).
- Use `cross-spawn` / `execa` for portable behaviour and better errors.

## Verify
- [ ] grep: no `exec(`/`shell: true` with interpolated user input.
- [ ] Every child has a timeout or abort path, and non-zero exit codes raise errors.

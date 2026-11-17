---
id: computing-software.web-development.bun.spawn-subprocess
name: spawn-subprocess
category: computing-software
field: web-development
product: bun
tags: [bun-spawn, spawn-sync, subprocess-ipc, spawn-timeout]
level: practitioner
status: docs-checked
description: "Run child processes with Bun.spawn and spawnSync: stdio modes, exit handling, timeout and killSignal, IPC serialization with Node, maxBuffer and PTY terminal."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/runtime/child-process.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
const proc = Bun.spawn(["ls", "-la"], { cwd: "/tmp", stderr: "pipe", timeout: 5000, killSignal: "SIGKILL" });
console.log(await proc.stdout.text());
await proc.exited;                        // exit code; also proc.exitCode, proc.signalCode

const r = Bun.spawnSync(["echo", "hi"]);  // stdout/stderr are Buffers
console.log(r.stdout.toString(), r.success);

const child = Bun.spawn(["bun", "child.ts"], { ipc(msg, c) { c.send("ack"); } });
child.send("hello");
```

- stdin defaults to no input; stdout defaults to `"pipe"` (a ReadableStream); stderr defaults to `"inherit"`, so `proc.stderr` is `undefined` unless `stderr: "pipe"`.
- `onExit(proc, exitCode, signalCode, error)`, `signal: AbortSignal`, `proc.kill("SIGTERM")`, `proc.unref()`.
- IPC `serialization` is `"advanced"` by default; Bun-to-Node IPC needs `"json"`.
- `proc.resourceUsage()` reports `maxRSS` and cpu time after exit.

Gotchas:
- The parent waits for children unless `unref()`.
- `killSignal` also applies when the AbortSignal fires.
- `maxBuffer` is `spawnSync` only and can overshoot by one read.
- `terminal` (PTY) is `Bun.spawn` only; `spawnSync` throws with it, and `proc.stdout` is null.

## Checked

2026-11-04. Confirmed against the Bun docs page runtime/child-process: stdin/stdout/stderr defaults, exited/exitCode/signalCode, onExit signature, kill and unref, AbortSignal, timeout with SIGTERM default, killSignal also used for abort, maxBuffer on spawnSync with single-read overshoot, IPC handler and send, serialization advanced default and json for Node, resourceUsage, the terminal option and its spawnSync restriction (reference comment). Nothing removed.
Method: documentation only; no commands were run.

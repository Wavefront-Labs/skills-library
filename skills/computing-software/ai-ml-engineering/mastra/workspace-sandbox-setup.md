---
id: computing-software.ai-ml-engineering.mastra.workspace-sandbox-setup
name: workspace-sandbox-setup
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, sandbox, workspace, localsandbox, filesystem, daytona, background-processes, isolation]
level: practitioner
status: docs-checked
description: "Give a Mastra agent a LocalSandbox or remote sandbox via a Workspace, tune generated tools, use per-user or per-thread resolvers, and handle lifecycle, networking and credentials."
sources:
  - https://mastra.ai/docs/sandbox/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: let an agent run commands and code in an isolated environment.

## Quickstart
```typescript
import { LocalSandbox, Workspace } from '@mastra/core/workspace'
export const codingAgent = new Agent({ id: 'coding-agent', name: 'Coding agent',
  instructions: 'Use the sandbox to complete coding tasks.', model: 'your-model',
  workspace: new Workspace({ sandbox: new LocalSandbox({ workingDirectory: './workspace' }) }) })
```
`LocalSandbox` runs on the host and is not isolated or secure by default. Enable native isolation (`isolation: 'seatbelt'` on macOS, `'bwrap'` on Linux, with `nativeSandbox: { allowNetwork: false, readOnlyPaths: [...] }`; `LocalSandbox.detectIsolation()` checks availability) or use a remote/container sandbox for untrusted code.

## Tools
Generated tools follow the backend's capabilities: `execute_command` (stdout, stderr, exit code; `background: true` where supported), `get_process_output` (`tail`, `wait: true`), `kill_process`. Configure with `tools: { requireApproval: true, [WORKSPACE_TOOLS.SANDBOX.EXECUTE_COMMAND]: { enabled: false } }`; top-level `enabled: false` disables all by default and per-tool `enabled: true` overrides. Tools and workflow steps get the live sandbox via `ctx.workspace.resolveSandbox({ requestContext: ctx.requestContext })`; check `sandbox.processes` before `spawn()`.

Background process callbacks: `backgroundProcesses: { onStdout, onStderr, onExit }` on the `EXECUTE_COMMAND` entry. Background processes inherit the agent's abort signal; set `abortSignal` to a custom signal, or `null`/`false`, to outlive the request.

## Per user or thread
Use a resolver plus `sandboxCacheKey`:
```typescript
new Workspace({
  sandbox: async ({ requestContext }) => {
    const sandbox = new DaytonaSandbox({ id: `user-${requestContext.get('user-id')}` })
    await sandbox.start(); return sandbox },
  sandboxCacheKey: ({ requestContext }) => requestContext.get('user-id') as string,
})
```
For persistence, also give `filesystem` a resolver (e.g. `S3Filesystem` with `prefix: threads/${threadId}`, keyed by `MASTRA_THREAD_ID_KEY` from `@mastra/core/request-context`) and call `sandbox.mount(fs, '/workspace')` inside the sandbox resolver, since static `mounts` cannot combine with a resolver.
- Resolver-returned sandboxes belong to your app: destroy them and call `workspace.clearSandboxCache(cacheKey)` when the user/thread/session ends; `workspace.destroy()` and `mastra.shutdown()` do not destroy them.
- A static sandbox is shared by every request of that agent (or all agents inheriting Mastra-level config), not scoped per thread.
- Agent `workspace` functions are called often (registration, `GET /api/agents`), uncached: keep them cheap, never start a sandbox in them.
- With resolvers all sandbox tools are exposed up front; an unsupported one fails with `SandboxFeatureNotSupportedError`.

## Lifecycle
Static sandboxes start on first command; `workspace.init()` at startup surfaces credential/network errors early (it does not start resolver sandboxes). Hooks `onStart`, `onStop`, `onDestroy`. `mastra dev` and the generated server clean up; in a custom server call `mastra.shutdown()`; standalone, `workspace.destroy()`. What `stop()`/`destroy()`/persistence do is backend-specific; sandbox `id` is not a cross-backend persistence guarantee.

## Network and credentials
No single network policy exists; check the backend. `LocalSandbox` with native isolation blocks network unless `allowNetwork`. Example: `new DaytonaSandbox({ networkBlockAll: true, domainAllowList: 'registry.npmjs.org,api.github.com' })` (applied at creation; `networkAllowList` for CIDR). `sandbox.networking?.getPortUrl(8000)` exposes a server port where supported and may make it reachable by others. Environment variables are visible to code in the sandbox; pass scoped tokens per command: `sandbox.executeCommand('node', ['scripts/download-reports.js'], { env: { REPORTS_READ_TOKEN: process.env.REPORTS_READ_TOKEN } })`.

Filesystems (S3, GCS, Google Drive) give read/write/search tools and FUSE mounts into remote sandboxes; see the Filesystem docs page.

## Checked

Method: 2026-11-08 read the raw MDX of the Mastra Sandboxes page in full and compared each claim in the skill (LocalSandbox isolation, generated tools and config, resolvers and sandboxCacheKey, lifecycle and cleanup, network and credential guidance); all are supported and unchanged.

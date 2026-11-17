---
id: computing-software.ai-ml-engineering.mastra.agent-controller-sessions
name: agent-controller-sessions
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, harness, agentcontroller, sessions, threads, modes, tool-approval, subagents]
level: sme
status: docs-checked
description: "Build interactive Mastra apps with AgentController: sessions, threads, modes, model switching, tool approvals, subagents, channels and browser clients."
sources:
  - https://mastra.ai/docs/harness/agent-controller
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: host ongoing, multi-mode agent conversations with `AgentController` instead of one-shot `Agent` calls.

## Model
- Controller: shared host (modes, models, storage, workspace, approvals, subagents, channels). Initialize once, reuse.
- Session: isolated live runtime per user/task (mode, model, state, event bus, grants, current thread). Do not store a "current" session on the controller.
- Thread: stored conversation; persists with storage. `session.state`, grants, pending approvals and active runs do not survive process recreation. Active mode and current model can persist as thread settings; switching modes does not change the model.
- For agents working in a codebase use `createCodingAgent()` rather than `new Agent()`.

## Quickstart
```typescript
import { AgentController } from '@mastra/core/agent-controller'
const controller = new AgentController({
  id: 'assistant-controller',
  agent,                       // backing Agent
  storage: new LibSQLStore({ id: 'agent-controller-storage', url: 'file:./mastra.db' }),
  workspace: new Workspace({ id: 'assistant-workspace', filesystem: new LocalFilesystem({ basePath: './workspace' }) }),
  modes: [
    { id: 'plan', name: 'Plan', metadata: { default: true }, instructions: 'Reason about the task before making changes.' },
    { id: 'build', name: 'Build', instructions: 'Implement the approved plan.' },
  ],
})
await controller.init()
const session = await controller.createSession({ resourceId: 'user-123' })
const unsubscribe = session.subscribe(event => {
  if (event.type === 'message_update' && event.event.type === 'text-delta') process.stdout.write(event.event.delta)
})
await session.sendMessage({ content: 'Plan a small TypeScript CLI.' })
unsubscribe()
```
Each message emits `message_start`, zero or more `message_update` deltas, then `message_end` (with message ID).

## Sessions and threads
- `createSession()` is get-or-create by `id` (defaults to `resourceId`). Different ids have separate buses, runs, state, mode/model and thread bindings but share `resourceId` threads and memory.
- `threadId` binds to an exact thread (switches to it or creates it), even for cached sessions.
- `session.thread.create({ title })`, `.switch({ threadId })`, `.list()`, `.getOwner()`, `.transferOwnership({ toOwnerId })`. Threads store `metadata.ownerId` and `metadata.createdBy` (creator never changes). Runs snapshot the owner at start (`AgentControllerRequestContext.threadOwnerId`). Transfers are serialized only within one process; for cross-process compare-and-set commit to your own storage first, then mirror.
- Client paging: `client.getAgentController('assistant-controller').session('user-123').listMessages(threadId, { page: 0, perPage: 20, orderBy, filter, include })`. `page` is zero-indexed; default `perPage` 40; `limit` is a deprecated alias and must be `perPage` when using `orderBy`/`filter`/`include`.

## Modes and models
Mode fields: `instructions`, `additionalTools` (or `tools`, mutually exclusive), `availableTools` (allowlist; permission denies still win), `transitionsTo`. Switch: `session.mode.switch({ modeId })`, read `session.mode.get()` / `.resolve()`. Models: `session.model.switch(id)` / `.get()`.
Observational Memory: `omConfig: { observerModel: 'auto', reflectorModel: 'auto', defaultObserverModelId, defaultReflectorModelId, resolveAutoModelId }`; `session.om.observer.switchModel({ modelId: 'auto' })`. If the resolver returns undefined or throws, the default id is used.

## State
`stateSchema` and `initialState` on the controller; `session.state.get()` (snapshot) and `await session.state.set({...})` (validated merge).

## Approvals and suspensions
- `toolCategoryResolver: name => 'execute' | null`; `session.permissions.setForCategory({ category, policy: 'ask' })`, `setForTool({ toolName, policy: 'deny' })`.
- On `tool_approval_required`: `session.respondToToolApproval({ toolCallId, decision: 'approve' })`. `always_allow_category` grants only for that gate's thread.
- `ask_user` and `submit_plan` use suspensions: on `tool_suspended`, `session.respondToToolSuspension({ toolCallId, resumeData })`. For `submit_plan` resume with `{ action: 'approved' }` or `{ action: 'rejected', feedback }`; it takes a plan file path (agent needs a writable filesystem), your app reads the file to show the plan.

## Subagents
`subagents: [{ id, name, description, instructions, allowedControllerTools, allowedWorkspaceTools, defaultModelId }]` plus the built-in `subagent` tool. `forked: true` clones the parent thread, uses parent instructions/tools, ignores the definition's instructions/tools/allowlists/model, and requires memory. `session.subagents.model.set({ modelId })` or with `agentType`; agent-type selection wins.

## Channels
`channels: { adapters: { slack: createSlackAdapter() }, resolveResourceId, onSessionStart, resolveSession, onStaleToolApproval }` and register via `new Mastra({ agentControllers: { controller }, storage })`. Webhook: `/api/agent-controllers/<CONTROLLER_ID>/channels/<PLATFORM>/webhook`.
- Default resource id is derived from the chat thread id, prefixed `channel:`; `resolveResourceId` affects new threads only.
- `onSessionStart` runs once per session before the first message; errors are swallowed, so it cannot refuse. Use `resolveSession` to authorize (throw to refuse; the chat stays silent; refusals are `ChannelSessionRejectedError`). Create the session under `thread.resourceId` with `threadId: thread.id`. It also runs on approval-card answers.
- Approval gates are in memory; stale approvals never run the tool. Handle via `onStaleToolApproval({ decision, toolCallId, runId, memory })`. Use a long-lived server. Adapters that cannot render approval controls run tools without prompting.

## UI
- Server: `session.subscribe`, `session.displayState.get()`, event `display_state_changed`.
- Browser: `client.getAgentController(key).session(id)`; key is the one used in `agentControllers`, may differ from controller `id`. `await session.create()`, then `await session.subscribe({ onEvent, onError, onReconnect, reconnect: true })`. `idleTimeoutMs` default 60000. Missed events are not replayed; call `session.state()` in `onReconnect`. Use `session.sendMessage(content)`, `approveTool(toolCallId, approved)`, `respondToToolSuspension(toolCallId, resumeData)`. No `displayState.get()` on the client.

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.

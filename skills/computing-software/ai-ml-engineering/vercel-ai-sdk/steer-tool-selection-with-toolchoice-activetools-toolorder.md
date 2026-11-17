---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.steer-tool-selection-with-toolchoice-activetools-toolorder
name: steer-tool-selection-with-toolchoice-activetools-toolorder
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [tool-calling, tool-choice, active-tools, tool-order, prompt-caching]
level: practitioner
status: docs-checked
description: "Force or forbid tool calls with toolChoice, limit exposed tools with activeTools, and stabilise definition order with toolOrder for provider caching."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/tools-and-tool-calling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: control which tools the model may call and how definitions are presented to the provider.

## toolChoice
| Value | Effect |
|---|---|
| `'auto'` (default) | model decides |
| `'required'` | must call some tool |
| `'none'` | must not call tools |
| `{ type: 'tool', toolName: 'weather' }` | must call that tool (name is typed) |

```ts
await generateText({ model, tools: { weather }, toolChoice: 'required', prompt });
```
With `'none'` the SDK prevents local tool execution even if the model returns a tool call; the response yields a `ToolChoiceViolationError`. In `streamText` the tool parts are withheld, so client-side tools are not invoked either. Tool call repair and input refinement are skipped for rejected calls.

## activeTools
Models handle a limited number of tools. `activeTools: ['firstTool']` limits what is sent while keeping static typing over a large `ToolSet`. Default `undefined` means all active. Can be returned from `prepareStep` per step.

## toolOrder
Some providers include tool definitions in the cached request prefix; changing order between similar requests can prevent cache reuse.
```ts
toolOrder: ['search', 'readFile']
```
The list may be partial: listed tools come first in that order, the rest follow alphabetically. Names are typed from your `tools`. It changes only definition order; it does not force calls (use `toolChoice`) or limit availability (use `activeTools`). When both are set, `activeTools` filters first, then `toolOrder` orders what remains.

## Related error classes
`NoSuchToolError`, `InvalidToolInputError`, `ToolCallRepairError`, `ToolChoiceViolationError` (response does not satisfy a required or specific choice).

## Gotchas
- Per-step forcing example: `prepareStep` returning `{ toolChoice: { type: 'tool', toolName: 'tool1' }, activeTools: ['tool1'] }` on step 0.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. No content change needed.

Method: documentation only; no commands were run.

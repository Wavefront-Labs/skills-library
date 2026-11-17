---
id: computing-software.ai-ml-engineering.mastra.agents-and-tools-as-workflow-steps
name: agents-and-tools-as-workflow-steps
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, workflows, agentstep, toolstep, createstep, structured-output, agent-shorthand, tool-shorthand]
level: practitioner
status: docs-checked
description: "Call Mastra agents and tools inside workflow steps, or compose them as steps with createStep, .agent() and .tool(), including structured output and input mapping."
sources:
  - https://mastra.ai/docs/workflows/agents-and-tools
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: use an LLM agent or an existing tool inside a Mastra workflow, choosing between calling it from `execute()` and composing it directly as a step.

## Choosing
- Call from a step's `execute()` when you want control: adjust the call, track message history, return structured output, or prepare context and process the response.
- Compose as a step (`createStep(agent)` / `createStep(tool)`) when you do not need to change how it is invoked.

## Call an agent inside execute()
Use `.generate()` or `.stream()` on an agent fetched from `mastra`:

```typescript
const step1 = createStep({
  execute: async ({ inputData, mastra }) => {
    const testAgent = mastra.getAgent('testAgent')
    const response = await testAgent.generate(`Convert this message into bullet points: ${inputData.message}`, {
      memory: { thread: 'user-123', resource: 'test-123' },
    })
    return { list: response.text }
  },
})
```

## Agent as a step
`const step1 = createStep(testAgent)`. With no `structuredOutput` option the agent step takes `{ prompt: string }` and returns `{ text: string }`. Use `.map()` before it to turn the previous output into a `prompt`:

```typescript
createWorkflow({})
  .map(async ({ inputData }) => ({ prompt: `Convert this message into bullet points: ${inputData.message}` }))
  .then(step1)
  .then(step2)
  .commit()
```

## Structured output from an agent step
Pass `structuredOutput` as the second argument. The step's `outputSchema` is set to match, so the next step can declare that schema as its `inputSchema`:

```typescript
const agentStep = createStep(testAgent, { structuredOutput: { schema: articleSchema } })
```

`structuredOutput.schema` accepts any Standard JSON Schema (the page uses a zod object). For error-handling strategies and streaming with structured output, the page points to the Structured Output docs.

## The .agent() shorthand
`.agent(testAgent, { structuredOutput: { schema: articleSchema } })` replaces wrapping in `createStep()`. It takes the same options as `createStep(agent, options)`, plus an agent ID string in place of the instance. It records a declarative entry in the workflow graph, so workflows built this way can be persisted as dynamic workflows.

## Call a tool inside execute()
```typescript
const response = await testTool.execute?.({ text }, { requestContext })
if (!response || isValidationError(response)) {
  throw new Error('testTool did not return a result')
}
```
`isValidationError` is imported from `@mastra/core/tools`.

## Tool as a step
`const step2 = createStep(testTool)`. Use it when the previous step's output matches the tool's input; otherwise insert `.map()` to reshape it (for example `.then(step1).map(async ({ inputData }) => ({ text: inputData.formatted })).then(step2)`).

## The .tool() shorthand
`createWorkflow({}).then(step1).tool(testTool).commit()`. It accepts a tool instance or a registered tool ID string, plus step-level `retries` and `metadata`. Like `.agent()`, it records a declarative entry so the workflow can be persisted as a dynamic workflow.

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.

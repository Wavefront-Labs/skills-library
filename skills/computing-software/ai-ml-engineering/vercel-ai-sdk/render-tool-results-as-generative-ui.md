---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.render-tool-results-as-generative-ui
name: render-tool-results-as-generative-ui
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [generative-ui, tools, usechat, react-components, tool-parts, vercel-ai-sdk]
level: practitioner
status: docs-checked
description: "Connect a streamText tool to a React component by rendering typed tool-NAME parts from useChat by state, and extend the pattern with more tools."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-ui/generative-user-interfaces
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Render tool results as generative UI

Goal: when the model calls a tool, show a React component fed by the tool's output instead of plain text.

## Steps

1. Define tools in `ai/tools.ts` with `tool` from `ai` (imported as `createTool`), a Zod `inputSchema`, and an `execute` whose return value becomes the component props:
   ```ts
   export const weatherTool = createTool({
     description: 'Display the weather for a location',
     inputSchema: z.object({ location: z.string().describe('The location to get the weather for') }),
     execute: async ({ location }) => ({ weather: 'Sunny', temperature: 75, location }),
   });
   export const tools = { displayWeather: weatherTool };
   ```
2. Pass them to the route: `streamText({ model, instructions, messages: await convertToModelMessages(messages), stopWhen: isStepCount(5), tools })` and return `createUIMessageStreamResponse({ stream: toUIMessageStream({ stream: result.stream }) })`.
3. Build a component whose props match the tool's return value (`temperature`, `weather`, `location`).
4. In `page.tsx`, map `message.parts`. Tool parts are typed `tool-${toolName}`, so the key in `tools` (`displayWeather`) gives `part.type === 'tool-displayWeather'`. Switch on `part.state`:
   ```tsx
   case 'input-available':  return <div>Loading weather...</div>;
   case 'output-available': return <Weather {...part.output} />;
   case 'output-error':     return <div>Error: {part.errorText}</div>;
   default: return null;
   ```
5. Send with `sendMessage({ text: input })` (state held in your own `useState`).

## Adding more tools

Add another entry (for example `getStockPrice: stockTool`), a matching component, and another `if (part.type === 'tool-getStockPrice')` branch. Match the component's props to that tool's return shape.

## Gotchas

- The docs example `execute` sleeps 2 seconds to simulate an API call; replace it with a real call.
- The docs example returns `null` for parts it does not handle and gives each element a `key` (the part `index`).
- The page handles only `input-available`, `output-available` and `output-error`; every other state falls to `default: return null`.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Removed the stopWhen sentence (not on the page) and restated two gotchas as what the docs example does (null for unhandled parts, only three tool states handled).

Method: documentation only; no commands were run.

---
id: computing-software.ai-ml-engineering.mastra.agent-browser-providers
name: agent-browser-providers
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, browser, screencast, agentbrowser, stagehand, firecrawl, cdp, recording]
level: advanced
status: docs-checked
description: "Give a Mastra agent a browser: choose AgentBrowser, Stagehand, Firecrawl or BrowserViewer, connect cloud/CDP browsers, configure screencast and session recording."
sources:
  - https://mastra.ai/docs/browser
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: attach browser automation to a Mastra agent and configure provider, cloud connection, screencast and recording.

## Providers
- SDK providers (tools given to the agent directly): `AgentBrowser` (`@mastra/agent-browser`, Playwright, finds elements by accessibility info; general automation/scraping), `StagehandBrowser` (`@mastra/stagehand`, AI-located elements via natural language), `FirecrawlBrowser` (`@mastra/browser-firecrawl`, AgentBrowser tools in hosted Firecrawl sessions).
- CLI provider: `BrowserViewer` launches Chrome and passes its CDP URL to CLI tools such as agent-browser, browser-use and browse; for workspace agents using shell commands.

## Quickstart
```bash
npm install @mastra/agent-browser
```
```typescript
import { AgentBrowser } from '@mastra/agent-browser'
export const browser = new AgentBrowser({ headless: false })
```
```typescript
import { Agent } from '@mastra/core/agent'
export const webAgent = new Agent({
  id: 'web-agent',
  name: 'Web Agent',
  description: 'A web automation assistant that can navigate websites and complete tasks.',
  model: 'openai/<model>',
  browser,
  instructions: 'You are a web automation assistant. Use browser tools to navigate websites and complete tasks.',
})
```
The agent automatically receives all of the provider's browser tools.

## Cloud and CDP
```typescript
new FirecrawlBrowser({ apiKey: process.env.FIRECRAWL_API_KEY })
new StagehandBrowser({ env: 'BROWSERBASE', apiKey: process.env.BROWSERBASE_API_KEY, projectId: process.env.BROWSERBASE_PROJECT_ID })
new AgentBrowser({ cdpUrl: `wss://connect.browser-use.com?apiKey=${process.env.BROWSER_USE_API_KEY}` })  // Browser Use Cloud
new AgentBrowser({ cdpUrl: process.env.BROWSER_CDP_URL, headless: true })  // any CDP endpoint
```

## Screencast
Providers stream a live feed to Mastra Studio. It needs WebSockets: `npm install ws @hono/node-ws`. These are not bundled because they are incompatible with serverless environments like Cloudflare Workers; without them screencast is disabled and everything else works. Enabled by default; configure:
```typescript
new AgentBrowser({ screencast: { format: 'jpeg', quality: 80, maxWidth: 1280, maxHeight: 720 } })
```

## Recording
AgentBrowser and StagehandBrowser: set `recording.outputDir` to add recording tools.
```typescript
new AgentBrowser({ recording: { outputDir: join(process.cwd(), 'browser-recordings') } })
```
The agent uses `browser_record` (start/check/stop) and `browser_record_caption` (label actions). A custom `outputPath` may be absolute or cwd-relative and must resolve inside `outputDir`. Format is Motion-JPEG AVI, no `ffmpeg` needed. Defaults/limits: 30 s default max duration, 120 s hard cap, 1024 x 720 max frame size, captions up to 80 characters, one active recording per process.

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. Removed invented package name and placeholder model string. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.

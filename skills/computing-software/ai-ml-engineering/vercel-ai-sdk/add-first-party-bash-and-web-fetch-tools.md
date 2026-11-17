---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.add-first-party-bash-and-web-fetch-tools
name: add-first-party-bash-and-web-fetch-tools
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [tools, bash-tool, web-fetch-tool, sandbox, secure-fetching]
level: practitioner
status: docs-checked
description: "Give an agent the first-party bash tool in a sandbox session and the web fetch tool, with timeouts, domain allowlists and prompt-injection safeguards."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/tools
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: add ready-made `@ai-sdk/tool-*` tools to `generateText`, `streamText` or `ToolLoopAgent`. Both need Node.js 22.13 or newer and a model with function calling.

## Bash tool
Install `ai @ai-sdk/tool-bash` plus a sandbox adapter (`@ai-sdk/sandbox-just-bash` in memory, `@ai-sdk/sandbox-vercel`, or your own `Experimental_SandboxSession`).
```ts
import { createJustBashNetworkSandboxSession } from '@ai-sdk/sandbox-just-bash';
import { experimental_createBashTool as createBashTool } from '@ai-sdk/tool-bash';
import { generateText, isStepCount } from 'ai';

const session = await createJustBashNetworkSandboxSession();
try {
  const sandbox = session.restricted();
  await sandbox.writeTextFile({ path: 'notes.txt', content: 'Apples: 10\nPears: 20\n' });
  const bash = await createBashTool({ sandbox, timeout: 10_000 });
  const result = await generateText({
    model, tools: { bash }, stopWhen: isStepCount(5),
    prompt: 'Read notes.txt and write a summary to summary.txt.',
  });
  console.log(await sandbox.readTextFile({ path: 'summary.txt' })); // null if missing
} finally { await session.destroy(); }
```
Options: `sandbox` (required), `workingDirectory` (absolute; created if needed), `maxOutputLength` (default 30000 characters per stream), `timeout` (ms per command, 1 to 2147483647, none by default). The model calls with `{ command }` and gets `{ stdout, stderr, exitCode }`; nonzero exit codes are returned so it can recover. Vercel Sandbox: wrap a native sandbox with `createVercelSandboxSessionFromNativeSandbox`, or use `createVercelNetworkSandboxSession()` and pass `session.restricted()`.

## Web fetch tool
Install `ai @ai-sdk/tool-web-fetch`.
```ts
import { experimental_createWebFetchTool as createWebFetchTool } from '@ai-sdk/tool-web-fetch';
const result = await generateText({
  model, tools: { webFetch: createWebFetchTool({ allowedDomains: ['ai-sdk.dev'], requireUrlInUserMessage: true }) },
  stopWhen: isStepCount(5), prompt: 'Summarize https://ai-sdk.dev/docs/introduction.',
});
```
Options: `allowedDomains` (cannot combine with `blockedDomains`; also applies to redirects), `blockedDomains`, `requireUrlInUserMessage` (default false), `maxLength` (50000), `maxBytes` (10 MiB), `timeout` (30000 ms), `fetch`, `defuddleOptions` (for example `contentSelector: 'article'`). Results are `{ type: 'document', ... nextOffset? }` or `{ type: 'error', ... }`; the model re-calls with `offset` to read long pages.

## Gotchas
- Both are `experimental_` exports and rename on import.
- You create, reconnect and destroy the sandbox; tools on the same session share files, and creating a tool does not reset them.
- Output truncation happens after execution; it does not limit command memory or duration. Timeout is per command, and the sandbox must honor cancellation.
- Fetched content is untrusted and may carry prompt injections or exfiltration instructions. Restrict with `allowedDomains`, `requireUrlInUserMessage`, or tool approval.
- `requireUrlInUserMessage` ignores URLs in tool results, so the model cannot follow links from fetched pages.
- No JavaScript runs, and PDFs, images, audio and video are unsupported.
- A custom `fetch` must validate resolved addresses itself. Off Node.js only the URL is validated, so restrict egress at the platform level.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. No content change needed.

Method: documentation only; no commands were run.

---
id: computing-software.ai-ml-engineering.llm-application-engineering.claude-agent-sdk
name: claude-agent-sdk
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, claude-agent-sdk, agents, agent-harness, mcp, subagents, hooks]
level: practitioner
status: docs-checked
description: "Build agents on the Claude Agent SDK: query() vs ClaudeSDKClient, ClaudeAgentOptions (tools, permissions, MCP, cwd), custom tools, hooks, subagents and hosting it yourself."
sources:
  - https://code.claude.com/docs/en/agent-sdk/overview
  - https://github.com/anthropics/claude-agent-sdk-python
  - https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Claude Agent SDK

**What it is:** the Claude Code agent harness as a library (`claude-agent-sdk` for Python; a TypeScript SDK also exists): agent loop, context management, built-in tools (Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch), permissions, hooks, subagents, sessions and MCP. You host and deploy it.

Not the same as the Messages API tool runner (a thin loop over tools you define) or Managed Agents (Anthropic hosts loop and sandbox).

## Minimal use
```python
import anyio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    options = ClaudeAgentOptions(
        system_prompt="You are a release-notes assistant.",
        allowed_tools=["Read", "Grep", "Glob"],     # auto-approved; use disallowed_tools to block others
        permission_mode="default",
        cwd="./repo", max_turns=20)
    async for message in query(prompt="Summarize changes since tag v1.4 from CHANGELOG and git log.", options=options):
        print(message)
anyio.run(main)
```
`ClaudeSDKClient` supports bidirectional, interactive conversations and, unlike `query()`, also enables custom tools and hooks defined as Python functions. `allowed_tools` is an auto-approve allowlist: unlisted tools fall through to `permission_mode`; it does not remove tools.

## Extending
- **Custom tools:** define with the SDK's `@tool` decorator and expose via an in-process MCP server (`create_sdk_mcp_server`), or connect external MCP servers through `mcp_servers`.
- **Hooks:** run code before/after tool use (e.g. block dangerous Bash commands, log every edit).
- **Subagents:** specialized agents with their own prompts and tool sets for delegation, keeping the main context small.
- **Settings and skills:** project-level instructions and Agent Skills can be loaded like in Claude Code.

## Deployment notes
- Run inside a container or sandbox with only the files and credentials the agent needs.
- Restrict tools per agent; require approval for writes/Bash in sensitive environments.
- Log transcripts for debugging and evaluation; set turn and cost limits.

## Verify
- [ ] Integration test runs the agent against a fixture repo and asserts on outputs and on denied tool attempts.

## Checked
2026-11-01. Confirmed against the Agent SDK overview (capabilities: built-in tools, hooks, subagents, MCP, permissions, sessions, skills; comparison with Client SDK and Managed Agents) and the Python SDK README (`pip install claude-agent-sdk`, `query`, `ClaudeSDKClient`, `ClaudeAgentOptions` fields, `@tool`, `create_sdk_mcp_server`, `allowed_tools` semantics). Removed: the TypeScript package name (not in the cited pages) and the 'least privilege' claim for `allowed_tools`.
Method: documentation only; no commands were run.

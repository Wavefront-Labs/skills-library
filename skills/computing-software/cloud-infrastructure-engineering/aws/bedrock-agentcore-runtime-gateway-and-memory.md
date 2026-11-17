---
id: computing-software.cloud-infrastructure-engineering.aws.bedrock-agentcore-runtime-gateway-and-memory
name: bedrock-agentcore-runtime-gateway-and-memory
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, bedrock, agentcore, ai-agents, agent-runtime, mcp-gateway, agent-memory, agent-observability]
level: practitioner
status: draft
description: "Run AI agents on Bedrock AgentCore: Runtime hosting for any framework, Gateway to expose APIs as MCP tools, Memory, Identity, built-in tools and observability."
sources: ["Amazon Bedrock AgentCore Developer Guide - What is Amazon Bedrock AgentCore", "Amazon Bedrock AgentCore Developer Guide - AgentCore Runtime", "Amazon Bedrock AgentCore Developer Guide - AgentCore Gateway and Memory", "Amazon Bedrock AgentCore starter toolkit documentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bedrock AgentCore

**What it is:** managed building blocks for running agents in production, independent of the agent
framework (Strands, LangGraph, CrewAI, LlamaIndex, custom) and model provider.

## Services
| Component | Does |
|---|---|
| **Runtime** | serverless hosting of agent code with per-session isolation, long-running sessions, streaming, IAM or OAuth inbound auth |
| **Gateway** | turns APIs (OpenAPI specs), Lambda functions and existing MCP servers into MCP tools agents can call, with auth handled |
| **Memory** | short-term (session events) and long-term memory (extracted facts, preferences, summaries) with strategies |
| **Identity** | agent identities; outbound OAuth/API key credentials to third-party services on behalf of users |
| **Code Interpreter** | sandboxed code execution tool |
| **Browser** | managed headless browser tool for web tasks |
| **Observability** | OpenTelemetry traces, metrics and logs into CloudWatch (GenAI observability dashboards) |

## Runtime: minimal agent
```python
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent
app = BedrockAgentCoreApp()
agent = Agent()
@app.entrypoint
def invoke(payload):
    return {"result": str(agent(payload.get("prompt", "")))}
if __name__ == "__main__":
    app.run()
```
With the starter toolkit:
```bash
pip install bedrock-agentcore bedrock-agentcore-starter-toolkit strands-agents
agentcore configure --entrypoint agent.py      # creates config, ECR repo and execution role settings
agentcore launch                               # builds an ARM64 container and deploys to Runtime
agentcore invoke '{"prompt": "Summarise the last incident"}'
```
Applications then call `InvokeAgentRuntime` with a session id to keep conversation context.

## Production concerns
- Execution role least privilege: only the models, tools and data the agent needs.
- Gateway inbound auth (OAuth/Cognito or IAM) and outbound credentials via Identity; do not embed API keys in agent code.
- Memory retention and PII: decide what is stored long-term; namespaces per user.
- Observability: enable CloudWatch Transaction Search to see agent traces; alarm on errors and latency per agent.
- Evaluate agents (task success, tool-call accuracy) before and after changes; guardrails on inputs/outputs.

## Gotchas
- Pricing is consumption-based per component (compute time, memory events, gateway calls); idle sessions cost little but long sessions accumulate.
- Region availability is limited; check before designing.
- Container must expose the expected HTTP contract (`/invocations`, `/ping`) if built without the SDK.

## Verify
- [ ] Agent deployed to Runtime answers via `InvokeAgentRuntime`; traces visible in CloudWatch.
- [ ] Gateway tool call succeeds with OAuth; memory recall works across sessions for the same user.

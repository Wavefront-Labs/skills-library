---
id: computing-software.cybersecurity-defensive.application-security.ai-coding-assistant-security
name: ai-coding-assistant-security
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [ai-coding-assistant-security, copilot, llm, secure-coding, slopsquatting, prompt-injection, coding-agents]
level: practitioner
status: draft
description: "Use AI coding assistants and agents safely: data exposure settings, reviewing generated code, hallucinated packages, agent permissions, prompt injection and policy."
sources: ["https://genai.owasp.org/llm-top-10/", "https://docs.github.com/en/copilot/managing-copilot/managing-github-copilot-in-your-organization", "https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Secure use of AI coding assistants

## Risks
1. **Insecure suggestions**: generated code reproduces common vulnerable patterns (string-built SQL, missing
   authorisation checks, weak crypto, disabled TLS verification). Studies of assistants found a substantial
   share of security-relevant suggestions vulnerable.
2. **Hallucinated dependencies (slopsquatting)**: models suggest package names that do not exist; attackers
   register them.
3. **Data exposure**: code, secrets and customer data sent to the provider; retention and training terms.
4. **Agentic tools**: assistants that run shell commands, edit files and open PRs can be steered by **prompt
   injection** in repo content, issues, web pages or dependency READMEs, and can exfiltrate secrets from the
   environment.
5. **Licence and provenance**: verbatim reproduction of licensed code.

## Controls
- **Enterprise tier** with no training on your data and defined retention; content exclusions for sensitive
  repos/paths (e.g. Copilot content exclusion); block personal accounts on corporate code.
- **Same review bar**: AI-written code gets the same PR review, SAST, SCA and tests as human code; mark
  AI-heavy PRs for reviewers if your policy asks.
- **Dependency checks**: verify every new package exists, has history and maintainers; registry proxy with
  allowlist or age/popularity rules; lockfiles.
- **Agent sandboxing**: run agents in containers/VMs or ephemeral dev environments without production
  credentials; least-privilege tokens (read-only where possible); require human approval for commands that
  touch network, secrets or git push; allowlist tools.
- **Secrets**: keep `.env` and credentials out of the agent's readable workspace; push protection on.
- **Prompt hygiene**: instruct assistants with your secure coding standard (repo instruction files), but do
  not rely on that as a control.
- **Public code filter** (duplication detection) on where licence risk matters.

## Policy essentials
Approved tools list, data classes allowed, review requirements, prohibited uses (pasting customer data or
secrets), reporting of suspicious agent behaviour.

## Verify
SAST runs on all PRs regardless of author; an agent session cannot read production secrets or push to
protected branches; new dependencies in PRs are flagged for existence and reputation checks.

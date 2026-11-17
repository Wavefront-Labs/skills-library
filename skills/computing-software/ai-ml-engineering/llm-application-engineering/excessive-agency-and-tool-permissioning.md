---
id: computing-software.ai-ml-engineering.llm-application-engineering.excessive-agency-and-tool-permissioning
name: excessive-agency-and-tool-permissioning
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, guardrails, excessive-agency, tool-permissions, least-privilege, human-approval, agent-security]
level: practitioner
status: docs-checked
description: "Limit what LLM agents can do: minimal tool sets, scoped per-user credentials, approval gates, rate and value limits, sandboxing and audit logging."
sources:
  - https://genai.owasp.org/llmrisk/llm062025-excessive-agency/
  - https://www.anthropic.com/engineering/claude-code-sandboxing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Excessive agency and tool permissioning

OWASP LLM06 breaks excessive agency into **excessive functionality** (tools the task does not need), **excessive permissions** (tools with broader rights than needed) and **excessive autonomy** (high-impact actions without confirmation). Any of them turns a hallucination or prompt injection into real damage.

## Controls
OWASP's mitigations, in order:
1. **Minimize extensions and their functionality:** give each agent only the tools its task needs (a mailbox summariser needs read, not delete or send); drop tools left over from development. **Avoid open-ended extensions** (run a shell command, fetch a URL): use granular ones, e.g. a specific file-writing tool instead of a shell, or `get_order_status(order_id)` instead of a generic `run_sql`.
2. **Minimize permissions:** a recommender needs read access to a products table only, enforced by database permissions on the identity the tool connects with (no INSERT, UPDATE or DELETE for a read tool).
3. **Execute in the user's context:** actions on a user's behalf run downstream as that user with minimum privileges (for example OAuth with minimum scope), not as a generic high-privileged identity.
4. **Require user approval** (human in the loop) for high-impact actions, implemented in a downstream system or inside the extension that performs the operation (for example the 'post' tool of a social-media agent). Show the exact action and arguments.
5. **Complete mediation:** enforce authorization in downstream systems against security policy rather than relying on the LLM to decide whether an action is allowed. In practice: hard limits in tool code (max refund amount, max recipients, allowed domains); the model cannot talk its way past a check in the tool implementation.
6. **Sanitise LLM inputs and outputs** (OWASP ASVS, SAST/DAST/IAST in pipelines).
Damage limiters per OWASP: **log and monitor** extension and downstream activity, and **rate-limit** to reduce undesirable actions per period and give monitoring time to catch them.

Additional practice:
- **Separate read and write tools**, so approval policy can differ (practitioner advice).
- **Sandboxing:** Anthropic's Claude Code sandboxing post says effective sandboxing needs both filesystem isolation (access limited to specific directories) and network isolation (only approved servers): without network isolation a compromised agent can exfiltrate files such as SSH keys, without filesystem isolation it can escape the sandbox. Claude Code's own model is permission-based: read-only by default, asking before modifications or commands, with a few safe commands auto-allowed. Keep credentials out of the sandbox where possible.

## Example policy table
| Tool | Risk | Policy |
|---|---|---|
| `search_kb` | low | auto |
| `get_customer` | medium (PII) | auto, scoped to the caller's account |
| `issue_refund` | high | auto <= 50 EUR, else human approval; 3/day/customer |
| `send_email` | high | draft only; human sends |
| `delete_account` | critical | not available to the agent |

## Verify
- [ ] Inventory of tools with risk level and policy reviewed per release.
- [ ] Tests attempt over-limit and out-of-scope actions (including via injected instructions) and confirm the tool layer refuses.
- [ ] Audit log reconstructs any action back to user request and approval.

## Checked
Method: docs-checked 2026-11-09 against the OWASP LLM06:2025 Excessive Agency page (read through the mitigation section) and the Anthropic engineering post on Claude Code sandboxing (read in full). Dropped: the Claude tool-use overview source (not read), the LangGraph `interrupt` and Managed Agents `always_ask` references, and the immutable-audit-log wording (OWASP only says log and monitor). The policy table is an illustrative example, not sourced.

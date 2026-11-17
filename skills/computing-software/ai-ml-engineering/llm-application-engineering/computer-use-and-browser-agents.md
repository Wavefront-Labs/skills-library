---
id: computing-software.ai-ml-engineering.llm-application-engineering.computer-use-and-browser-agents
name: computer-use-and-browser-agents
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, agents, computer-use, browser-agents, playwright, gui-automation, agent-sandbox]
level: practitioner
status: docs-checked
description: "Build computer-use and browser agents safely: Claude computer use toolset in an isolated VM, screenshot/action loops, DOM-first alternatives, approval controls."
sources:
  - https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Computer use and browser agents

## Prefer APIs, then DOM, then pixels
1. A real API or MCP server for the target system: fastest, most reliable.
2. Browser automation via the DOM or accessibility tree - typically more robust and cheaper in tokens than screenshots.
3. Pixel-level computer use (screenshots + mouse/keyboard) for legacy desktop apps, canvas UIs and sites without usable DOM.

## Claude computer use
- Claude 5.5 and later models use the **`computer_toolset_20260801`** toolset, declared as `{"type": "computer_toolset_20260801"}` in `tools` with no beta header. They return a 400 for any computer use tool version they do not accept, such as `computer_20251124` on the Claude API. Opus 4.7, Opus 4.6, Sonnet 4.6 and Opus 4.5 support computer use only through `computer_20251124`, which needs a beta header. The toolset cannot be declared alongside a `computer_20251124` entry.
- Your code runs the loop: iterate over every `tool_use` block in order, dispatch on the member `name` together with `toolset_name`, perform the action on your container or VM, and return the result (a screenshot) in a `tool_result` that echoes `toolset_name`. Leaving any block in a batch unanswered is rejected with `invalid_request_error`; run batched actions sequentially and stop at the first failure.
- Run inside a **dedicated virtual machine or container with minimal privileges**. The docs describe a sandboxed environment with a virtual X11 display (Xvfb) that renders the desktop Claude sees as screenshots.
- Coordinates are in the pixel space of the screenshots you return. If your screen exceeds the image limits, resize each screenshot (docs example: long edge at most 1568 px and about 1.15 million total pixels) and scale Claude's coordinates back; mismatched scaling causes misclicks.
- Failed actions (screenshot capture error, out-of-bounds coordinates) should return a tool result with an error message saying what went wrong.

## Safety
- **Prompt injection from the screen:** instructions on web pages or in images can override your instructions. The docs recommend a dedicated VM or container with minimal privileges, no access to sensitive data (such as account logins), an allowlist of domains for internet access, and human confirmation for decisions with real-world consequences or affirmative consent (accepting cookies, financial transactions, terms of service). Anthropic also runs classifiers over tool returns such as screenshots that steer the model to check whether an instruction really came from you.
- Logging in raises prompt-injection risk; review the Mitigate jailbreaks and prompt injections guide before giving the model credentials. Practitioner advice: prefer scoped accounts or hand control to the user.
- Record sessions (screenshots + actions) for audit and debugging (practitioner advice).

## Reliability tips
- Prompt Claude to take a screenshot after each step and evaluate whether it achieved the right outcome before moving on; it can otherwise act as if actions succeeded without checking.
- If dropdowns or scrollbars are hard to manipulate with the mouse, prompt the model to use keyboard shortcuts.
- Provide task-specific hints (where things are, expected screens) in the system prompt (practitioner advice).
- Set max steps and a wall-clock timeout; on failure return a structured status, not silence (practitioner advice).

## Verify
- [ ] Agent runs in an isolated environment with egress allowlist; host filesystem not mounted.
- [ ] Eval of 20+ representative tasks with success rate, steps and cost per task.
- [ ] Consequential actions pause for approval in tests.

## Checked
Method: docs-checked 2026-11-09 against the Claude computer-use-tool page (platform.claude.com, markdown version; availability, safety, loop, scaling and prompting-tip sections read by keyword search). Dropped: the quickstart demo (Docker, VNC) details, Playwright and OpenAI computer-use claims and sources (not read), the 1280x800 resolution suggestion, and the context editing advice. The API, then DOM, then pixels ordering is practitioner guidance.

---
id: computing-software.ai-ml-engineering.open-webui.enable-python-code-interpreter-and-pyodide
name: enable-python-code-interpreter-and-pyodide
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [open-webui, code-execution, pyodide, code-interpreter, matplotlib]
level: practitioner
status: docs-checked
description: "Enable the Open WebUI code interpreter and manual Run button on Pyodide, use /mnt/uploads files, show matplotlib charts inline and handle the Edge crash."
sources:
  - https://docs.openwebui.com/features/chat-conversations/chat-features/code-execution/python
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Enable the Python code interpreter (Pyodide)

Goal: let models run Python, and let users run code blocks, without extra servers. Pyodide and Jupyter engines are legacy; Open Terminal is the recommended route for real workloads.

## Two features
- **Run button** on code blocks: controlled only by `ENABLE_CODE_EXECUTION`; every user gets it. Runs in the browser (Pyodide) unless `CODE_EXECUTION_ENGINE=jupyter`.
- **Code Interpreter**: model capability. Enable per model in Settings > Admin > Models > model > Capabilities > Code Interpreter. Global switches: Settings > Admin > Code Execution, or `ENABLE_CODE_INTERPRETER` (default true), `CODE_INTERPRETER_ENGINE` (`pyodide` default or `jupyter`), `CODE_INTERPRETER_PROMPT_TEMPLATE`, `CODE_INTERPRETER_BLOCKED_MODULES` (comma-separated; only blocks direct top-level imports, not a security boundary).

## Native mode
In Native function calling (the default) the interpreter is the builtin tool `execute_code`; it needs the global flag, the model capability and Native mode (not Legacy). Interpreter tags written by a Native-mode model are shown as text, not run.

## Files
With Pyodide, `/mnt/uploads/` is a persistent virtual filesystem (IDBFS). Attached files are mounted there automatically; a Files tab appears in the chat side panel for browse/upload/download. Persistence across page reloads needs `ENABLE_PYODIDE_FILE_PERSISTENCE=true` (off by default). Jupyter has no such mount or panel.

## Inline charts
Print a base64 data URL; Open WebUI uploads it and swaps in a file URL like `/api/v1/files/{id}/content` which the model embeds as markdown:
```python
buf = io.BytesIO()
plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
buf.seek(0)
print(f"data:image/png;base64,{base64.b64encode(buf.read()).decode()}")
plt.close()
```
`plt.show()` shows nothing. Raw base64 in the reply means the model echoed it instead of using the converted URL.

## Library limits
Included, auto-detected from imports and loaded on demand: micropip, requests, beautifulsoup4, numpy, pandas, matplotlib, seaborn, scikit-learn, scipy, regex, sympy, tiktoken, pytz, openpyxl, python-pptx, python-docx. Nothing else can be installed (no torch, tensorflow, opencv, psycopg2).

## Gotchas
- Edge crashing with `STATUS_ACCESS_VIOLATION`: turn off "Enhance your security on the web" at `edge://settings/privacy/security`, use Chrome/Firefox, or switch the engine to jupyter.
- Stuck "Analyzing..." spinner: timeout or error; check backend logs.

## Checked
2026-11-04. Confirmed against the Open WebUI docs page features/chat-conversations/chat-features/code-execution/python (read in full): the legacy-engine caution, Run button controlled by ENABLE_CODE_EXECUTION alone, the model capability steps and admin panel, the four env variables and defaults, native mode requirements and execute_code, tags shown as text, /mnt/uploads IDBFS behaviour with opt-in ENABLE_PYODIDE_FILE_PERSISTENCE, the Files tab and Jupyter exclusion, the base64 chart pattern and URL swap, the library list and no-install warning, the Edge STATUS_ACCESS_VIOLATION fixes and the stuck spinner row. Reworded the library loading phrase to match the page.
Method: documentation only; no commands were run.

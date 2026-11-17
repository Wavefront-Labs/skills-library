---
id: computing-software.ai-ml-engineering.litellm.litellm-proxy-debug-logging
name: litellm-proxy-debug-logging
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, litellm-log, detailed-debug, proxy-debugging]
level: intro
status: docs-checked
description: "Turn on proxy debug output with --debug, --detailed_debug or the LITELLM_LOG environment variable."
sources:
  - https://docs.litellm.ai/docs/proxy/quick_start
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: see what the proxy is doing.

CLI flags:

```
litellm --model gpt-6-luna --debug            # events during normal operation
litellm --model gpt-6-luna --detailed_debug   # detailed information
```

Environment variable:

```
export LITELLM_LOG=INFO    # normal operation
export LITELLM_LOG=DEBUG   # detailed information
export LITELLM_LOG=ERROR   # errors only
```

LITELLM_LOG must be a valid Python logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).

Failure mode: setting LITELLM_LOG to None makes `import litellm` fail.

Where the flags fit: `--detailed_debug` is also shown on the quick start page as the way to get detailed debug logs when the proxy runs with a single `--model`, and both flags combine with `--config`, for example:

```
litellm --config config.yaml --detailed_debug
```

Other useful checks from the same page: `litellm --test` sends a test chat completion, and GET /models lists the models the proxy exposes.

## Checked

2026-11-03. Confirmed on the proxy quick start page (docs.litellm.ai/docs/proxy/quick_start): --debug, --detailed_debug, LITELLM_LOG levels, the valid Python logging levels and the failure when set to None, litellm --test and GET /models. Removed an unconfirmed recommendation paragraph.

Method: documentation only; no commands were run.

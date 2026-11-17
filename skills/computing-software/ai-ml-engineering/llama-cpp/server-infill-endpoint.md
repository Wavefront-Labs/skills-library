---
id: computing-software.ai-ml-engineering.llama-cpp.server-infill-endpoint
name: server-infill-endpoint
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, infill, fill-in-the-middle, code-completion, fim]
level: advanced
status: docs-checked
description: "Code completion with POST /infill: prefix, suffix, extra context files and how the prompt is built with or without repo-level FIM tokens."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# POST /infill

Takes a prefix and a suffix and returns the predicted completion as a stream.

Fields:

- `input_prefix`: prefix of the code to infill.
- `input_suffix`: suffix of the code to infill.
- `input_extra`: additional context inserted before the FIM prefix; an array of `{"filename": string, "text": string}` objects.
- `prompt`: added after the FIM_MID token.
- The endpoint also accepts all the options of `/completion`.

Prompt layout depends on the model's tokens. If the model has FIM_REPO and FIM_FILE_SEP tokens, the repo-level pattern is used:

```
<FIM_REP>myproject
<FIM_SEP>{chunk 0 filename}
{chunk 0 text}
<FIM_SEP>filename
<FIM_PRE>[input_prefix]<FIM_SUF>[input_suffix]<FIM_MID>[prompt]
```

If those tokens are missing, the extra context is simply prefixed at the start: `[input_extra]<FIM_PRE>[input_prefix]<FIM_SUF>[input_suffix]<FIM_MID>[prompt]`.

```bash
curl http://localhost:9931/infill -H "Content-Type: application/json" -d '{
  "input_prefix": "def add(a, b):\n    ",
  "input_suffix": "\n\nprint(add(1, 2))",
  "input_extra": [{"filename": "util.py", "text": "# helpers"}],
  "n_predict": 64 }'
```

Server flag `--spm-infill` uses the Suffix/Prefix/Middle pattern instead of Prefix/Suffix/Middle, as some models prefer this (default disabled).

The `/completion` field `t_max_predict_ms` is described there as useful for FIM: a generation time limit in ms, measured from the first token and triggering only once a newline has been generated.

## Checked

Date: 2026-11-08. Confirmed against the /infill section, the `--spm-infill` flag and the `t_max_predict_ms` entry of the llama-server README. Corrected: a model without FIM_REPO/FIM_FILE_SEP tokens does not fail; the extra context is simply prefixed. Removed the claim that `--spm-infill` should be used only for models trained that way (the page says only that some models prefer it).

Method: docs-only read of cited pages, 2026-11-08

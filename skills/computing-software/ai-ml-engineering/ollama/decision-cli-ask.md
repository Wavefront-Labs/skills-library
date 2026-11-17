---
id: computing-software.ai-ml-engineering.ollama.decision-cli-ask
name: decision-cli-ask
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [decision-model, ask, choice, level]
level: practitioner
status: docs-checked
description: "Classify text from the terminal with ollama run nimble --ask, --choice, --level and --format json."
sources:
  - https://docs.ollama.com/capabilities/decision.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get a yes/no, label or score from a shell pipeline.

Setup: Ollama v0.35.0 or later, then `ollama pull nimble`. Nimble and Tev1 are decision models; Clef and Clef Flash also judge images and need v0.35.1 or later. Local requests need no API key.

Each question is `--ask`, answered yes or no unless you attach labels (`--choice`) or scale levels (`--level`):

```
ollama run nimble --ask "Is a refund being requested?" < ticket.txt
ollama run nimble --ask "Which team should handle this?" \
  --choice billing="Payments and refunds" \
  --choice technical="Software problems" < ticket.txt
ollama run nimble --ask "How urgent is this?" \
  --level "Routine" --level "Soon" --level "Immediate" < ticket.txt
```

List levels from lowest to highest. Several `--ask` options run in one call. Input can be text or JSON; with JSON, refer to fields in backticks, as in `Is a refund being requested in \`body\`?`.

Output is one line per answer: the likelier answer with its probability, a label with its probability, or a score such as `Soon 64% 1.2 / 2`.

Judge an image with Clef: `ollama run clef ./receipt.png --ask "Is this a restaurant receipt?"`.

`--format json` prints the full response. Without a state, `ollama run nimble` opens a prompt where the first message is the state and each later line is a yes/no question; `/clear` starts over. With `--ask`, each interactive message is a new state to answer those questions about.

## Checked

Method: 2026-11-08 read the full decision capability page. Claims matched; dropped the cli.md source (not needed, not read in full) and added the interactive `--ask` behaviour.

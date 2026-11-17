---
id: computing-software.ai-ml-engineering.llama-cpp.gbnf-grammar-syntax
name: gbnf-grammar-syntax
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, gbnf, grammar, constrained-output, grammar-flags]
level: practitioner
status: docs-checked
description: "Write GBNF grammars to constrain model output and pass them with --grammar, --grammar-file or the API."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md", "https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GBNF grammars

GBNF (GGML BNF) constrains model output; it extends BNF with regex-like features. Rules have the form `nonterminal ::= sequence...`, and `root` is the start rule, defining what the entire output must match.

```
root ::= ("- " item)+
item ::= [^\n]+ "\n"
```

Syntax:

- Non-terminals (rule names) must be a dashed lowercase word, such as `move`, `castle` or `check-mate`.
- Terminals are code points: quoted sequences like `"O-O"`, ranges like `[1-9]` or `[NBKQR]`, negated ranges like `[^\n]`. Unicode can be written directly (`[ぁ-ゟ]`) or with escapes `\xXX`, `\uXXXX`, `\UXXXXXXXX`.
- `|` alternatives, `( )` grouping.
- Repetition: `*` (same as `{0,}`), `+` (`{1,}`), `?` (`{0,1}`), `{m}` exactly m, `{m,}` at least m, `{m,n}` between m and n, `{0,n}` at most n.
- Tokens: `<[1000]>` matches the token with that ID; `<think>` matches the token whose text is exactly that string (it must be a single token in the vocabulary or the grammar fails to parse); `!<[1000]>` or `!<think>` matches any token except that one.
- `#` starts a comment. Newlines are allowed between rules and inside parentheses, and a newline after `|` continues the current rule.

Performance: writing `x? x? x?` N times can make sampling extremely slow; use `x{0,N}` instead.

Use:

```bash
./llama-cli -m <model> --grammar-file grammars/some-grammar.gbnf -p 'Some prompt'
```

- llama-cli and llama-completion: `--grammar` and `--grammar-file`.
- llama-server completion endpoints: the `grammar` body field; the server README also lists `--grammar` and `--grammar-file`. Invalid grammar sent to the completions endpoint returns an error with code 400, message `Failed to parse grammar`, type `invalid_request_error`.
- `test-gbnf-validator` tests a grammar against strings.
- JSON schemas can be converted to grammars (see the json-schema-constrained-output skill).

## Checked

Date: 2026-11-08. Confirmed against the GBNF guide and the llama-server README (flags, error response). Removed: the arithmetic example grammar (written for this skill, not from the page), and the explicit `\t` escape claim (only `\n` and `\t` appear in page examples, not in an escape list).

Method: docs-only read of cited pages, 2026-11-08

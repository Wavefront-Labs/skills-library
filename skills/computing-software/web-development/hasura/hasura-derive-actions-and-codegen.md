---
id: computing-software.web-development.hasura.hasura-derive-actions-and-codegen
name: hasura-derive-actions-and-codegen
category: computing-software
field: web-development
product: hasura
tags: [hasura, actions, derive, codegen, cli]
level: intro
status: docs-checked
description: "Derive a Hasura Action from an existing mutation with --derive-from and generate handler boilerplate with hasura actions use-codegen."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/actions/derive.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/actions/codegen/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: start an action from a mutation you already have, and scaffold the handler.

Derive: write the mutation you want to wrap, using variables for its arguments, then derive an action from it:

```bash
hasura actions create insertAuthor --derive-from 'mutation insertAuthor($name: String) { insert_author_one(object: { name: $name }) { id name } }'
```
This opens an editor on `metadata/actions.graphql` with the action types auto-filled. In the Console, paste the query in GraphiQL (`API` tab) and use the Derive action button. The derived output type comes from the original operation's output type.

Codegen: run

```bash
hasura actions use-codegen
```
and answer prompts for the framework, whether to clone a starter kit, and the output directory. Choices are written to the CLI `config.yaml` under `actions.codegen` (`framework`, `output_dir`). Then `hasura actions codegen <action-name>` generates the files at `output_dir`.

Console path: `Actions -> [action-name] -> Codegen` tab, where you pick a framework to see handler boilerplate.

Gotcha: the CLI does not persist information about derived actions, so to generate delegation code for one, pass the operation again: `hasura actions codegen <action-name> --derive-from '<query/mutation string>'`.

## Checked

2026-11-04. Confirmed against the cited pages: derive and codegen pages: derive flow in Console and CLI, `insert_author_one` example, actions.graphql editor, use-codegen prompts, config.yaml codegen keys, Codegen tab, --derive-from on codegen. Removed or corrected: wrong example field `insert_authors_one`, the adapt-for-validation advice, the securing gotcha and the Verify step.

Method: documentation only; no commands were run.

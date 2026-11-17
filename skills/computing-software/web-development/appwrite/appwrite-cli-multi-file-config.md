---
id: computing-software.web-development.appwrite.appwrite-cli-multi-file-config
name: appwrite-cli-multi-file-config
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, cli, configuration, includes, monorepo]
level: advanced
status: docs-checked
description: "Split a large appwrite config into multiple files with the includes key available from CLI 20.0.0."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/tooling/command-line/installation/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/tooling/command-line/commands/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep big projects maintainable.

From CLI version 20.0.0 the single `appwrite.config.json` can be split: add an `includes` object whose keys name a top-level resource array and whose values are paths to JSON files. Each included file contains the JSON array that would normally live under that key.

```json
{
  "projectId": "<PROJECT_ID>",
  "endpoint": "https://<REGION>.cloud.appwrite.io/v1",
  "includes": {
    "functions": "./appwrite/functions.json",
    "topics": "./appwrite/topics.json"
  }
}
```

Supported include keys: `functions`, `sites`, `databases`, `tablesDB`, `tables`, `topics`, `teams`, `buckets`, `webhooks`, `messages`.

Include path rules: local JSON files inside your project, relative paths ending in `.json`; no parent-directory segments, absolute paths, URLs, URL-like schemes, null bytes or JSON pointer fragments.

Resource paths: the CLI resolves a resource's `path` (for example a function's) relative to the file that defines it. If `functions` is included from `./appwrite/functions.json`, the function path resolves from `./appwrite/`, not from the folder with the root config.

Compatibility: the single-file format still works, and you can split arrays over time while keeping others in the root config. The `init`, `pull`, `push` and `run` commands support multi-file configuration.

Gotcha: because resource paths resolve from the defining file, moving a function array into a subfolder changes how its `path` values are read.

## Checked

2026-11-04. Confirmed against the Appwrite docs pages CLI Installation (Multi-file configuration section) and CLI Commands: version 20.0.0, the `includes` field, the ten supported keys, include path rules, relative resolution of resource paths, single-file compatibility, and the four supporting commands. Replaced the sources: the original cited pages that do not describe `includes` in detail. Removed: the `tables/orders.json` example and the claim that `appwrite push all --all --force` combines with it, which no page states, and the "nested folders per feature" advice.
Method: documentation only; no commands were run.

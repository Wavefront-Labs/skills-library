---
id: computing-software.cloud-infrastructure-engineering.saltstack.top-file-merging-strategy
name: top-file-merging-strategy
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, top-file, top-file-merging-strategy, merge-all, gitfs, saltenv]
level: advanced
status: docs-checked
description: "Choose how Salt combines top files across environments with top_file_merging_strategy (merge, same, merge_all) and avoid stale GitFS tag states."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/ref/states/top.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Top file merging

If an environment is specified (minion `environment` setting or `saltenv`), only that environment's top file is used. With none specified, all environments' top files are processed according to `top_file_merging_strategy`:

- `merge` (default): combine the top files.
- `same`: each environment uses only its own top file.
- `merge_all` (2016.11.0): apply all configured states from all top files, without duplicates.

Related minion options: `state_top_saltenv`, `env_order`, `default_top`.

GitFS warning: each branch and tag is an environment, so old tags can pull in outdated states. Set the strategy to `same`, or use `gitfs_saltenv_whitelist` and `gitfs_saltenv_blacklist`.

```yaml
top_file_merging_strategy: same
```

## Checked

2026-11-04: read the Salt top file reference page in full (How Top Files Are Compiled and the four compilation scenarios). Confirmed merge, same and merge_all behaviour, the 2016.11.0 merge_all note, the related options and the GitFS advice. Nothing removed.

Method: documentation only; no commands were run.


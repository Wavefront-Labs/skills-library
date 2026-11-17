---
id: computing-software.cybersecurity-defensive.authelia.access-control-check-policy-cli
name: access-control-check-policy-cli
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, check-policy, access-control, cli, debugging, rule-testing]
level: practitioner
status: docs-checked
description: "Use authelia access-control check-policy to see which rule matches a URL, method, user, groups and IP, and read its hit, miss and may output."
sources:
  - https://www.authelia.com/reference/cli/authelia/authelia_access-control_check-policy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Instead of guessing why a request gets a policy, ask Authelia offline.

```bash
authelia access-control check-policy --config /path/to/configuration.yml \
  --url https://app.example.com/api/v1 --method GET

authelia access-control check-policy --config /path/to/configuration.yml \
  --url https://app.example.com --username john --groups admin,public --ip 192.0.2.10 --verbose
```

Flags: `--url` (the object), `--method` (defaults to `GET`), `--username`, `--groups` (strings, comma-separated in the examples), `--ip`, `--verbose`, and the global `--config` for configuration files or directories.

Reading the output, per the command's legend:

- `#` is the rule position in the configuration.
- `*` marks the first fully matched rule, which is the one that applies.
- `~` marks a potential match: if the user were authenticated they might match.
- Each criterion column shows `hit`, `miss` or `may`.

Important note from the command help: a rule that potentially matches causes a redirect to one-factor authentication, so Authelia can determine whether the rule really matches.

Suggested practice (not from the page): run it after every rules edit against a regression list of URLs you expect to be denied, bypassed or protected, with the same environment variables as production.

Check: confirm that a URL you intend to leave open shows `bypass` on a `*` row and not `~`.

## Checked

2026-11-08. Read in full: CLI page for access-control check-policy. Added missing --username flag; practice advice labelled.

Method: documentation only; no commands were run.

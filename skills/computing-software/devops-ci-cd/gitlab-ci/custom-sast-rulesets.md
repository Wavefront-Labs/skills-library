---
id: computing-software.devops-ci-cd.gitlab-ci.custom-sast-rulesets
name: custom-sast-rulesets
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, sast-custom-rulesets, ruleset-toml, semgrep-passthrough, sast-rule-override]
level: advanced
status: docs-checked
description: "Tune GitLab SAST with .gitlab/sast-ruleset.toml: disable noisy rules, override severity, replace or extend Semgrep rules via passthroughs, and share rulesets across projects."
sources: ["https://docs.gitlab.com/user/application_security/sast/customize_rulesets/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom SAST rulesets (`ruleset.toml`)

File: `.gitlab/sast-ruleset.toml` in the project, or a remote ruleset via `SAST_RULESET_GIT_REFERENCE` (a local file takes precedence). The customize-rulesets page lists the Ultimate tier.

## 1. Disable or re-rate predefined rules
```toml
[semgrep]
  [[semgrep.ruleset]]
    disable = true
    [semgrep.ruleset.identifier]
      type = "semgrep_id"
      value = "gosec.G107-1"            # find ids in the gl-sast-report.json identifiers

  [[semgrep.ruleset]]
    [semgrep.ruleset.identifier]
      type = "semgrep_id"
      value = "gosec.G106-1"
    [semgrep.ruleset.override]
      severity = "Critical"
```
Identifiers: use the `type`/`value` pairs exactly as they appear in the report's
`vulnerabilities[].identifiers`.

## 2. Add your own Semgrep rules (passthrough)
```toml
[semgrep]
  description = "org rules"
  targetdir = "/sgrules"
  [[semgrep.passthrough]]
    type  = "git"
    value = "<RULES_REPO_URL>"
    ref = "main"
```
- A passthrough pulls ruleset customisations from a file, Git repository, URL or raw value; `targetdir` is where the final configuration is persisted.
- Support differs per analyzer: for GitLab Advanced SAST only `file` and `raw` passthroughs apply and other types are ignored. GitLab supports only the Semgrep analyzer integration and default rulesets.
- Pulling rules from another repository extends your trust boundary; use repositories you control.

## 3. Share across projects
Create a remote ruleset and point projects at it with the `SAST_RULESET_GIT_REFERENCE` variable (see the page's "Reference the remote ruleset" section for the value format). A local `.gitlab/sast-ruleset.toml` takes precedence. Pin the reference to a specific Git SHA so the ruleset cannot change without an explicit update.

## 4. Gotchas
- Check the next report after changing a ruleset to confirm the change took effect.
- Disabling rules hides findings for everyone; prefer dismissing individual false positives with reasons unless the rule is noise across the codebase.

## Verify
- [ ] Next `gl-sast-report.json` no longer contains the disabled rule; overridden finding shows the new severity.

## Checked
2026-10-28. Confirmed on the GitLab customize rulesets page: filename `sast-ruleset.toml`; Ultimate tier; `disable = true` under `[[semgrep.ruleset]]`; `semgrep_id` identifier type (as in the report's identifiers); overriding the severity of default rules; passthrough sources (file, Git, URL, raw) and `targetdir`; `SAST_RULESET_GIT_REFERENCE`, local file precedence, trust-boundary warning and pinning to a Git SHA.
Fixed: the skill said to pin a tag; the docs say pin to a specific Git SHA. Passthrough `type` support is limited for Advanced SAST (only file and raw).
Removed (not confirmed): the `cwe` identifier example, `validate = true`, `mode = "append"`, the `@v2` reference format, and the list of other analyzers that honour rulesets.

Method: documentation only; no commands were run.

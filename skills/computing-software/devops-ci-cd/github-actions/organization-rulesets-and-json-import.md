---
id: computing-software.devops-ci-cd.github-actions.organization-rulesets-and-json-import
name: organization-rulesets-and-json-import
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, organization-rulesets, ruleset-json-import, ruleset-targeting, gh-ruleset, rule-insights]
level: advanced
status: docs-checked
description: "Enforce branch and tag rules across an org with organization rulesets: repository targeting by name or custom property, evaluate mode, and JSON export/import via UI and API."
sources: ["https://docs.github.com/en/organizations/managing-organization-settings/creating-rulesets-for-repositories-in-your-organization", "https://docs.github.com/en/rest/orgs/rules", "https://cli.github.com/manual/gh_ruleset"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Organization rulesets and JSON import/export

## 1. Targeting
Org **Settings → Repository → Rulesets → New branch ruleset**:
- Repositories: all, by naming convention, or by **custom property** (for example `tier = critical`).
- Branches: `~DEFAULT_BRANCH`, `~ALL`, or `refs/heads/release/*`.
- Enforcement: `active`, `disabled`, or `evaluate` (dry run; evaluate is only available with GitHub Enterprise): roll out new rules in evaluate and read **Rule Insights** before activating.

## 2. Ruleset as code
```json
{
  "name": "default-branch-baseline",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "ref_name": { "include": ["~DEFAULT_BRANCH"], "exclude": [] },
    "repository_property": { "include": [{ "name": "tier", "property_values": ["critical"] }], "exclude": [] }
  },
  "bypass_actors": [],
  "rules": [
    { "type": "deletion" }, { "type": "non_fast_forward" },
    { "type": "pull_request", "parameters": { "required_approving_review_count": 1,
      "dismiss_stale_reviews_on_push": true, "require_code_owner_review": true,
      "require_last_push_approval": false, "required_review_thread_resolution": true } },
    { "type": "required_status_checks", "parameters": { "strict_required_status_checks_policy": false,
      "required_status_checks": [{ "context": "ci-ok" }] } }
  ]
}
```
```bash
gh api /orgs/my-org/rulesets      # GET /orgs/{org}/rulesets lists organisation rulesets
```
Create and update calls are in the REST docs for organisation rules; the token needs the "Administration" organisation permission (write). Existing rulesets can be imported in the UI (see "Importing prebuilt rulesets"; GitHub's ruleset-recipes repo has prebuilt ones).

## 3. Gotchas
- `integration_id` is optional: it names the integration the status check must come from.
- Bypass actors use numeric `actor_id` values for Integration, RepositoryRole, Team and User actors, which differ between organisations; check them when moving JSON between orgs.

## Verify
- [ ] The org ruleset appears in a targeted repository's rules.
- [ ] Rule insights show no unexpected bypasses after activation.

## Checked
2026-10-28. Confirmed in the REST organisation rules page and the creating-rulesets page: `~DEFAULT_BRANCH` and `~ALL` ref patterns; `repository_property` condition; enforcement `disabled`, `active`, `evaluate` with Rule Insights (Evaluate needs Enterprise); `bypass_actors` fields (`actor_id`, `actor_type`, `bypass_mode`); rule types `non_fast_forward`, `pull_request` with `required_approving_review_count`, `dismiss_stale_reviews_on_push`, `require_code_owner_review`, `require_last_push_approval`, `required_review_thread_resolution`; `required_status_checks` with `context`, optional `integration_id`, `strict_required_status_checks_policy`; GET `/orgs/{org}/rulesets`; Administration organisation permission; importing rulesets.
Removed (not confirmed): the GitHub Actions integration id 15368, the example bypass actor id, the POST/PUT commands, `gh ruleset check` (gh manual page was a stub), export menu path, name pattern examples, the claim that the most restrictive ruleset wins.

Method: documentation only; no commands were run.

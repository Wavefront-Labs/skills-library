---
id: computing-software.cloud-infrastructure-engineering.aws.well-architected-tool-profiles-and-review-templates
name: well-architected-tool-profiles-and-review-templates
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, well-architected, review-templates, wa-profiles, well-architected-tool, custom-lens, review-at-scale]
level: practitioner
status: docs-checked
description: "Scale Well-Architected reviews in the WA Tool: profiles that prioritise questions by business context, review templates that pre-fill shared answers, sharing and custom lenses."
sources: ["https://docs.aws.amazon.com/wellarchitected/latest/userguide/tool-profiles.html", "https://docs.aws.amazon.com/wellarchitected/latest/userguide/review-templates.html", "https://docs.aws.amazon.com/wellarchitected/latest/userguide/define-workload-from-template.html", "https://docs.aws.amazon.com/wellarchitected/latest/userguide/tool-sharing-profiles.html", "https://docs.aws.amazon.com/wellarchitected/latest/userguide/sharing-review-templates.html", "https://docs.aws.amazon.com/wellarchitected/latest/userguide/lenses-custom.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WA Tool profiles and review templates

## Profiles
A **profile** captures business context and goals you want to accomplish in a review. Attached to a workload, it
gives a prioritised list of questions relevant to your business and shows which risks are prioritised for the
improvement plan. (The AWS Well-Architected Agent has separate "profiles"; they are unrelated to WA Tool profiles.)
```bash
aws wellarchitected create-profile --profile-name regulated-fintech \
  --profile-description "Compliance-first workloads" --profile-questions file://answers.json
aws wellarchitected associate-profiles --workload-id "$WL" --profile-arns "$PROFILE_ARN"
```
- `answers.json` is a list of `{"QuestionId": "...", "SelectedChoiceIds": ["..."]}`. `ProfileName` is 3-100
  characters and `ProfileDescription` 3-100 characters.
- A workload carries at most one profile. After a profile changes, `upgrade-profile-version` updates a workload to
  the latest profile version.
- `list-answers --question-priority PRIORITIZED` returns only prioritised questions.

## Review templates
A **review template** holds pre-filled answers and notes for Framework and custom-lens best practices that are
common across workloads (org-wide controls such as logging, threat detection, identity, backup policy, landing zone
networking).
```bash
aws wellarchitected create-review-template --template-name org-baseline \
  --description "Controls provided by the landing zone" --lenses wellarchitected
aws wellarchitected update-review-template-answer --template-arn "$T" --lens-alias wellarchitected \
  --question-id <QUESTION_ID> --selected-choices <CHOICE_ID> \
  --notes "Provided by landing zone; evidence: <link>"
aws wellarchitected create-workload --workload-name payments ... --review-template-arns "$T"
```
- Template answers stay answered in the new workload; teams answer the rest. Profiles and templates can be used
  together, with the questions prioritised by the profile.
- A workload can be defined only from a template that still exists, and a template with an outdated lens version must
  be upgraded first (`upgrade-review-template-lens-review`). A workload takes at most one review template.
- Defining a workload from a template needs `wellarchitected:CreateWorkload` plus `GetReviewTemplate`,
  `GetReviewTemplateAnswer`, `ListReviewTemplateAnswers` and `GetReviewTemplateLensReview`.
- Share templates and profiles with an IAM user or account, or an organization or OU (`create-template-share`,
  `create-profile-share`); sharing with an organization needs AWS Organizations enabled for the tool. Review templates
  can be shared only within the same AWS Region.

## Custom lenses
Encode your organisation's standards as a custom lens JSON (see the lens format specification page) with
questions, choices and risk rules; preview, publish, publish updates, and share it.

## Operating model
- Platform team owns review templates (shared controls) and custom lens.
- Profiles per workload class (regulated, internal tool, customer-facing).
- Workload teams answer remaining questions; facilitators review evidence.

## Gotchas
- Pre-filled answers are only as true as the platform controls: re-validate on a schedule.
- Template answers can hide workload-specific deviations; require teams to confirm.

## Verify
- [ ] New workloads are created from the baseline template with the right profile.
- [ ] Template last reviewed date recorded; custom lens version current.

## Checked
Date: 2026-10-27. Documentation release: AWS Well-Architected Tool User Guide and API Reference (latest) and
botocore wellarchitected 2020-03-31 model. Confirmed: profile and review template purpose, `create-profile`,
`associate-profiles`, `create-review-template`, `update-review-template-answer` and share operations and their
required parameters and name limits, profile and template per-workload maximum of one, template upgrade requirement,
required IAM actions, sharing targets and Region limit, and the existence of `UpgradeProfileVersion` and
`UpgradeReviewTemplateLensReview`. Replaced made-up question and choice ids with placeholders and removed the
unconfirmed "workloads can pull template updates" claim; replaced prose-title `sources` with real URLs.
Method: documentation only; no commands were run.

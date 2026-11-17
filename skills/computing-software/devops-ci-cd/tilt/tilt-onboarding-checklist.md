---
id: computing-software.devops-ci-cd.tilt.tilt-onboarding-checklist
name: tilt-onboarding-checklist
category: computing-software
field: devops-ci-cd
product: tilt
tags: [onboarding-checklist, tilt]
level: practitioner
status: docs-checked
description: "Checklist of questions to answer before asking a team to run tilt up: compatibility, update speed, error visibility, and support channels."
sources:
  - "https://docs.tilt.dev/onboarding_checklist.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Team onboarding checklist for Tilt

Goal: before asking teammates to `tilt up`, answer these questions so onboarding goes smoothly.

## Setup and compatibility

- Have you tested Tilt on all the operating systems your team uses?
- Do colleagues know how to run Kubernetes locally? The guide to choosing a cluster can help.
- Which services do they hack on, and do all of them start up OK in Tilt?
- Are there known gotchas or spurious error messages when you `tilt up` a server? Are they documented?

## Enhancements, errors, and optimizations

- `tilt up` each server and edit a file. Does the server auto-update with your changes?
- Are updates slow to show up? A `live_update` rule could sync changes much faster.
- Do some file edits trigger unnecessary rebuilds? Add ignore rules to prevent wasted work.
- Is auto-update right for every server? For some, you may prefer they update only when you are ready (manual update control).
- Introduce a syntax error: does Tilt pop up an error, and could teammates find it?
- Log a runtime error: does it show up in the Tilt logs?

## Support and followup

- Is there a dedicated place (mailing list, Slack) to discuss dev environment improvements?
- Do teammates know where to ask for help when the workflow breaks or gets slow?
- Is there a README to help teammates `tilt up` and go?
- Could other teams in your org benefit from a cloud-native dev environment like Tilt?

Once ready, fork the tilt-init repo (tilt-dev/tilt-init) and edit away.

## Checked

2026-11-07. Pages read from the tilt-dev/tilt.build source of docs.tilt.dev. Read the onboarding checklist page in full. Confirmed all three question groups and the tilt-init fork suggestion; the skill drops the page's links but keeps its content. Nothing removed. The skill is a checklist with few checkable facts. 

Method: documentation only; no commands were run.

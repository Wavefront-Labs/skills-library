---
id: computing-software.devops-ci-cd.jenkins.plugin-health-scores-and-adoption
name: plugin-health-scores-and-adoption
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, plugin-health-score, plugin-management, deprecated-plugins]
level: practitioner
status: docs-checked
description: "Evaluate a Jenkins plugin before adopting or keeping it using the plugin health score, maintenance signals, security warnings, adoption status and installation counts."
sources: ["https://www.jenkins.io/doc/developer/plugin-governance/plugin-health-score/", "https://plugins.jenkins.io/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Plugin health scores and adoption checks

The Plugin Manager and plugins.jenkins.io show a **health score** per plugin from the Plugin
Health Scoring service, which evaluates source code, repository content and external metrics
(such as open pull requests) the same way for every plugin. The score reflects the latest data,
not the installed release. Details per plugin are on the plugin's health score section or at
`plugin-health.jenkins.io/scores/<plugin>`; the plugin page lists recommendations to improve it.

## Adoption checklist
1. Read the health score and its detail page, not only the number.
2. Check labels: "deprecated", "up for adoption", "security warnings".
3. Release history: recent releases, and a required core version your LTS supports.
4. Installation trend (stats) and number of dependants.
5. Does a core feature or better-maintained plugin replace it?

## Auditing an existing controller
Manage Jenkins > Plugins > Installed shows deprecation and security warnings and the health
score; the plugin installation manager can print available updates:
`jenkins-plugin-cli --available-updates --plugin-file plugins.txt`.

## Acting on low scores
- Remove unused plugins (no dependants, not referenced in jobs).
- Replace deprecated ones in a staging controller first.
- Consider adopting critical abandoned plugins; adopting or contributing is welcome per the Jenkins plugin-management docs.

## Verify
- [ ] Inventory doc lists each plugin with score and owner; no deprecated plugins without a removal ticket.

## Checked
2026-11-02. Confirmed against the Jenkins plugin management handbook page (health score section), the plugin deprecation governance page and the plugin-installation-manager-tool README (--available-updates, --plugin-file). Removed: 0-100 range, probe list, score thresholds, 12-month rule, specific replacement suggestions, script-console snippet.
Method: documentation only; no commands were run.

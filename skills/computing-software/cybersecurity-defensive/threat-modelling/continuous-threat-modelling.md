---
id: computing-software.cybersecurity-defensive.threat-modelling.continuous-threat-modelling
name: continuous-threat-modelling
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [threat-modelling, continuous-threat-modelling, agile, threat-model-as-code, pytm, devsecops]
level: practitioner
status: docs-checked
description: "Keep threat models current in agile teams: Manifesto values, Autodesk Continuous Threat Modeling, and threat-model-as-code with pytm and Threagile."
sources: ["https://www.threatmodelingmanifesto.org/", "https://raw.githubusercontent.com/Autodesk/continuous-threat-modeling/master/README.md", "https://raw.githubusercontent.com/izar/pytm/master/README.md", "https://raw.githubusercontent.com/Threagile/threagile/master/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Continuous threat modelling in agile teams

## Principles (Threat Modeling Manifesto)
- Values: continuous refinement over a single delivery; doing threat modelling over talking
  about it; people and collaboration over processes, methodologies and tools; a journey of
  understanding over a security snapshot.
- Threat modelling must align with the organisation's development practices and follow
  design changes in iterations that are each scoped to manageable portions of the system.
- The best use is early and frequent analysis.
- Four questions: What are we working on? What can go wrong? What are we going to do about
  it? Did we do a good enough job?
- Anti-patterns: hero threat modeller, admiration for the problem, tendency to overfocus,
  perfect representation.

## Autodesk Continuous Threat Modeling
Autodesk's methodology lets development teams threat model with minimal initial security
knowledge and less dependence on security experts. It is described as evolutionary and
dynamic, suited to teams using Agile and evolving architectures, with emphasis on simplicity,
return on investment and a developer-friendly workflow. Autodesk's repository points to a
talk, "Threat Modeling Every Story", for how the handbook and checklist are used; the
checklist content itself was not read for this review.

## Living model as code
Keep the model in the repository so it changes with the system.
- **pytm**: the model is Python. From the README, `./tm.py --dfd | dot -Tpng -o dfd.png`
  produces a data flow diagram via Graphviz, `./tm.py --seq` produces a sequence diagram
  (PlantUML), and `./tm.py --report <template> | pandoc -f markdown -t html > report.html`
  produces a report. `--list` lists the available threats and `--describe <Element>` lists an
  element's properties.
- **Threagile**: an architecture model written as YAML. Running the toolkit checks all
  standard risk rules (and any custom ones) against the model. Documented flags include
  `-model`, `-output`, `-create-stub-model` and `-create-example-model`, and the easiest way
  to run it is the `threagile/threagile` Docker image.

## Gotchas
- A model is not a one-off: the OWASP cheat sheet says it should be maintained, updated and
  refined alongside the system and integrated into the team's normal SDLC.
- Generated output reflects only what the model states.

## Verify
- [ ] The model lives in the repository and changes in the same pull request as the
      architecture it describes.
- [ ] The diagram and report regenerate from the model with the documented commands.

## Checked
Confirmed 2026-11-09 against the Threat Modeling Manifesto page, the Autodesk continuous-threat-modeling README, the pytm README (usage, diagram and report commands) and the Threagile README (flags, Docker), all read in full, plus the OWASP Threat Modeling Cheat Sheet for the maintenance statement.
Removed as unconfirmed: the three-question per-story checklist attributed to the Autodesk handbook, the 15 to 30 minute STRIDE timebox, security acceptance criteria rules, ticket labelling and dashboard advice, the annual review cadence, and the champion spot-check and service-catalogue gotchas.
Method: docs-checked 2026-11-09 against threatmodelingmanifesto.org, Autodesk continuous-threat-modeling README, izar/pytm README and Threagile README

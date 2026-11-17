---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.change-and-process-induced-emergencies
name: change-and-process-induced-emergencies
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [change-induced-emergency, process-induced-emergency, emergency-response, test-induced-emergency, automation-safety]
level: practitioner
status: docs-checked
description: "Respond to and prevent the SRE Book's three emergency types: test-induced, change-induced (config pushes) and process-induced (runaway automation), with the lessons each taught."
sources: ["https://sre.google/sre-book/emergency-response/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Change- and process-induced emergencies

The SRE Book chapter "Emergency Response" gives three case studies, each triggered differently: a proactive
test, a configuration change, and turndown automation. Responders in all three did not panic, pulled in others
when needed, and documented new failure modes.

## Test-induced
A test meant to flush out hidden dependencies by blocking access to one database out of a hundred broke key
systems within minutes. SRE assumed the test was responsible and aborted it at once, but the permissions
rollback failed because rollback had not been tested; they fell back to an already tested approach.
Lessons from the book:
- A thoroughly reviewed, well-scoped test can still reveal poorly understood dependencies.
- Follow the incident response process even for your own test, so services and customers know.
- Test rollback procedures in a test environment before large-scale tests.
- Set up periodic retesting after the fix.

## Change-induced
A configuration change to abuse-protection infrastructure was pushed globally and triggered a crash-loop bug
across externally facing systems. The push engineer noticed complaints and rolled the change back quickly;
some services still took up to an hour to recover.
Lessons from the book:
- An earlier thorough canary missed the bug because it never exercised a rare keyword in combination with the
  new feature; the change was judged not risky and had a lighter canary. Canary thoroughly regardless of
  perceived risk.
- Keep out-of-band communication and command-line or alternative access methods for rolling back when normal
  interfaces are down, and practise them.
- Alert floods disrupted on-call work; tooling used for troubleshooting may itself sit behind the crash-looping
  jobs.
- The affected system rate-limiting full updates to new clients may have throttled the crash loop.

## Process-induced
Two consecutive turndown requests for the same server installation hit a subtle automation bug: an empty
response was passed on as an empty filter, so the machine database was told to erase all machines involved
("sometimes zero does mean all"). On-call engineers drained traffic, disabled all team automation to prevent
further damage, and froze other automation and maintenance. Traffic was fully diverted within an hour.
Lessons from the book:
- The root cause was missing sanity checks on the commands the turndown server sent.
- Large installations were unaffected because proxies there are managed differently, and could carry full load.
- Recovery (reinstallation) was slow, hit by overloaded and mis-tuned install infrastructure; plan the
  recovery path, not only the stop.

## All emergencies
- If overwhelmed, pull in more people; follow your incident process.
- The person with the most state is often the one whose action triggered the event; use them.
- Keep and publish a history of outages, and follow up on postmortem actions.
- Ask "what if" questions and test proactively, ideally when your best people are at hand.

## Checked
2026-11-01. Confirmed against the SRE Book chapter Emergency Response: all three case studies and the lessons
listed. Removed: the specific 5 percent bound, two-person rule, kill-switch and git-log playbook, which the
chapter does not state.
Method: documentation only; no commands were run.

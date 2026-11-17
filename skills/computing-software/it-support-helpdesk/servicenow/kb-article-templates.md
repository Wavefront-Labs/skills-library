---
id: computing-software.it-support-helpdesk.servicenow.kb-article-templates
name: kb-article-templates
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, kb-article-template, knowledge-base, kcs, article-structure, knowledge-management, how-to-article]
level: practitioner
status: draft
description: "Write and configure KB article templates: KCS issue / environment / resolution / cause structure, how-to vs troubleshooting templates, titles users search for, and template setup."
sources:
  - "https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide/030/030/010/030"
  - "https://www.servicenow.com/docs/bundle/zurich-servicenow-platform/page/product/knowledge-management/concept/knowledge-article-templates.html"
  - "https://www.servicenow.com/docs/bundle/zurich-servicenow-platform/page/product/knowledge-management/task/create-knowledge-article-template.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# kb-article-templates

A template makes articles consistent enough that agents and users scan them in seconds.
KCS v6 Structure practice defines the content model; ServiceNow article templates
enforce it as fields.

## KCS structure (troubleshooting article)
| Section | Content | Rule |
|---|---|---|
| Issue | What the user sees, in their words; exact error text | Searchable phrases, quote errors verbatim |
| Environment | Product, version, OS, configuration where it applies | Things that *stay* true, not steps |
| Resolution | Numbered steps to fix or work around | One action per step |
| Cause | Why it happens (optional) | Helps reuse and problem mgmt |

Plus metadata: keywords, product/category, audience (internal or external), owner.

## Other templates
- **How-to**: Goal, Prerequisites, Steps, Result/verify. For requests ("how do I map a
  drive") rather than faults.
- **Known error**: Symptom, Workaround, Status of permanent fix, Linked problem.
- **FAQ**: one question per article; don't stack ten Q&As in one.

## Creating templates in ServiceNow
1. Knowledge > Administration > Article Templates (Knowledge Management Advanced /
   templates plugin): create a template; it generates a child table of `kb_knowledge`
   with one HTML field per section.
2. Assign templates to knowledge bases; authors pick the template when creating.
3. Mandatory sections via the template field definitions; keep Cause optional.
4. Converting legacy free-text articles isn't automatic; migrate the top 50 by view count.

## Writing rules
- Title = the issue as a user would type it: "Outlook keeps asking for password", not
  "Outlook authentication remediation procedure".
- Steps start with a verb, include the exact menu path (Settings > Accounts > Access
  work or school) and expected result.
- Screenshots only where text can't explain it; they go stale on every UI update.
- Internal-only steps (admin tools) in a separate internal section or article.

## Gotchas
- Templates with too many mandatory sections stop agents capturing in the moment, which
  kills the KCS solve loop. Four sections is enough.
- Changing a template after articles exist doesn't restructure them.

## Verify
New articles in each KB use a template; a search for the verbatim error text returns the
article in the top three; agents can follow the resolution without asking anyone.

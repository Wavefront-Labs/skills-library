---
id: engineering-technology.invention-prototyping.patent-disclosure.writing-an-invention-disclosure
name: writing-an-invention-disclosure
category: engineering-technology
field: invention-prototyping
product: patent-disclosure
tags: [invention-prototyping, patent-disclosure, invention-disclosure, invention-disclosure-form, idf, prior-art, prior-art-search, patentability, novelty, inventive-step, non-obviousness, enablement, best-mode, inventor-notebook, lab-notebook, grace-period, public-disclosure, confidentiality, nda, google-patents, espacenet, cpc-classification, claims, embodiments, technology-transfer, intellectual-property]
level: practitioner
status: draft
description: "Capture an invention for protection: dated records, prior-art search, problem-solution novelty framing, enabling detail, variants and a disclosure form for counsel."
sources: ["WIPO Patent Drafting Manual", "EPO Guidelines for Examination (problem-solution approach)", "USPTO Manual of Patent Examining Procedure (general background)", "Espacenet and Google Patents search help pages", "University technology-transfer office invention disclosure guides (general practice)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing an invention disclosure — the technical record counsel needs

**Goal:** capture what the invention is, why it is new, and how to make it, clearly
enough that a patent attorney or agent can assess and draft it — before anything is
made public.

> This is a technical documentation method, not legal advice. Patentability, filing
> strategy and claim drafting are decisions for a registered patent attorney/agent and
> your organisation's IP policy.

## 1. Protect novelty first
- **Do not publish, demo, pitch, post or sell** before speaking to counsel. Conference
  talks, preprints, crowdfunding pages, trade shows and theses all count as disclosure.
- Share outside the team only under a written confidentiality agreement, and record who
  saw what and when.
- **Grace periods differ — treat them as a last resort, not a plan.** The US gives the
  inventor's own disclosures a 12-month grace period before filing. The European Patent
  Office is **absolute novelty**: essentially any public disclosure before filing, including
  your own, can destroy patentability (narrow exceptions only). Other countries vary.
  A disclosure that is safe for a US filing can still cost you Europe.

## 2. Keep records as you go
- Dated, page-numbered notebook (bound paper or an electronic notebook with audit trail).
  No blank gaps; strike through errors rather than erasing.
- Record ideas, sketches, test setups, raw results and failed attempts.
- Have a non-inventor colleague who understands it sign/date key pages; version-control CAD, code and data.
These records establish who contributed what and when; inventorship is decided by
contribution to the claimed concept, not by job title — counsel decides it.

## 3. Search the prior art (an hour or two, not a legal opinion)
1. Write the invention as 3–5 key features in plain words.
2. Search **Google Patents** and **Espacenet** with keyword combinations and synonyms
   (UK/US terms, trade jargon).
3. Find the **CPC classification** codes of the closest hits and search within them —
   this finds documents that use different words.
4. Follow citations backwards and forwards from the closest documents.
5. Also search non-patent literature: papers, product manuals, datasheets, videos.
6. Record the closest 3–5 references and, for each, which of your features it has and
   which it lacks. Give these to counsel; hiding close art helps nobody and, in the US,
   there is a duty to disclose known material art.

## 4. Frame novelty and inventive step
Use the problem-solution structure that examiners use:
- **Closest prior art:** the single nearest existing solution.
- **Distinguishing features:** what yours has that it does not.
- **Technical effect:** what measurable difference those features make (e.g. 40% less
  power, no calibration step, works when wet).
- **Objective problem:** the problem those features solve.
- **Why not obvious:** why a skilled practitioner would not simply have done it — a
  prejudice overcome, an unexpected result, a long-felt need, failed attempts by others.
Support effects with data from your tests where you have it.

## 5. Write the disclosure
| Section | Content |
|---|---|
| Title | Descriptive, not marketing ("Two-stage magnetic latch for…") |
| Field and background | The problem and existing solutions, with references |
| Summary | The core idea in one paragraph |
| Detailed description | Enough for a skilled person to build it: parts, materials, dimensions or ranges, steps, control logic |
| Drawings | Numbered figures with reference numerals for every part |
| Best embodiment | The version that works best as far as you know |
| Variants and alternatives | Other materials, layouts, ranges, uses — broadens protection |
| Test evidence | Data showing the effect |
| Disclosures and dates | Any past or planned public exposure, sales, collaborations, funding |
| Contributors | Who contributed which feature |

Write ranges as well as point values ("0.5–3 mm, preferably 1 mm") and describe features
by **function** as well as by the specific part ("a biasing element, e.g. a coil spring").

## Gotchas
- Describing only the prototype: competitors design around a single embodiment.
- Omitting the "how": an idea with no enabling detail is not protectable.
- Leaking via git: a public repository or package release is a publication.
- Treating a search with no hits as proof of novelty — it is only evidence.

## Verify
- [ ] No public disclosure has happened, or every one is listed with its date.
- [ ] The closest prior art is identified and the distinguishing features stated.
- [ ] A skilled person could build the invention from the description and figures.
- [ ] At least three variants or alternative embodiments are described.
- [ ] Dated, witnessed records support the contribution and timeline.

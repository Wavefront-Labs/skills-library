---
id: law-government.intellectual-property-law.patent-prosecution.claim-drafting-and-office-action-responses
name: claim-drafting-and-office-action-responses
category: law-government
field: intellectual-property-law
product: patent-prosecution
tags: [intellectual-property-law, patent-prosecution, patent, claims, claim-drafting, independent-claim, dependent-claim, specification, written-description, enablement, antecedent-basis, office-action, rejection, 102, 103, novelty, obviousness, inventive-step, 101, patent-eligibility, alice, interview, amendment, prosecution-history-estoppel, continuation, epo, uspto, pct]
level: advanced
status: docs-checked
description: "Draft patent claims with a claim ladder and supporting specification, then answer office actions on novelty, obviousness and eligibility without creating estoppel."
sources: ["35 U.S.C. 102 (https://www.law.cornell.edu/uscode/text/35/102)", "37 CFR 1.56 (https://www.law.cornell.edu/cfr/text/37/1.56)", "37 CFR 1.134 (https://www.law.cornell.edu/cfr/text/37/1.134)", "EPC Article 55 (https://www.epo.org/en/legal/epc/2020/a55.html)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Claim drafting and office-action responses

**Goal:** obtain claims that are as broad as the prior art allows, supported by the
specification, and still valuable after prosecution history is read against them.
US terms (USPTO, §§101/102/103/112) with EPO equivalents noted; patent offices differ on
eligibility, inventive-step methodology and amendment rules — check the office's manual.

## 1. Before drafting: understand the invention and the art
- Interview inventors for the **problem**, the solution, and every alternative embodiment
  ("what else would work instead of X?"). Alternatives are what let claims be generic.
- Review a prior-art search (see law-government.intellectual-property-law.patent-search-platforms)
  to place the **point of novelty**.
- Identify who infringes: write claims a single actor performs or makes (direct
  infringement by one party is far easier to prove than divided infringement).

## 2. Build a claim ladder
- **Independent claims**: broadest reasonable statement of the invention — fewest
  elements needed to distinguish the art. Usually one per category (method, apparatus/
  system, computer-readable medium), each aimed at a different infringer.
- **Dependent claims**: fallback positions in descending breadth, each adding one
  commercially meaningful feature. They are the amendments you'll want later.
- Drafting discipline:
  - Every element has **antecedent basis** ("a sensor" then "the sensor").
  - Avoid functional language that may be read as means-plus-function (US §112(f)) unless
    intended; if used, the spec must disclose the corresponding structure.

## 3. Specification that supports the claims
- Every claim term must be described (**written description**) and enabled for its full
  scope (**enablement**). Broad genus claims need multiple representative species.
- Include definitions for key terms, ranges with fallback sub-ranges, and figures
  showing each claimed element.
- For software/business methods, describe the technical implementation and the technical
  improvement — eligibility under §101 (US) and the technical-character requirement (EPO)
  often turns on it.

## 4. Reading an office action
Tabulate each rejection: claims affected, statutory basis, references, the examiner's
mapping of each element. Calendar the response deadline: the Office action sets any shortened period, and a maximum
of six months is allowed (37 CFR 1.134); extension fees apply.
- **Novelty (§102 / EPC Art 54)**: one reference must disclose every element as arranged.
  Find the missing element.
- **Obviousness / inventive step (§103 / Art 56)**: attack the combination — missing
  elements, no reason to combine, teaching away, unexpected results. Check the office's
  manual (MPEP; EPO Guidelines) for its current approach.
- **§112**: clarity, support, enablement — often fixed with a careful amendment.
- **§101**: argue the claim is a specific technical improvement; amend to recite it.

## 5. Writing the response
- Consider an **examiner interview** first (US). Record its substance accurately.
- Prefer argument over amendment when the argument is strong; every narrowing amendment
  and argument becomes **prosecution history** that can limit claim scope in later
  litigation.
- Amend by importing a dependent claim's feature, or spec-supported features; cite the
  support location for every amendment (check the office's added-matter rules).
- Say no more than needed: avoid characterising "the invention" broadly or disclaiming
  subject matter unnecessarily.
- Keep a continuation/divisional on file if broader or different claims may be wanted
  later (US continuation practice; EPO divisional rules differ).

## Gotchas
- Public disclosure before filing can destroy novelty; grace periods vary. In the US, an
  inventor's own disclosure made 1 year or less before the effective filing date is
  excepted from prior art (35 U.S.C. 102(b)(1)); under Art. 55 EPC only disclosures within
  six months before filing resulting from evident abuse or display at an officially
  recognised international exhibition are disregarded.
- Duty of disclosure (US, 37 CFR 1.56): each named inventor, and each attorney or agent who
  prepares or prosecutes the application, must disclose information known to be material to
  patentability.

## Verify
- [ ] Each independent claim distinguishes the closest art and targets a single direct infringer.
- [ ] Every claim term has antecedent basis and written-description support.
- [ ] Dependent claims form a meaningful fallback ladder.
- [ ] Response addresses every rejection with element-by-element reasoning and cites support for amendments.
- [ ] Prosecution-history effect of each argument considered; continuation decision recorded.

## Checked
Checked 2026-10-24. Jurisdiction: United States (USPTO) with EPO notes. Sources read 2026-10-24: 35 U.S.C. 102(b)(1) (1-year grace for inventor disclosures); 37 CFR 1.56 (who owes the duty; materiality); 37 CFR 1.134 (the Office action sets the period; six-month maximum); EPC Art. 55 (six months; evident abuse or recognised exhibition only). Fixed: the earlier text said the EPO "essentially" has no grace period; Art. 55 provides a narrow six-month exception. Removed unconfirmed statements on spec wording effects, fee thresholds, Alice, problem-solution detail and estoppel. General information, not legal advice.
Method: documentation only; no commands were run.

---
id: languages-linguistics.translation.legal-translation.legal-system-equivalence-and-certified-translation
name: legal-system-equivalence-and-certified-translation
category: languages-linguistics
field: translation
product: legal-translation
tags: [legal-translation, translation, contract-translation, court-documents, judgments, official-documents, birth-certificate, certified-translation, sworn-translation, traductor-jurado, beeidigter-uebersetzer, naati, translator-statement, apostille, legalisation, notarised-translation, legal-terminology, common-law, civil-law, functional-equivalence, legal-system-mismatch, formatting, immigration-documents]
level: advanced
status: draft
description: "Translate contracts and official documents: handle concepts with no target-system equivalent, keep structure, and meet the receiving authority's certified or sworn translation rules."
sources: ["Šarčević, New Approach to Legal Translation (Kluwer 1997)", "Cao, Translating Law (Multilingual Matters 2007)", "Hague Apostille Convention (HCCH) — scope of apostilles"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Legal-system equivalence and certified translation

**Goal:** a legal translation that a lawyer, court or authority in the target country can
rely on: no concept silently swapped for a false equivalent, nothing added or omitted, and
the formal certification the receiving body actually requires.

## 1. Know the purpose and the receiver first
Ask: Who will read it, and why? (a court, a registry, an immigration office, opposing counsel,
the client for information). Is it for **information** (target reader needs to understand the
source law's effect) or a **binding/parallel text** (both versions may have legal force — the
contract should say which prevails)? The purpose determines how literal you must be.

## 2. Legal-system mismatch
Law is system-bound: common-law and civil-law concepts often don't map one-to-one
(e.g. *trust*, *consideration*, *estoppel* in English law; *notaire* in French law is not a
US *notary public*; German *Gesellschaft mit beschränkter Haftung* is not exactly a "limited
company"). For each term choose:
- **functional equivalent** — target term with the closest function, when the difference is
  irrelevant for the purpose;
- **borrowing + explanation** — keep the source term (italics or brackets) with a brief gloss,
  when the difference matters;
- **literal/descriptive rendering** — neutral description ("limited liability company
  (GmbH)").
Never use a target term that carries legal effects the source concept doesn't have, without flagging.
Use authoritative sources: legislation in both languages, bilingual statutes (e.g. Canada,
EU law in EUR-Lex, Swiss federal law), IATE for EU terminology.

## 3. Drafting conventions
- Preserve structure: numbering, clause references, defined terms (capitalised, used
  identically every time), cross-references.
- Keep "shall/must/may" deontic distinctions; don't stylistically vary obligations.
- Don't resolve source ambiguity — reproduce it, and add a translator's note if needed.
- Names, addresses, registration numbers, dates: transcribe exactly; transliterate names using
  the form in the person's passport where given.

## 4. Certified / sworn translation
Requirements are set by the **receiving** jurisdiction or authority and vary widely:
- Some civil-law countries use court-appointed **sworn translators** (e.g. Spain *traductor
  jurado*, Germany court-authorised translators) whose stamp is required.
- Other systems accept a **translator's statement** of accuracy and competence, sometimes
  notarised (common in the US and UK).
- Some require accreditation by a national body (e.g. NAATI in Australia).
- An **apostille** certifies the origin of a public document (often the source document, or the
  notary's signature on a translation), not translation accuracy.
Always get the receiving authority's written requirements before quoting.
*Rules change and differ by agency within one country — this list is illustrative, not complete.*

## 5. Official documents (certificates, IDs)
- Translate everything visible: stamps, seals ("[Seal: Civil Registry of …]"), handwritten
  notes ("[handwritten: …]"), illegible parts ("[illegible]").
- Mirror layout reasonably so items can be matched; don't reproduce coats of arms.
- Don't convert dates of birth formats ambiguously (write the month in words if formats differ).

## Gotchas
- "Improving" a badly drafted source contract changes its meaning — translate the flaws.
- False friends: *actual* (Spanish = current), *eventual* (= possible), *jurisdiction* senses.
- Translating "notary" or "attorney" with the target-system title misrepresents the role.
- Confidentiality: legal documents often contain personal data — use secure transfer and
  check whether MT/cloud tools are allowed.

## Verify
- [ ] Purpose, receiving authority and their certification requirements are documented.
- [ ] Every system-bound term has a deliberate procedure and a cited source.
- [ ] Defined terms, numbering and cross-references match the source exactly.
- [ ] All stamps, seals and handwriting are accounted for in brackets.
- [ ] A second reader compared figures, names, dates and negations line by line.

Related: `languages-linguistics.translation.translation-revision.bilingual-revision-and-mqm-error-typology`,
`languages-linguistics.translation.technical-translation.terminology-consistency-and-controlled-language`.

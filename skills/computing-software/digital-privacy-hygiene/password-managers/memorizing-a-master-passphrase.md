---
id: computing-software.digital-privacy-hygiene.password-managers.memorizing-a-master-passphrase
name: memorizing-a-master-passphrase
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, master-password-memorization, master-password, spaced-repetition, diceware, passphrase, lockout-prevention]
level: intro
status: docs-checked
description: "Commit a new random master passphrase to memory with spaced recall and a temporary paper backup, so a strong passphrase never becomes a lockout."
sources:
  - "https://ssd.eff.org/module/creating-strong-passwords"
  - "https://www.eff.org/dice"
  - "https://bitwarden.com/help/master-password/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memorising a master passphrase

**Goal:** remember a truly random multi-word passphrase reliably. Forgetting the passphrase of a
password vault is a serious risk that can mean permanently losing data (EFF), and some managers cannot reset it:
Bitwarden states its staff and systems have no way to retrieve or reset a master password.

## Procedure
1. **Generate** with dice and EFF's Long Wordlist (five dice per word), or the manager's passphrase generator. EFF
   suggests six words for most uses and a minimum of six from its long list; SSD says at least six words for disk
   encryption and a password manager. Random choice matters because people are not good at making unpredictable choices.
2. **Make a mnemonic**: EFF's step 6 is a story, scenario or sentence that reminds you of the words you chose, in
   order. Keep the order straight; the example on the EFF page links all six words in one sentence.
3. **Write a temporary paper copy** while learning. EFF says to keep a written passphrase in a safe place, not where
   the data it protects is stored, and notes it is safer to write on a single thickness of paper on a hard surface so
   no imprint is left.
4. **Practise recall with increasing gaps**: lock the vault and type the passphrase from memory several times over the
   first days and weeks, lengthening the interval each time. (The schedule is yours to choose; the cited pages give none.)
   If your manager offers biometric or PIN unlock, check its documentation, because those unlock a locked vault
   without typing the passphrase (Bitwarden lists biometrics and PIN as unlock options, not login alternatives), so
   they do not rehearse the memory.
5. When recalls are consistently clean, **decide the paper copy's fate**: destroy it, or move it into the emergency kit
   / sealed envelope for your legacy plan (see
   `computing-software.digital-privacy-hygiene.password-hygiene.digital-legacy-and-shared-household-credentials`).
6. **Ongoing**: type the passphrase regularly so the memory stays fresh.

## Related facts
- Use the passphrase for one purpose only; do not reuse it for an online account (EFF).
- Bitwarden: master passwords created after release 2023.3.0 must be at least 12 characters, and a hint can be
  requested by email at the login screen, so write a hint only you understand.
- Keep any written copy apart from the data it protects (EFF), so not inside the vault it opens.

## Gotchas
- Malware on the device can watch you type a master password (EFF), so keep devices clean.

## Verify
- [ ] Typed from memory correctly without hints after a few weeks of spaced practice.
- [ ] Paper copy destroyed or sealed in a deliberate location, apart from the vault.

## Checked
Confirmed 2026-11-08 against EFF's dice passphrase page (six words, long wordlist, five dice, mnemonic, paper-copy
advice, single-purpose use), EFF Surveillance Self-Defense "Creating Strong Passwords" (six-word minimum, spyware
note) and Bitwarden's master password page (no reset, 12-character rule, hint, unlock options). Removed: the +1 h to
+2 weeks schedule, the three-week trigger, the claim that 1Password and Bitwarden biometric unlock fall back to the
master password after restarts, the advice not to swap words, and "5-7 word" in the goal.
Method: docs-only read of cited pages, 2026-11-08

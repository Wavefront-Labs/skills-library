---
id: computing-software.cryptography-implementation.applied-cryptography.entropy-source-health-tests
name: entropy-source-health-tests
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, random-generation, entropy-health-tests, sp-800-90b, repetition-count-test, adaptive-proportion-test, min-entropy, trng]
level: sme
status: docs-checked
description: "Implement SP 800-90B health tests for an entropy source: repetition count and adaptive proportion cutoffs, start-up and on-demand testing, failure handling."
sources: ["https://csrc.nist.gov/pubs/sp/800/90/b/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entropy source health tests

SP 800-90B requires health tests on the entropy source: start-up tests, continuous tests
(primarily on the noise source) and on-demand tests (section 4). Two continuous tests are approved:
the Repetition Count Test and the Adaptive Proportion Test (section 4.4).

## Repetition Count Test (4.4.1)
Detects catastrophic failure, a noise source stuck on one value. With assessed min-entropy H per
sample and false-positive probability alpha:

```
C = 1 + ceil(-log2(alpha) / H)
fail if a sample value is repeated C or more times in a row
```

Examples from the SP: alpha = 2^-20 and H = 2.0 gives C = 11 (so H = 1 gives 21); an 8-bit source has
a cutoff of 6. The test is "not very powerful": a source degraded to 4 bits per sample (1/16
chance of repeating) would still take about one million samples to be noticed.

## Adaptive Proportion Test (4.4.2)
Detects a large loss of entropy, for example from physical failure or environmental change. Take
a sample, count how often the same value occurs in the next W-1 samples, and signal an error if the
count reaches the cutoff C, chosen so that Pr(B >= C) <= alpha. Window size W is fixed: 1024 for a
binary source (two distinct values) and 512 for a non-binary source. For binary sources the
developer may also check that W-B >= C. The SP's Table 2 gives example cutoffs for alpha = 2^-20
(for instance W = 1024, H = 0.2 gives C = 941). For alphabets above 256 symbols the alphabet may be
reduced by the method in section 6.4.

## Start-up and on-demand (section 4.3 requirements)
- Start-up tests run the continuous tests over at least 1024 consecutive samples; samples that
  pass may be released for operational use or discarded.
- The source must support on-demand testing that includes at least the start-up tests, by
  restarting the source or rerunning start-up tests; document the approach used.
- Developers may add their own tests for known failure modes.

## On failure
- The entropy source must notify the consuming application (for example the RBG) of the error.
  Developers may define intermittent and persistent failure types with different cutoffs.
- On a persistent failure the source must produce no outputs; it may support being reset by the
  consuming application. Returning to operation after intermittent failures needs evidence that
  they are really intermittent and that permanent failures are ultimately detected.
- Recommended false-positive probability is between 2^-20 and 2^-40 (lower is acceptable); document
  the value chosen. The SP notes about one error in 2^20 samples can be expected at alpha = 2^-20.

## Assessing min-entropy
Use the assessed H (from the SP's estimators on raw, pre-conditioning samples) rather than a design
guess to set the cutoffs. Tool invocation details were not verified here.

## Verify
- [ ] Forcing constant samples trips the Repetition Count Test within C samples.
- [ ] A biased source simulation trips the Adaptive Proportion Test.
- [ ] Output stays blocked until the start-up tests pass.

## Checked
Method: docs-checked 2026-11-09 against NIST SP 800-90B (section 4 health tests including 4.4.1, 4.4.2 and Table 2; downloaded PDF). Corrected the window sizes (1024 binary, 512 non-binary), removed the NIST assessment-tool commands and jitterentropy claim (those pages were not verified) and the FIPS error-state claim.

---
id: computing-software.cryptography-implementation.applied-cryptography.sp-800-90b-min-entropy-estimation
name: sp-800-90b-min-entropy-estimation
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, min-entropy-estimation, sp-800-90b, entropy-source, ea-tool, esv, noise-source]
level: sme
status: docs-checked
description: "Estimate noise-source min-entropy with SP 800-90B and NIST's SP800-90B_EntropyAssessment tool: IID versus non-IID tests, restart tests, and reading results."
sources: ["https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-90B.pdf", "https://github.com/usnistgov/SP800-90B_EntropyAssessment", "https://csrc.nist.gov/projects/cryptographic-module-validation-program/entropy-validations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SP 800-90B min-entropy estimation

## Data collection
- Capture raw noise-source samples before any conditioning: at least 1,000,000 samples (if consecutive
  collection is impossible, concatenated sets of at least 1000 consecutive samples each; section 3.1.1).
  The tool expects each symbol to fit in one byte, with `bits_per_symbol` giving the meaningful bits.
- Also collect restart data: 1000 restarts x 1000 consecutive samples, for the restart tests (section 3.1.4).
- Restart the source the way it restarts in real use, with outputs taken after start-up tests complete.

## Run the NIST tool
```sh
git clone https://github.com/usnistgov/SP800-90B_EntropyAssessment && cd cpp && make
./ea_iid -v data.bin 8              # IID track
./ea_non_iid -v data.bin 8          # non-IID track
./ea_restart -n -v restart.bin 8 <H_I> # restart tests (-i for IID data, -n for non-IID); H_I = initial estimate
```
The number after the file name is bits per symbol. `ea_iid` and `ea_non_iid` take `-i` (unconditioned,
default) or `-c` (conditioned data, assessed as a bitstring). The README says to run `make` for all binaries.

## Track choice
The IID track needs the submitter's IID claim with rationale plus passing IID tests on the sequential,
row and column datasets (section 3.1.2); otherwise use the non-IID track. Most common sources are not IID.

## Reading results
- Initial estimate H_I = min(H_original, n x H_bitstring, H_submitter) for non-binary sources, or
  min(H_original, H_submitter) for binary ones (section 3.1.3). With a conditioning component, update per section 3.1.5.
- Restart tests: a failed sanity check, or min(Hr, Hc) below half of H_I, fails validation with no entropy
  estimate awarded; otherwise the assessment is min(Hr, Hc, H_I) (section 3.1.4.2).

## Use the number
Size the conditioning input so the DRBG seed gets full entropy (e.g. 0.5 bits/sample needs 512 samples for
256 bits). Health test cutoffs (RCT, APT) derive from the claimed entropy.

## Verify
- [ ] Raw data path documented and reproducible; the tool output is kept with the submission material.

## Checked

2026-11-01. Confirmed against NIST SP 800-90B (sections 3.1.1 to 3.1.5, restart tests) and the
SP800-90B_EntropyAssessment README (tool flags, restart usage). Removed the worst-case-conditions
advice, the permutation-then-MCV and 10-estimator descriptions, and the ESV wording, which the
documents read did not state.

Method: documentation only; no commands were run.

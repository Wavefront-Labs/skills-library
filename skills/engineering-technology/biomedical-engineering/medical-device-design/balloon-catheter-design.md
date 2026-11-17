---
id: engineering-technology.biomedical-engineering.medical-device-design.balloon-catheter-design
name: balloon-catheter-design
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [balloon-catheter, compliance-chart, rated-burst-pressure, dilatation-balloon, semi-compliant]
level: advanced
status: gated
description: "Design balloon catheters: material and wall thickness, compliance chart, rated burst pressure with reliability, inflation and deflation time, bonds and crossing profile."
sources: ["https://www.iso.org/standard/76495.html","https://www.accessdata.fda.gov/cdrh_docs/pdf4/K041293.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Balloon catheter design

**Goal:** a balloon that reaches nominal diameter predictably, survives rated pressure and deflates quickly, on a low profile shaft.

## Elements
- **Materials:** nylon and polyamide elastomers (semi-compliant), PET (non-compliant, thin high-strength wall), polyurethane (compliant). Biaxial blow moulding sets orientation and strength (gated: unconfirmed, source is paywalled or blocked).
- **Compliance chart:** diameter versus pressure from nominal to rated burst pressure (RBP); report per size.
- **RBP:** commonly defined by a statistical statement that a very small fraction of balloons burst below RBP at a stated confidence (a frequently cited form is 99.9 percent reliability at 95 percent confidence; it appears as an acceptance criterion in FDA 510(k) summary K041293, but is not a universal rule, so confirm the expectation for your device class and regulator against ISO 10555-4:2023 and FDA recognised guidance). See confidence-reliability-sampling.
- **Profile:** folded crossing profile, wrap and re-wrap after inflation; deflation time.
- **Bonds:** balloon-to-shaft and shaft joints tested in tension and under pressure.
- **Fatigue:** repeat inflation cycles to RBP.

## Verify
- [ ] Burst and compliance data per size with the reliability statement.
- [ ] Bond tensile and leak tests; fatigue inflations; deflation time.
- [ ] Particulate and coating assessment where coated.
- [ ] Failure mode (burst as a longitudinal tear rather than a fragmenting rupture) reviewed in the risk file.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.

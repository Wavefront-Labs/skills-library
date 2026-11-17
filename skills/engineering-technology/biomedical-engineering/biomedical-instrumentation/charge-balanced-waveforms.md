---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.charge-balanced-waveforms
name: charge-balanced-waveforms
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [charge-balance, neurostimulation, stimulator-design, charge-balanced-waveforms, biphasic-pulse, blocking-capacitor, residual-dc, interphase-delay]
level: advanced
status: draft
description: "Design charge-balanced biphasic stimulation: cathodic-first pulses, interphase gap, asymmetric phases, blocking capacitors and passive discharge to keep residual DC near zero."
sources: ["Merrill, Bikson and Jefferys, Electrical stimulation of excitable tissue: design of efficacious and safe protocols (J Neurosci Methods 2005)", "ISO 14708-3 Active implantable medical devices - Implantable neurostimulators (confirm edition)", "Webster (ed.), Medical Instrumentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Charge-balanced stimulation waveforms

**Goal:** stimulate tissue with each cathodic charge returned by an anodic charge, preventing net DC that causes electrode corrosion and tissue damage.

Regulated implantable-device work; limits come from the applicable standard and the electrode and tissue data.

## Waveform choices
- **Biphasic, symmetric:** cathodic phase (excitatory) followed by equal anodic phase; simple but the anodic phase may partially cancel the effect.
- **Biphasic, asymmetric:** a short high-amplitude cathodic phase and a long, low-amplitude anodic phase with equal charge; reduces cancellation.
- **Interphase gap** (tens to hundreds of microseconds between phases) lets the cathodic phase act before reversal, improving efficiency.
- **Monophasic** pulses are used only with capacitive coupling.
- Pulse width typically 50 microseconds to a few milliseconds; frequency and amplitude depend on therapy.

## Hardware safeguards
1. **Blocking (coupling) capacitor** in series with each output so no net DC can pass even if a switch fails; size so the voltage across it stays modest during a pulse.
2. **Passive discharge:** after each pulse, short the electrodes through a switch for a few milliseconds to discharge any residual voltage.
3. **Charge-balance monitor:** measure the net charge or electrode voltage and shut down if it exceeds a threshold.
4. **Matching of current sources:** cathodic and anodic current sources never match perfectly; use the above to catch the difference.
5. Residual DC limits in neurostimulators are very small (in the order of nanoamps to a microamp) and are justified in the risk file.

## Verify
- [ ] Measure the waveform on a load model (electrode-tissue impedance network) at all amplitude and pulse-width extremes.
- [ ] Verify residual DC with and without a simulated component fault.
- [ ] Electrode charge density within the limits you set (see charge-injection-limits).

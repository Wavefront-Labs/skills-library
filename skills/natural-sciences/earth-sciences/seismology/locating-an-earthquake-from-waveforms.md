---
id: natural-sciences.earth-sciences.seismology.locating-an-earthquake-from-waveforms
name: locating-an-earthquake-from-waveforms
category: natural-sciences
field: earth-sciences
product: seismology
tags: [seismology, earthquake-location, waveform-analysis, p-wave, s-wave, phase-picking, s-p-time, travel-time, velocity-model, iasp91, hypocenter, epicenter, azimuthal-gap, obspy, fdsn, iris, earthscope, seiscomp, nonlinloc, hypoinverse, instrument-response, magnitude, focal-mechanism, depth-phases]
level: practitioner
status: gated
description: "Fetch waveforms, pick P and S arrivals, and locate an earthquake with a velocity model; judge the result by residuals, azimuthal gap and depth control, using ObsPy and FDSN."
sources: ["Stein & Wysession, An Introduction to Seismology, Earthquakes, and Earth Structure", "ObsPy documentation (docs.obspy.org)", "Havskov & Ottem\u00f6ller, Routine Data Processing in Earthquake Seismology", "https://docs.obspy.org/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Locating an earthquake from waveforms

**Goal:** from raw station data to a hypocentre with honest uncertainties, and knowing
which parts of the solution (usually depth) you actually constrained.

## 1. Get the data
With ObsPy and an FDSN data centre (e.g. EarthScope/IRIS, ORFEUS, GEOFON; in ObsPy the shortcut "IRIS" resolves to service.earthscope.org):
```python
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
c = Client("IRIS")
t = UTCDateTime("2026-01-01T12:00:00")   # placeholder origin estimate
st = c.get_waveforms("IU", "ANMO", "00", "BH?", t - 60, t + 600)
inv = c.get_stations(network="IU", station="ANMO", level="response")
st.detrend("demean"); st.taper(0.05)
st.remove_response(inventory=inv, output="VEL", pre_filt=(0.01, 0.02, 8, 10))
```
Check sample rate before choosing the high corners of `pre_filt` — they must be below
Nyquist. Response removal without a pre-filter blows up long-period noise.

## 2. Pick phases
- **P** on the vertical component: first onset of energy above noise. Zoom to
  sample level; label impulsive ("i") vs emergent ("e") and give a pick uncertainty.
- **S** on the horizontals (rotate to radial/transverse if the back-azimuth is known);
  S is often emergent and sits in P coda — pick conservatively and wider uncertainty.
- Filter to help visibility (e.g. 1–10 Hz bandpass for local events), but note that
  causal filters shift onsets; use zero-phase for viewing, check the pick on raw data.
- Automatic pickers (STA/LTA, AR-AIC, ML pickers like PhaseNet) are good first passes;
  review picks on the closest stations by eye.

## 3. Quick sanity check: S−P
For local events, distance (km) ≈ (S−P seconds) × ~8 (crustal rule of thumb: 1/(1/3.5 - 1/6) = 8.4 km per second of S-P for Vp 6, Vs 3.5 km/s). Three stations' circles give a rough epicentre — useful to catch
a mis-picked phase before running the inversion.

## 4. Locate
- Choose a **velocity model**: a local 1-D model if one exists for your region; IASP91 or
  ak135 (both load in `obspy.taup.TauPyModel`) for regional/teleseismic. The model choice can move a location by kilometres.
- Run a locator: Hypoinverse/HYPO71-style linearised (fast, needs a good start),
  NonLinLoc (probabilistic, gives a full PDF and copes with poor geometry), or
  SeisComP for network operations.
- Use relative relocation (HypoDD, GrowClust) on clusters for sharp structure.

## 5. Judge the solution
- **RMS residual** should be close to your pick uncertainty (local: roughly 0.1-0.3 s (gated: unconfirmed, source is paywalled or blocked)). A single
  large residual usually means a wrong phase or a timing problem at that station.
- **Azimuthal gap**: >180° means poor constraint perpendicular to the station cluster.
- **Depth** is only constrained if a station is within roughly one focal depth of the
  epicentre, or you have depth phases (pP, sP) teleseismically. Otherwise depth is
  traded off against origin time — report it as poorly constrained or fixed.
- Error ellipses assume your velocity model is right; real uncertainty is larger.

## 6. Magnitude (brief)
Local magnitude ML from Wood-Anderson-simulated amplitudes with a regional distance
correction; moment magnitude Mw from spectra or moment tensor inversion for larger events.
State which.

## Gotchas
- Station clock errors (check GPS status/timing quality flags in the data).
- Picking on a channel whose response has the wrong polarity or units.
- Mixing up UTC and local time when matching to felt reports.
- Overconfident depths from a network with no nearby station.

## Verify
- [ ] Response removed with an appropriate pre-filter; units known (velocity/displacement).
- [ ] Every pick has a quality/uncertainty; S picks checked on horizontals.
- [ ] S−P circles agree with the inverted epicentre.
- [ ] RMS, azimuthal gap and nearest-station distance reported with the location.
- [ ] Depth labelled fixed or free, with its constraint stated.

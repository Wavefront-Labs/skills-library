---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.biosignal-adc-selection
name: biosignal-adc-selection
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [adc-resolution, signal-conditioning, biomedical-filters, delta-sigma, enob, sampling-rate, anti-aliasing, quantization-noise]
level: practitioner
status: draft
description: "Choose an ADC for biosignals: required resolution from signal and offset, sampling rate and anti-aliasing, delta-sigma versus SAR, ENOB, input range and reference noise."
sources: ["Webster (ed.), Medical Instrumentation: Application and Design", "Kester (ed.), Data Conversion Handbook (Analog Devices)", "Kligfield et al., Recommendations for the standardization and interpretation of the electrocardiogram Part I (Circulation 2007)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# ADC selection for biosignals

**Goal:** capture the signal and its worst-case offset with enough resolution and bandwidth, and with low added noise.

## Resolution
- LSB size = full-scale range / 2^N. A DC-coupled ECG front end that must accept plus or minus 400 mV offset (800 mV span) with 16 bits has an LSB of 800 mV / 65536 = 12.2 microvolts, which is coarse for a 5 microvolt target; at 24 bits, LSB is 0.05 microvolts.
- Diagnostic ECG typically targets a resolution of 5 microvolts or finer; EEG needs better than about 1 microvolt; EMG tens of microvolts to millivolts.
- Practical resolution is the effective number of bits (ENOB) after noise, not the nominal bit count.
- Alternative: **AC-couple** or analogue offset cancellation before gain, then use a lower-bit ADC (12-16 bit); trade-offs are baseline recovery and ST distortion.

## Sampling
- Choose the sample rate above 2 times the signal bandwidth with margin: diagnostic ECG at 500 sps or higher (pacemaker pulses need much higher, several kHz), EEG 256-1000 sps, EMG 1000-4000 sps.
- **Delta-sigma ADCs** oversample internally with a digital decimation filter that provides anti-aliasing, ideal for slow biosignals, 16-24 bits, but have latency and settling after multiplexing.
- **SAR ADCs** offer low latency and multiplexing with 12-18 bits; require an analogue anti-alias filter and a driver amplifier.

## Other parameters
- Input range and PGA settings; reference noise and stability; INL and DNL (matter for small signals on large offsets); simultaneous sampling for multi-lead timing (skew between channels corrupts vectors); power and isolation requirements.

## Verify
- [ ] Noise floor measured with inputs shorted, converted to microvolts at the input.
- [ ] Full-scale offset case tested with no clipping.
- [ ] Aliasing test with out-of-band tones.

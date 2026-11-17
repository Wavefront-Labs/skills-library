---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.k-space-sampling
name: k-space-sampling
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [k-space, mri-physics, mri-hardware, fourier-transform, field-of-view, undersampling, parallel-imaging, echo-planar]
level: practitioner
status: draft
description: "Understand MRI k-space: relation to image FOV and resolution, Cartesian, radial and spiral trajectories, undersampling, partial Fourier and parallel imaging, and common artefacts."
sources: ["Bernstein, King and Zhou, Handbook of MRI Pulse Sequences", "Brown et al., Magnetic Resonance Imaging: Physical Principles and Sequence Design", "Pruessmann et al., SENSE: sensitivity encoding for fast MRI (Magn Reson Med 1999)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# k-space sampling in MRI

**Goal:** relate the acquired data to the final image so you can predict FOV, resolution, scan time and artefacts.

## The relationship
The MR signal is the Fourier transform of the image: S(kx, ky) = integral of rho(x, y) exp(-i 2 pi (kx x + ky y)) dx dy, with kx = (gamma / 2 pi) x integral of Gx dt.
- **Field of view** = 1 / delta k (spacing between k-space samples).
- **Spatial resolution** about 1 / (2 k_max) (extent of k-space coverage).
- The **centre** of k-space carries contrast and signal; the **periphery** carries edge detail.

## Trajectories
- **Cartesian (line-by-line):** one phase-encode per TR; simple, robust. Scan time = TR x number of phase-encode steps x averages.
- **Echo-planar imaging (EPI):** whole k-space in one or few shots; fast, with distortion near susceptibility and N/2 (Nyquist) ghosts.
- **Radial and spiral:** oversample the centre, tolerate motion better and enable undersampling with streaky (benign) artefacts; need gradient delay correction and regridding.
- **Partial Fourier:** acquire slightly more than half of k-space and use conjugate symmetry; reduces time, lowers SNR.

## Acceleration
- **Parallel imaging** (SENSE in image domain, GRAPPA in k-space) undersamples phase encoding using coil sensitivity differences; noise amplification is quantified by the g-factor; acceleration factor R above the number of coil elements is not possible.
- **Compressed sensing** exploits sparsity with random undersampling and nonlinear reconstruction.

## Common artefacts
- **Aliasing (wrap-around)** if FOV is less than the object (phase direction).
- **Gibbs ringing** from truncated k-space.
- **Motion ghosts** along the phase-encode direction.
- **Zipper artefacts** from RF leakage.

## Verify
- [ ] Compute FOV and resolution from the sequence parameters and compare to scanner readout.
- [ ] Simulate undersampling on a phantom and observe aliasing patterns.
- [ ] Check noise amplification (g-factor) for the coil and R used.

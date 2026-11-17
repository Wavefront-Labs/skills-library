---
id: natural-sciences.neuroscience.computational-neuroscience.simulating-neuron-and-network-models
name: simulating-neuron-and-network-models
category: natural-sciences
field: neuroscience
product: computational-neuroscience
tags: [computational-neuroscience, neuroscience, neural-modelling, leaky-integrate-and-fire, lif, hodgkin-huxley, izhikevich, spiking-network, rate-model, brian2, nest, neuron-simulator, python, numerical-integration, euler, time-step, balanced-network, e-i-balance, parameter-sweep, model-fitting, reproducibility, random-seed, firing-rate, cv-isi]
level: advanced
status: verified
description: "Build and simulate neuron and network models: choose model complexity, implement LIF/HH in Brian2/NEST/NEURON, pick time steps, sweep parameters, validate against data and keep it reproducible."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Simulating neuron and network models

**Goal:** a model that answers a specific question about neural mechanism, with
numerics you trust and results others can reproduce.

## 1. Pick the simplest model that can answer the question
- **Rate models** (firing rates evolve via ODEs): population dynamics, attractors,
  working-memory or decision models; fast and analysable.
- **Leaky integrate-and-fire (LIF)** and variants (adaptive exponential, Izhikevich):
  spike timing and network statistics with thousands to millions of neurons.
- **Hodgkin–Huxley-type conductance models:** channel mechanisms, action-potential
  shape, pharmacology.
- **Multi-compartment morphological models:** dendritic integration, backpropagating spikes.
More detail = more parameters you can't constrain. State what the model must explain
and which data constrain it, before choosing.

## 2. A minimal LIF network (Brian2 sketch)
```python
from brian2 import *
seed(42)   # set before any random draws
tau=20*ms; v_rest=-70*mV; v_th=-50*mV; v_reset=-65*mV
eqs = 'dv/dt = (v_rest - v + I)/tau : volt (unless refractory)\nI : volt'
G = NeuronGroup(1000, eqs, threshold='v>v_th', reset='v=v_reset',
                refractory=2*ms, method='exact')
G.v = 'v_rest + rand()*(v_th - v_rest)'   # random initial conditions
G.I = 22*mV
S = Synapses(G, G, on_pre='v += 0.2*mV'); S.connect(p=0.1)
M = SpikeMonitor(G); run(1*second)
```
Brian2 handles units (catching many dimension errors). Alternatives: **NEST** for
large point-neuron networks, **NEURON** for morphological models, plain NumPy/SciPy
for small ODE systems, **Jaxley**/JAX-based tools for gradient-based fitting.

## 3. Numerics
- **Time step:** common dt = 0.1 ms for LIF networks; HH models may need 0.01–0.025 ms.
  Halve dt and confirm results (spike counts, statistics) don't change materially.
- Forward Euler is simple but can be unstable for stiff equations; use exact
  integration for linear subthreshold dynamics, or RK4/implicit solvers for HH.
- Spike times are quantised to dt on grid-based simulators; matters for synchrony.
- Delays must be ≥ dt; NEST requires delays as multiples of the resolution.

## 4. Network design checks
- Specify connectivity (probability, in-degree), weights, delays and external drive.
- **E/I balance**: in balanced networks, irregular asynchronous firing (CV of ISI
  near 1, low synchrony) emerges for suitable inhibition dominance; check regime with
  firing rate, CV-ISI, and pairwise correlations.
- Discard an initial transient (e.g. first 100–200 ms) before computing statistics.
- Scale: changing network size changes fluctuations; rescale weights (e.g. 1/√K)
  deliberately if you resize.

## 5. Parameter exploration and fitting
- Sweep parameters on a grid or with random/Sobol sampling; plot regimes (phase
  diagrams). Run several random seeds per point and report variability.
- Fit to data with explicit loss functions (feature-based: spike rate, adaptation
  index, AP width), using evolutionary algorithms, Bayesian optimisation, or
  simulation-based inference (e.g. `sbi`). Report parameter identifiability
  (many parameter sets may fit equally well).

## 6. Validate and reproduce
- Validate on data **not** used for fitting; make out-of-sample predictions.
- Version-control code, pin simulator versions (environment file/container), record seeds.
- Share code and parameters in a standard description table (model, populations,
  connectivity, inputs, measurements) as in published network-model reporting guidelines.

## Gotchas
- Units: mixing mV and V or ms and s silently breaks NumPy models.
- Results that depend on dt or a single seed are artefacts.
- An over-parameterised model can fit anything; explanation needs constraints.

## Verify
- [ ] Model complexity justified by the question and constraining data.
- [ ] dt halving and integrator choice leave results unchanged.
- [ ] Network regime characterised (rates, CV-ISI, correlations) after transient.
- [ ] Multiple seeds and parameter sweeps reported.
- [ ] Code, versions, seeds and parameters archived for reproduction.

Run check: the Brian2 block executes unchanged on Brian2 (numpy code generation, no C compiler): 1000 neurons, I = 22 mV, mean rate about 23 Hz, mean CV-ISI about 0.04. That is regular, tonic firing, not the irregular balanced regime of section 4. Add inhibitory synapses and noisy input for that.

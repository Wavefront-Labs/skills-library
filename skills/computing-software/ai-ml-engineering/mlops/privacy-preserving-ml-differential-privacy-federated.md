---
id: computing-software.ai-ml-engineering.mlops.privacy-preserving-ml-differential-privacy-federated
name: privacy-preserving-ml-differential-privacy-federated
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, differential-privacy, federated-learning, opacus, flower, privacy-engineering]
level: practitioner
status: draft
description: "Train with privacy guarantees: DP-SGD with Opacus and epsilon accounting, federated learning with Flower and secure aggregation, and when each actually protects data."
sources:
  - https://opacus.ai/tutorials/
  - https://github.com/tensorflow/privacy
  - https://flower.ai/docs/framework/
  - https://csrc.nist.gov/pubs/sp/800/226/final
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Privacy-preserving ML (differential privacy, federated learning)

**Goal:** models trained on sensitive data do not memorise or leak individual records, with a stated, measurable privacy guarantee.

## Threats
Membership inference (was this person in training?), training data extraction (LLMs regurgitating records), attribute inference. Removing names is not protection; models memorise rare records.

## Differential privacy with DP-SGD (Opacus)
```python
from opacus import PrivacyEngine
from opacus.validators import ModuleValidator
model = ModuleValidator.fix(model)            # e.g. BatchNorm -> GroupNorm
engine = PrivacyEngine()
model, optimizer, loader = engine.make_private_with_epsilon(
    module=model, optimizer=optimizer, data_loader=loader,
    target_epsilon=8.0, target_delta=1e-5, epochs=EPOCHS, max_grad_norm=1.0)
# train as usual
print(engine.get_epsilon(delta=1e-5))
```
- Per-sample gradient clipping (`max_grad_norm`) plus calibrated noise; the accountant tracks cumulative epsilon.
- `delta` well below 1/N (training set size).
- Expect accuracy loss and slower training; larger batches and pretrained public models (fine-tune with DP) recover much of it.
- Epsilon is a policy decision: report it with delta, the unit of privacy (record vs user), and the accountant. Hyperparameter tuning on private data also spends budget.
TensorFlow: `tensorflow_privacy` DP Keras optimizers provide the same mechanism.

## Federated learning (Flower)
Data stays on clients; only model updates leave.
```python
import flwr as fl
class Client(fl.client.NumPyClient):
    def get_parameters(self, config): return get_weights(model)
    def fit(self, parameters, config):
        set_weights(model, parameters); train(model, local_data); return get_weights(model), len(local_data), {}
    def evaluate(self, parameters, config):
        set_weights(model, parameters); loss, acc = test(model, local_val); return loss, len(local_val), {"acc": acc}
strategy = fl.server.strategy.FedAvg(fraction_fit=0.1, min_available_clients=50)
```
- Updates can leak data (gradient inversion): add secure aggregation (server sees only the sum) and DP on client updates for real guarantees.
- Non-IID client data slows convergence; FedProx and personalization help.
- Ops: client availability, stragglers, versioning, and attacks via poisoned updates (robust aggregation).

## Choosing
Central DP when you hold the data but must limit what the model reveals; federated (+ secure aggregation + DP) when data cannot be centralised (devices, hospitals); both are complements to access control, minimisation and retention limits.

## Verify
- [ ] Reported epsilon, delta and privacy unit for every DP model.
- [ ] Membership-inference test shows near-chance advantage on held-out vs training records.
- [ ] Federated setup uses secure aggregation; server never logs individual updates.

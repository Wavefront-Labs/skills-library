---
id: computing-software.ai-ml-engineering.pytorch.overfit-one-batch-and-shape-sanity-checks
name: overfit-one-batch-and-shape-sanity-checks
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, overfit-one-batch, sanity-checks, debugging, training-loop, shape-errors, initial-loss]
level: practitioner
status: verified
description: "Prove a PyTorch model and loop can learn before scaling up: overfit one batch, check initial loss, shapes, label alignment and gradient flow per layer."
sources:
  - https://karpathy.github.io/2019/04/25/recipe/
  - https://pytorch.org/tutorials/beginner/basics/optimization_tutorial.html
  - https://pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Overfit one batch and shape sanity checks

**Goal:** catch wiring bugs (wrong labels, wrong loss input, frozen layers, broadcasting) in five minutes instead of after a three-day run.

## 1. Check the loss at step 0
Before any optimizer step, the loss should equal the "know nothing" value:
- Cross-entropy over C balanced classes: `-ln(1/C)` (10 classes -> 2.303, 1000 -> 6.908).
- Binary with `BCEWithLogitsLoss` and zero-mean logits: `ln 2 = 0.693`.
- Regression with MSE and zero output: `mean(y**2)`, which equals `var(y)` only when targets have zero mean (about 1.0 for standardised targets; tested).
A much larger value means the final layer init is too large or you feed probabilities into a loss that expects logits (`CrossEntropyLoss` already applies log-softmax; adding `softmax` before it is the classic bug). Fix by zero-initialising or scaling down the last layer and setting its bias to the class prior log-odds for imbalanced data.

## 2. Overfit a single batch
```python
model.train()
xb, yb = next(iter(train_loader))          # fixed batch, e.g. 8-32 examples
xb, yb = xb.to(dev), yb.to(dev)
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
for step in range(500):
    opt.zero_grad(set_to_none=True)
    loss = loss_fn(model(xb), yb)
    loss.backward()
    opt.step()
    if step % 50 == 0:
        print(step, loss.item())
```
- Expect loss near 0 and 100% train accuracy on that batch. If it plateaus, the problem is in the model/loss/labels, not in data volume or hyperparameters.
- Turn off regularisation for this test (dropout, weight decay, augmentation), or it may not reach 0.
- If it never moves: check `opt` holds the right parameters (`sum(p.numel() for g in opt.param_groups for p in g['params'])`), that no layer is accidentally `requires_grad=False`, and that the loss is not detached (`loss.requires_grad` must be True).

## 3. Shape and broadcasting traps
- `MSELoss(pred, y)` with `pred` shape `(N, 1)` and `y` shape `(N,)` broadcasts to `(N, N)` and silently trains on garbage. PyTorch only warns. Assert shapes: `assert pred.shape == y.shape`.
- `CrossEntropyLoss` wants logits `(N, C)` (or `(N, C, d1...)`) and integer targets `(N,)` of dtype `long`, not one-hot (unless you pass class probabilities deliberately).
- Sequence models: `(batch, seq, feat)` vs `(seq, batch, feat)` - check `batch_first=True` on `nn.LSTM` / `nn.TransformerEncoderLayer`.
- Images: `channels_last` vs `(N, C, H, W)`; a model that accepts `(N, H, W, C)` without error may have a `Linear` absorbing the wrong axis.

## 4. Check labels line up with inputs
- Visualise or print 10 `(x, y)` pairs straight out of the DataLoader, after all transforms. Shuffling inputs and labels separately, or sorting one list, is common.
- Shuffle labels deliberately: a model trained on shuffled labels should do no better than chance on validation. If it does better, there is leakage.

## 5. Gradient flow per layer
```python
loss.backward()
for n, p in model.named_parameters():
    if p.grad is None:
        print("NO GRAD", n)
    else:
        print(f"{n:40s} {p.grad.norm():.2e}")
```
`None` grads mean the parameter is not in the graph (unused branch, `torch.no_grad` region, a `.detach()` or `.item()` in the forward). Norms of 0 in early layers point to dead ReLUs or saturated activations.

## 6. Data-independence test
Feed all-zero inputs: the model should do worse than with real inputs. If it does just as well, it is not using `x` (for example a bug overwrote features).

## Verify
- [ ] Step-0 loss matches the analytical baseline within ~10%.
- [ ] A single batch reaches near-zero loss with regularisation off.
- [ ] `pred.shape == target.shape` asserted for regression; target dtype `long` for CE.
- [ ] Every trainable parameter has a non-None gradient after one backward pass.
- [ ] Shuffled-label run scores at chance on validation.

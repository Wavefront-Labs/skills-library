---
id: computing-software.ai-ml-engineering.feature-engineering.on-demand-request-time-features
name: on-demand-request-time-features
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, on-demand-features, request-time-features, feast, online-features, feature-store]
level: practitioner
status: draft
description: "Compute features at request time: Feast on-demand feature views, combining request data with stored features, latency budgets, train/serve parity and logging served features."
sources:
  - https://docs.feast.dev/reference/beta-on-demand-feature-view
  - https://docs.feast.dev/getting-started/concepts/feature-view
  - https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# On-demand / request-time features

**Need:** some features depend on the request itself (transaction amount vs the customer's stored average, distance between request location and home, time since last login at request time) and cannot be precomputed.

## Feast on-demand feature view
```python
from feast import Field, RequestSource, on_demand_feature_view
from feast.types import Float64, Int64
import pandas as pd

txn_request = RequestSource(name="txn", schema=[Field(name="amount", dtype=Float64)])

@on_demand_feature_view(sources=[customer_stats_fv, txn_request],
                        schema=[Field(name="amount_to_avg_ratio", dtype=Float64)],
                        mode="pandas")
def amount_features(inputs: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame()
    out["amount_to_avg_ratio"] = inputs["amount"] / inputs["avg_amount_30d"].clip(lower=1.0)
    return out
```
Online: `store.get_online_features(features=["amount_features:amount_to_avg_ratio"], entity_rows=[{"customer_id": 42, "amount": 310.0}])`. Offline: the same function runs in `get_historical_features` when the request columns are present in the entity dataframe, giving parity. `mode="python"` avoids pandas overhead for low latency.

## Design rules
- Keep transformations cheap and deterministic (ms budget); heavy work belongs in batch/streaming features.
- One implementation used for both training and serving (feature store transformation, or a shared library imported by both).
- Log the exact feature vector served with each prediction (with request id). Training on logged features eliminates skew for future models.

## Without a feature store
Implement as a preprocessing step inside the model artifact (sklearn FunctionTransformer / custom layer) receiving raw request fields plus fetched stored features.

## Verify
- [ ] Parity test: compute features for historical requests through the offline path and the online path; values match within float tolerance.
- [ ] p99 latency of feature computation measured under load.

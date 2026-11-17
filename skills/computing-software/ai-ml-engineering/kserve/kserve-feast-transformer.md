---
id: computing-software.ai-ml-engineering.kserve.kserve-feast-transformer
name: kserve-feast-transformer
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [feast, feature-store, online-features, redis, driver-transformer, feast-serving-url, entity-id-name, feature-refs]
level: practitioner
status: docs-checked
description: "Fetch Feast online features (Redis store, feature-server on 6566) in a KServe transformer with feast_serving_url, entity_id_name and feature_refs args."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/predictive-inference/transformers/feast-feature-store/feast-feature-store.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Feast online features in a transformer

Example uses Feast 0.30.2 with Redis as the online store. The transformer replaces plain input transformation with online feature augmentation before calling the model.

Pieces:
1. Redis Deployment (`redis` image, port 6379, `--appendonly yes`) plus a `redis-service` Service.
2. Feast server Deployment `feature-server` (port 6566, args `-c /mnt/driver_feature_repo/feature_repo serve -h 0.0.0.0`) with an init container `feature-store-initializer` that creates a sample feature repo, loads sample driver data into the online store and copies the repo to a shared `emptyDir` mounted at `/mnt`. Expose as `feature-server-service`.
3. A transformer image whose `DriverTransformer` extends `Model`; `preprocess` fetches features and `postprocess` returns the result. For a gRPC predictor you must override `predict` yourself.

```yaml
spec:
  transformer:
    containers:
      - name: driver-container
        image: "kserve/driver-transformer:latest"
        command: ["python", "-m", "driver_transformer"]
        args:
          - --feast_serving_url
          - "feature-server-service.default.svc.cluster.local:6566"
          - --entity_id_name
          - "driver_id"
          - --feature_refs
          - "driver_hourly_stats:conv_rate"
          - "driver_hourly_stats:acc_rate"
          - "driver_hourly_stats:avg_daily_trips"
  predictor:
    model:
      modelFormat: {name: sklearn}
      storageUri: "gs://kfserving-examples/models/feast/driver"
```

Request: `{"instances": [[1001], [1002]]}` (entity ids) to `/v1/models/NAME:predict`; the transformer adds the features before the sklearn model scores them. The page builds its own `feature-store-initializer`, `feast-server` and `driver-transformer` images from the KServe repository's Dockerfiles and pushes them to your registry, so replace the image placeholders first.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed against the KServe website Feast feature store page: Feast 0.30.2, Redis args and ports, feature server args, init container and volume, transformer arguments, gRPC `predict` override note, manifest and request body. No claims removed.

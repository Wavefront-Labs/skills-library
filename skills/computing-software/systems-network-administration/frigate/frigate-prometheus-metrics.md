---
id: computing-software.systems-network-administration.frigate.frigate-prometheus-metrics
name: frigate-prometheus-metrics
category: computing-software
field: systems-network-administration
product: frigate
tags: [prometheus-metrics, api-metrics-endpoint, detector-inference-speed, storage-metrics, promql, telemetry]
level: practitioner
status: docs-checked
description: "Scrape Frigate's Prometheus metrics endpoint and use its system, camera, detector and storage gauges in PromQL."
sources: ["https://docs.frigate.video/configuration/metrics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Frigate Prometheus metrics

Frigate exposes Prometheus metrics at `/api/metrics`, available by default with no extra configuration (telemetry options are under Settings, System, Telemetry).

Metric groups:
- System: `frigate_cpu_usage_percent` and `frigate_mem_usage_percent` (per process), `frigate_gpu_usage_percent`, `frigate_gpu_mem_usage_percent`.
- Camera: `frigate_camera_fps` (consumed), `frigate_detection_fps`, `frigate_process_fps`, `frigate_skipped_fps`, `frigate_detection_enabled`, `frigate_audio_dBFS`, `frigate_audio_rms`.
- Detector: `frigate_detector_inference_speed_seconds`, `frigate_detection_start`.
- Storage: `frigate_storage_free_bytes`, `total_bytes`, `used_bytes` and `frigate_storage_mount_type`. These report the whole filesystem as the operating system sees it (the same numbers as `df`), not Frigate's own recordings footprint.
- Service: `frigate_service_uptime_seconds`, `frigate_service_last_updated_timestamp`, `frigate_device_temperature`.
- Events: `frigate_camera_events{camera, label}` is the count of camera events since the exporter started.
Metric types: `frigate_camera_events` is a counter, `frigate_storage_mount_type` is an Info metric, and the page's example of a gauge is `frigate_cpu_usage_percent`.

Prometheus scrape config from the docs: `job_name: "frigate"`, `metrics_path: "/api/metrics"`, `static_configs` target `frigate:5000`, `scrape_interval: 15s`.

Example queries: `avg(frigate_cpu_usage_percent)`, `sum(frigate_gpu_mem_usage_percent)`, `rate(frigate_detection_fps{camera_name="front_door"}[5m])`, `(frigate_storage_used_bytes / frigate_storage_total_bytes) * 100` and `increase(frigate_camera_events[1h])`. Useful dashboard panels: CPU, memory and GPU over time, camera and detection FPS, storage trends, event counts and temperatures. The docs say a sample Grafana dashboard JSON is planned.

## Checked

2026-11-04. Confirmed against the Metrics page: endpoint and default availability, all metric names and groups, storage figures matching df, scrape config, example queries, dashboard ideas and the planned sample dashboard. Fixed the metric type claim (events is a counter) and the events description, and replaced an example query with the page's own.
Method: documentation only; no commands were run.

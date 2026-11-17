---
id: computing-software.qa-testing-engineering.selenium.grid-video-recording-vnc
name: grid-video-recording-vnc
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [grid-video-recording, selenium-video, novnc, se-recordvideo]
level: practitioner
status: docs-checked
description: "Record videos and watch live sessions on Selenium Grid: noVNC on node containers, the selenium/video sidecar, se:recordVideo in dynamic grid and file naming."
sources:
  - https://github.com/SeleniumHQ/docker-selenium/blob/trunk/README.md
  - https://github.com/SeleniumHQ/docker-selenium/blob/trunk/ENV_VARIABLES.md
  - https://github.com/SeleniumHQ/docker-selenium/tree/trunk/charts/selenium-grid
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Video recording and VNC on Grid nodes

## Watch live (noVNC)
docker-selenium node/standalone images expose noVNC on **7900**: open `http://<host>:7900/?autoconnect=1&resize=scale&password=secret`. The VNC server listens on 5900 (`SE_VNC_PORT`); the default VNC password is `secret` (`SE_VNC_PASSWORD`, or `SE_VNC_NO_PASSWORD=true`). Disable VNC to save resources with `SE_START_VNC=false`.

## Video sidecar (static grid)
```yaml
  chrome:
    image: selenium/node-chrome:<tag>
    shm_size: 2gb
    environment: { SE_EVENT_BUS_HOST: selenium-hub, SE_EVENT_BUS_PUBLISH_PORT: 4442, SE_EVENT_BUS_SUBSCRIBE_PORT: 4443 }
  chrome_video:
    image: selenium/video:<tag>
    volumes: ["./videos:/videos"]
    depends_on: [chrome]
    environment:
      DISPLAY_CONTAINER_NAME: chrome
      SE_VIDEO_FILE_NAME: auto        # <se:name>_<sessionId>.mp4 from session capabilities
      SE_NODE_GRID_URL: http://selenium-hub:4444
```
One video container per node container (a 1-to-1 mapping). With `SE_VIDEO_FILE_NAME=auto` the file name is built from the `se:name` capability plus the session id (spaces become `_`; only letters, digits, `-` and `_` are kept). Videos are written to `/videos` in the video container. With several video containers set distinct file names. Headless browsers cannot be recorded.

## Dynamic grid
Set `video-image` in the `[docker]` config and request `se:recordVideo: true` per session; videos and session information land in the mounted assets folder.

## Practice
- Video recording uses considerable CPU; the README suggests estimating 1 CPU per video container plus 1 CPU per browser container.
- `se:recordVideo` on a session overrides `SE_RECORD_VIDEO`, so recording can be off by default and enabled per test.
- Name sessions (`se:name` = test id) so videos map to failures.
- Upload is done with rclone via `SE_UPLOAD_DESTINATION_PREFIX`; ship videos as CI artifacts with retention limits.

## Gotchas
- In the Helm chart, recording runs inside the node container by default (chart 0.44.0 and later); `videoRecorder.sidecarContainer: true` restores a sidecar.

## Verify
A failing CI test has a matching MP4 named after the test in the artifact bundle.

## Checked

Checked 2026-10-25 against the docker-selenium repository (pushed 2026-10-20; README, ENV_VARIABLES.md, chart README). Confirmed: noVNC on 7900 with the `secret` password and the autoconnect URL, `SE_START_VNC`, `SE_VNC_PASSWORD`, `SE_VNC_NO_PASSWORD`, the sidecar compose layout with `DISPLAY_CONTAINER_NAME`, `SE_VIDEO_FILE_NAME=auto` naming rule, `se:recordVideo` precedence over `SE_RECORD_VIDEO`, the dynamic grid `video-image` key, the CPU estimate, headless not recordable, rclone upload variables. Corrected: auto file name is `se:name` plus session id, not just `se:name`. Removed: the Grid UI camera-icon claim, the max-sessions-1 advice and the delete-on-pass tip.

Method: documentation only; no commands were run.

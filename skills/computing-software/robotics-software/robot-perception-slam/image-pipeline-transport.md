---
id: computing-software.robotics-software.robot-perception-slam.image-pipeline-transport
name: image-pipeline-transport
category: computing-software
field: robotics-software
product: robot-perception-slam
tags: [image-transport, image-proc, rectify, compressed-image, cv-bridge, republish]
level: practitioner
status: docs-checked
description: "Rectify and transport images with image_proc, image_transport plugins and convert with cv_bridge."
sources:
  - https://github.com/ros-perception/image_pipeline/blob/rolling/image_proc/doc/components.rst
  - https://github.com/ros-perception/image_pipeline/blob/rolling/image_proc/doc/tutorials.rst
  - https://github.com/ros-perception/vision_opencv/blob/rolling/cv_bridge/python/cv_bridge/core.py
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/interfaces/topics/About-Quality-of-Service-Settings.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Image pipeline
```bash
ros2 run image_proc rectify_node --ros-args -r image:=/camera/image_raw -r camera_info:=/camera/camera_info   # publishes image_rect
```
```python
from cv_bridge import CvBridge
bridge = CvBridge()
cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
out = bridge.cv2_to_imgmsg(gray, encoding='mono8'); out.header = msg.header   # keep stamp and frame
```
- `image_proc` is a set of components, each also a standalone node: `rectify_node` (subscribes `image` and `camera_info`, publishes `image_rect`), `debayer_node` (subscribes `image_raw`, publishes `image_mono` and `image_color`), `resize_node`, `crop_decimate_node`. The docs recommend composing them in one container to avoid serialising images between components.
- Each component has an `image_transport` parameter (default `raw`) that selects the transport.
- `cv_bridge`'s `imgmsg_to_cv2(img_msg, desired_encoding='passthrough')` converts to an OpenCV image; with `passthrough` the encoding of the message is kept. `cv2_to_imgmsg` converts back and takes an optional `header`.
- Copy `header.stamp` and `frame_id` from the source message when you publish a derived image.
- The QoS page describes the sensor data profile as best effort reliability with a smaller queue.

## Gotchas
- Check the encoding string you request; a conversion that is not possible raises `CvBridgeError`.

## Self-check
`ros2 topic hz /camera/image_rect` equals the camera rate and the image displays correctly.

## Checked
2026-11-03. Confirmed in the image_proc component docs and launch tutorial (node names, topics, `image_transport` parameter, composition advice), cv_bridge `core.py` (`imgmsg_to_cv2`, `cv2_to_imgmsg` signatures, passthrough, `CvBridgeError`) and the QoS page (sensor data profile). Removed: `ros2 run image_proc image_proc` (no such executable in the package), the `image_color` output of the rectifier, `rqt_image_view`, the `image_transport` `republish` command and the compressed/theora variants, and the BGR versus RGB and lossy-depth gotchas.
Method: documentation only; no commands were run.

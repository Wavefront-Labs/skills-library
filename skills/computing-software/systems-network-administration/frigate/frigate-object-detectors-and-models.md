---
id: computing-software.systems-network-administration.frigate.frigate-object-detectors-and-models
name: frigate-object-detectors-and-models
category: computing-software
field: systems-network-administration
product: frigate
tags: [object-detectors, models-list, edgetpu, openvino, onnx-detector, tensorrt, model-scenes, model-resolution]
level: advanced
status: docs-checked
description: "Choose a Frigate detector for your hardware, configure the models list with devices, run several models by scene and pick a model size."
sources: ["https://docs.frigate.video/configuration/object_detectors/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Object detectors and the models list

Object detection is configured through a `models` list. Each entry holds `devices`, `path`, `model_type`, `width` and `height`. A device is a detector type, optionally followed by a colon and a device, such as `edgetpu:pci:0`, `edgetpu:usb`, `openvino:GPU`, `openvino:NPU`, `tensorrt:0` or plain `onnx`. By default Frigate uses a single CPU detector, which the docs do not recommend; OpenVINO in CPU mode is usually better.

Hardware groups in the docs: Coral EdgeTPU, Hailo, MemryX and DEEPX for most hardware; ROCm and ONNX for AMD; OpenVINO and ONNX for Intel (6th gen Skylake and newer, also AMD CPUs although unofficial); ONNX in the `-tensorrt` image for Nvidia; TensorRT with the `-tensorrt-jp6` image for Jetson; RKNN for Rockchip. For ONNX the build decides the backend: `-rocm` uses ROCm, the default image uses OpenVINO, `-tensorrt` uses Nvidia.

More throughput: repeat a device (`openvino:GPU` twice, or `onnx` twice) to run multiple detectors. Coral, MemryX and Axelera Metis devices can only be opened by one process, so those cannot be repeated. On Intel Core Ultra, use the NPU for detection and the GPU for enrichments; the NPU needs `/dev/accel:/dev/accel` passed into the container and host firmware at least as new as the bundled driver.

Scenes: give a model `scene: thermal` and set `detect.scene: thermal` on a camera to use a different model for it. The `default` scene covers every camera that does not set one. Do not duplicate one model under several scenes to dedicate detectors to cameras; every detector already serves all cameras on that model.

Model size: `320x320` is the best choice for nearly all setups, as Frigate compensates by cropping regions. Larger variants (tiny, small, medium) are slower and gradually more accurate. For TensorRT on Jetson, models are generated at first start into `/config/model_cache/tensorrt`, selected with the `YOLO_MODELS` variable (for example `yolov7-320,yolov7x-640`); append `-dla` for DLA hardware and set `USE_FP16=False` if the GPU lacks FP16.

## Checked

Method: docs-checked 2026-11-09 against docs.frigate.video/configuration/object_detectors (read as raw markdown from the blakeblackshear/frigate docs folder); documentation only, no commands were run.

Confirmed against those pages: the settings, topics, defaults and procedures described above.

Removed or corrected: Nothing removed.

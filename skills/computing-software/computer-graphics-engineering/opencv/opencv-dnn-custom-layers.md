---
id: computing-software.computer-graphics-engineering.opencv.opencv-dnn-custom-layers
name: opencv-dnn-custom-layers
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-dnn, dnn-custom-layers, unsupported-layer, registerlayer, opencv-dnn]
level: advanced
status: docs-checked
description: "Handle unsupported layers in OpenCV DNN: the can't-create-layer error, deriving cv::dnn::Layer, registering custom layers in C++ and via cv2.dnn_registerLayer."
sources: ["https://raw.githubusercontent.com/opencv/opencv/4.x/doc/tutorials/dnn/dnn_custom_layers/dnn_custom_layers.md", "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/dnn/edge_detection.py", "https://raw.githubusercontent.com/opencv/opencv/4.x/modules/dnn/include/opencv2/dnn/layer.details.hpp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unsupported layers and custom layer registration

Typical failure when the importer meets an unknown layer type (tutorial):
`Unspecified error: Can't create layer "layer_name" of type "MyType" in function getLayerInstance`.
`MyType` is the type of the unimplemented layer.

## Options
1. File a feature request at the OpenCV issue tracker with the model source and layer type; it may be implemented if the community shares the need.
2. Define a custom layer so the dnn engine knows how to run it.

## C++ custom layer
Derive from `cv::dnn::Layer` and provide:
- a constructor that reads hyper-parameters from `cv::dnn::LayerParams` (trainable weights are already in the layer's `blobs`);
- a static `create` that returns a `cv::Ptr` to a new instance;
- `getMemoryShapes` to return output shapes from input shapes (extra memory can be requested through `internals`);
- `forward` to compute outputs from inputs;
- optional `finalize`.

Register before importing the model with `CV_DNN_REGISTER_LAYER_CLASS(Type, Class)` (place it inside function code); `CV_DNN_REGISTER_LAYER_CLASS_STATIC` registers at module load time and goes outside function code (layer.details.hpp).

Call order (tutorial): `create` once, then `getMemoryShapes` for every created layer, then `finalize`; after initialisation only `forward` is called per input.
- OpenCV manages layer memory and often reuses it, so `forward` must not rely on `outputs` or `internals` still holding data from the previous call.
- Varying input height, width or batch size makes OpenCV reallocate all internal memory; deploy with a fixed batch size and image dimensions.
- For TensorFlow imports, node `attr` values go into `LayerParams` and input `Const` blobs into `Layer::blobs`.

## Python custom layer
The tutorial example replaces Caffe's `Crop` layer (top-left cropping in current Caffe and OpenCV) with a centre crop for the HED edge model.
```python
class CropLayer(object):
    def __init__(self, params, blobs):
        self.xstart = self.xend = self.ystart = self.yend = 0
    def getMemoryShapes(self, inputs):
        inputShape, targetShape = inputs[0], inputs[1]
        batchSize, numChannels = inputShape[0], inputShape[1]
        height, width = targetShape[2], targetShape[3]
        self.ystart = (inputShape[2] - targetShape[2]) // 2
        self.xstart = (inputShape[3] - targetShape[3]) // 2
        self.yend = self.ystart + height
        self.xend = self.xstart + width
        return [[batchSize, numChannels, height, width]]
    def forward(self, inputs):
        return [inputs[0][:,:,self.ystart:self.yend,self.xstart:self.xend]]
cv.dnn_registerLayer('Crop', CropLayer)
net = cv.dnn.readNet(prototxt, caffemodel)   # register before reading
```
Both `getMemoryShapes` and `forward` must return lists (tutorial note). The type string passed to the register call is the layer type from the error message.

## Verify
- [ ] The network imports without the "Can't create layer" error and its output matches the source framework's output on the same input.

## Checked
Method: docs-checked 2026-11-09 against the dnn_custom_layers tutorial markdown, samples/dnn/edge_detection.py and layer.details.hpp, all raw GitHub (4.x); docs.opencv.org was not readable.
Removed as unconfirmed: all ONNX export advice (opset, einsum, grid_sample, dynamic_axes), the onnx-simplifier command (page not read), release-specific op additions (4.8, 4.10), Python layers being slow or breaking GPU fusion, the ONNX Runtime or OpenVINO alternative, the 1e-4 tolerance, and the example error text for ONNX nodes. Tags trimmed (onnx-simplifier).

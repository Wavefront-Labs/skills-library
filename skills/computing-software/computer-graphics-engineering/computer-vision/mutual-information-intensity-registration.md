---
id: computing-software.computer-graphics-engineering.computer-vision.mutual-information-intensity-registration
name: mutual-information-intensity-registration
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, alignment-stitching, mutual-information, image-registration, simpleitk, multimodal-registration, medical-imaging]
level: advanced
status: verified
description: "Register images with different intensities (multimodal, medical) using mutual information: SimpleITK registration setup, sampling, multi-resolution, optimisers and validation."
sources: ["https://simpleitk.readthedocs.io/en/master/registrationOverview.html", "https://itk.org/ItkSoftwareGuide.pdf", "https://doi.org/10.1109/42.563664"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Intensity-based registration (mutual information)

Feature matching fails when intensities differ non-linearly (MRI vs CT, IR vs visible, stained vs
unstained). Mutual information (MI) measures statistical dependence of intensities and is maximised
at alignment without assuming a linear relationship.

## SimpleITK rigid/affine
```python
import SimpleITK as sitk
fixed = sitk.ReadImage("ct.nii.gz", sitk.sitkFloat32); moving = sitk.ReadImage("mr.nii.gz", sitk.sitkFloat32)
init = sitk.CenteredTransformInitializer(fixed, moving, sitk.Euler3DTransform(),
                                         sitk.CenteredTransformInitializerFilter.GEOMETRY)
R = sitk.ImageRegistrationMethod()
R.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
R.SetMetricSamplingStrategy(R.RANDOM); R.SetMetricSamplingPercentage(0.05)
R.SetInterpolator(sitk.sitkLinear)
R.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=200, convergenceWindowSize=10)
R.SetOptimizerScalesFromPhysicalShift()
R.SetShrinkFactorsPerLevel([4, 2, 1]); R.SetSmoothingSigmasPerLevel([2, 1, 0])
R.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()
R.SetInitialTransform(init, inPlace=False)
tx = R.Execute(fixed, moving)
out = sitk.Resample(moving, fixed, tx, sitk.sitkLinear, 0.0)
```
- `SetOptimizerScalesFromPhysicalShift` balances rotation (radians) and translation (mm) parameter step sizes.
- The block above ran end to end on a synthetic 48x48x48 phantom (all calls valid, including `SetMetricFixedMask`), but there its result did not recover the known transform (the coarsest level is only 12 voxels wide): tune the sampling percentage, shrink levels and learning rate on your data and always check the target registration error.
- Multi-resolution pyramid avoids local maxima; initialise by geometry centre or moments.
- Then deformable: `BSplineTransformInitializer` with MI, or use elastix/ANTs for production.

## 2D in OpenCV
OpenCV has no MI metric; `findTransformECC` assumes photometric linearity (on a contrast-inverted copy it stopped with "Iterations do not converge").
Use SimpleITK on 2D images or compute MI from `np.histogram2d` and optimise with scipy (on cameraman against an inverted, nonlinearly remapped, shifted copy, correlation was -0.88 yet an exhaustive MI search peaked exactly at the true (3, 5) pixel shift and `scipy.optimize.minimize(method="Powell")` converged to (3.00, 5.00)).

## Pitfalls
- Physical metadata (spacing, origin, direction) matters in medical images: register in physical
  space, not voxel indices.
- Large background regions dominate the joint histogram: use masks
  (`SetMetricFixedMask`).
- If the metric changes with the overlap region, also try `SetMetricAsJointHistogramMutualInformation` (available alongside the Mattes metric in SimpleITK).

## Validate
Target registration error on manually placed landmarks; checkerboard overlay of fixed and
resampled moving image for visual QA.

## Checked
SimpleITK 2.5.6, OpenCV 5.0.0, SciPy 1.18.1, scikit-image 0.26.0.
- Run: the registration block (valid API, see the added bullet for convergence), the ECC failure, the `np.histogram2d` MI search and Powell optimisation; listed `ImageRegistrationMethod` metric setters.
- Not confirmed: the CT/MR file example (no medical data here) and ELASTIX/ANTs mention are only named.

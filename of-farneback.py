import time
import sys
import nibabel as nib
import numpy as np
from farneback3d import Farneback

"""
Parameters are based on the default parameters from
https://github.com/theHamsta/farneback3d/blob/f669d612621a9a52d2c2fb7cc90cac3fe99a1199/README.rst
and adjusted for MRI by manual testing.
Exaplanation of parameters:
https://www.geeksforgeeks.org/opencv-the-gunnar-farneback-optical-flow/
"""

script_start_time = time.time()

ref_img = nib.load(sys.argv[1])
ref_d = ref_img.get_fdata().astype(np.float32)
warp_d = nib.load(sys.argv[2]).get_fdata().astype(np.float32)

f = Farneback(
              pyr_scale=0.8,         # Scaling between multi-scale pyramid levels
              levels=6,              # Number of multi-scale levels
              num_iterations=5,      # Iterations on each multi-scale level
              winsize=7,             # Window size for Gaussian filtering of polynomial coefficients (default 9)
              poly_n=5,              # Size of window for weighted least-square estimation of polynomial coefficients (default 5)
              poly_sigma=0.5,        # Sigma for Gaussian weighting of least-square estimation of polynomial coefficients (default 1.2)
              )
flow_d = f.calc_flow(ref_d, warp_d)

# x, y, z, c component form
flow_d = np.transpose(flow_d, (3, 2, 1, 0))

# Invert flow in z axis
flow_d[...,-1] *= -1

flow_img = nib.spatialimages.SpatialImage(flow_d, affine=ref_img.affine, header=ref_img.header)

nib.save(flow_img, sys.argv[3])

print("Script execution time: %i s" % np.int(time.time()-script_start_time))
print(sys.argv[0] + " done")

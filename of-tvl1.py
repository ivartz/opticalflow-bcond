import time
import sys
import nibabel as nib
from skimage.registration import optical_flow_tvl1
import numpy as np

script_start_time = time.time()

ref_img = nib.load(sys.argv[1])
ref_d = ref_img.get_fdata()
warp_d = nib.load(sys.argv[2]).get_fdata()

# Common normalization to between 0 and 1, assuming no negative values
m = np.max([ref_d.max(), warp_d.max()])
ref_d /= m
warp_d /= m

flow_d = optical_flow_tvl1(ref_d, warp_d)

# x, y, z, c component form
flow_d = np.transpose(flow_d, (1, 2, 3, 0))

# Invert flow in z axis
flow_d[...,-1] *= -1

flow_img = nib.spatialimages.SpatialImage(flow_d, affine=ref_img.affine, header=ref_img.header)

nib.save(flow_img, sys.argv[3])

print("Script execution time: %i s" % np.int(time.time()-script_start_time))
print(sys.argv[0] + " done")

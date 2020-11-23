import sys
import nibabel as nib
import numpy as np

seg = nib.load(sys.argv[1]).get_fdata()
data = nib.load(sys.argv[2]).get_fdata()

for i in range(np.int(np.max(seg))):
    v = i+1
    d = data[seg == v]
    if d.size == 0:
        print("nan")
    else:
        print(np.median(d[d.nonzero()]).astype(np.float32))

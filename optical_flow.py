#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Optical flow for motion estimation in cancer simulation.

"""

import numpy as np
import cv2
import nibabel as nib
import matplotlib.pyplot as plt
from skimage.registration import optical_flow_tvl1, optical_flow_ilk
import os
from skimage.transform import warp


def plot_flow(image, flow, slice_num, step=4, p=None, use_skimage=True, save_file=True):
    """Plot the 2D optical flow.

    Parameters
    ----------
    image : 2D array
        The reference grayscale 2D image.
    flow : 3D array
        The estimate flow in each axis.
    i : int
        Slice number of the volume.
    step : int
        Step size for downsampling the flow along each axis.
    p : None or int
        Percentile to select only more significant motion.
    use_skimage : bool
        Use optical flow algorithms in skimage. The format of returned flow differs between skimage and opencv.
    save_file : bool
        True to save to motion/ folder, False to plot the result.

    Returns
    -------

    """
    # img0 = np.rot90(ref_img[:, :, i], k=-2)
    # img1 = np.rot90(warped_img[:, :, i], k=-2)

    v, u = (flow[0], flow[1]) if use_skimage else (flow[:, :, 1], flow[:, :, 0])
    # u, v = flow[...,0], flow[...,1]  # opencv
    # v, u = flow[0], flow[1]  # skimage
    norm = np.sqrt(v ** 2 + u ** 2)

    # Select more significant motion/displacements
    if p:
        thresh = np.percentile(norm, p)
        mask = norm > thresh
        v *= mask
        u *= mask
        norm *= mask
    # fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(10, 7))  # plot reference and magnitude (and direction)
    fig, ax0 = plt.subplots(1, 1, figsize=(10, 7))  # plot only reference and direction
    ax0.imshow(image, cmap='gray')
    ax0.set_title("Reference image, step=%d, slice %d" % (step, slice_num))
    ax0.set_axis_off()

    nl, nc = image.shape
    y, x = np.mgrid[:nl:step, :nc:step]  # plot flow every step-th pixel
    u_, v_ = u[::step, ::step], v[::step, ::step]
    # ax1.imshow(norm, cmap='gray')
    ax0.quiver(x, y, u_, v_, color='r', scale=1,
               angles='xy', scale_units='xy', lw=3)
    # ax1.set_title("Estimated flow (subsampling every %d pixels)" % step)
    # ax1.set_axis_off()
    fig.tight_layout()

    # print("Slice ", slice_num)
    if save_file:
        dir_to_save = "motion/"
        if not os.path.exists(dir_to_save):
            os.mkdir(dir_to_save)
        plt.savefig(dir_to_save+"%d.png" % slice_num)
    else:
        plt.show()


def estimate_3d_motion_from_2d(reference_image, warped_image, slice_range=None, save_file=True):
    """Estimate the 3D motion/displacements between two registered 3D volume by
    applying optical flow for each pair of slices.

    Parameters
    ----------
    reference_image : 3D array
        Reference image
    warped_image : 3D array
        Warped image.
    slice_range : None or list
        Range of slices for motion estimation.
    save_file : bool
        True to save to motion/ folder, False to plot the result.

    Returns
    -------
    flow : 4D array
        The estimated 2D optical flow for each axis.

    """
    # For using 2D iterative LK algorithm in skimage, the input needs to be grayscale
    # reference_image = reference_image.astype(np.float64)
    # warped_image = warped_image.astype(np.float64)
    # reference_image /= reference_image.max()
    # warped_image /= warped_image.max()

    image_shape = reference_image.shape
    if not slice_range:  # if not defined, use all slices
        slice_range = range(image_shape[0])

    all_flow = np.zeros((image_shape[2], 2, *(image_shape[:2])))  # store each 2D flow
    for i in slice_range:
        print(i)
        image0, image1 = reference_image[:, :, i], warped_image[:, :, i]
        all_flow[i] = optical_flow_ilk(image0, image1, radius=5)
        nr, nc = image0.shape
        row_coords, col_coords = np.meshgrid(np.arange(nr), np.arange(nc), indexing='ij')
        estimated_warp = warp(image1, np.array([row_coords+all_flow[i][0], col_coords+all_flow[i][1]]), mode='nearest')
        plt.imshow(estimated_warp, cmap='jet')
        plt.show()
        plot_flow(image0, all_flow[i], i, save_file=save_file)

    return all_flow


def estimate_3d_motion(reference_image, warped_image, save_file=False, reference_image_orgin=None):
    """Directly estimate the 3D motion between two 3D volumes using optical flow.

    Parameters
    ----------
    reference_image : 3D array
        Reference image.
    warped_image : 3D array
        Warped image.
    save_file : bool
        Save the 3D flow to file
    reference_image_orgin : nifti object
        Provide the header information used when saving nifti files.

    Returns
    -------
    flow : 4D array
        The estimated 3D optical flow for each axis.

    """
    # w, v, u = optical_flow_tvl1(ref_img, warped_img)
    flow = optical_flow_ilk(reference_image, warped_image, radius=7)  # radius can be tuned

    if save_file:
        try:  # check if nifti object provided correctly
            flow_image = nib.spatialimages.SpatialImage(np.transpose(flow, (1, 2, 3, 0)),  # displacements as last axis
                                                        affine=reference_image_origin.affine,
                                                        header=reference_image_origin.header)
        except:
            print("Original nifti object not provided or with wrong format!")
            return
        nib.save(flow_image, "3d_flow.nii.gz")

    return flow


def estimate_2d_motion(ref, warped, slice_num, nvec=20, save_file=True):
    """ NOT USED!!!
    Estimate the 2D motion using optical flow.

    """
    # v, u = optical_flow_ilk(ref, warped, radius=4)
    v, u = optical_flow_tvl1(ref, warped)

    plot_flow(ref, np.stack((v, u), axis=-1))
    # # flow = cv2.calcOpticalFlowFarneback(ref, warped, None, 0.8,15,5,10,5,0,10)
    # # v, u = flow[:,:,0], flow[:,:,1]


def optical_flow_opencv(ref, warped):
    """  NOT USED!!
    2D optical flow using opencv.
    
    """
    ref = ref.astype(np.uint8) #np.uint16)
    warped = warped.astype(np.uint8) #np.uint16)

    flow = cv2.calcOpticalFlowFarneback(ref, warped, None, 0.5, 3, 7, 3, 5, 1.2, 0)
    # flow = optical_flow_ilk(ref, warped, radius=7)
    # flow = optical_flow_tvl1(ref, warped, num_warp=10)

    return flow


if __name__ == "__main__":
    reference_image_origin = nib.load("T1c.nii.gz")  # nib.load("2-T1c.nii.gz")
    reference_image = nib.load("T1c.nii.gz").get_fdata().astype(np.float64)  # convert data type when needed
    # warped_image = nib.load("3-T1c.nii.gz").get_fdata().astype(np.float64)
    warped_image = nib.load("warped.nii.gz").get_fdata().astype(np.float64)  # convert data type when needed
    # truth = nib.load("interp-field-8.0mm.nii.gz").get_fdata().astype(np.float64)

    print("Reference image: ", reference_image.shape)

    # Normalization
    reference_image /= reference_image.max()
    warped_image /= warped_image.max()

    # slice_range = range(40, 72) # range(60, 80)
    # slice_range = range(30, 90)
    # slice_range = range(115, 116)
    slice_range = range(70, 71)

    # Calculate all 2D flow and plot/save it
    all_flow = estimate_3d_motion_from_2d(reference_image, warped_image, slice_range=slice_range, save_file=False)
    print("All 2D flow: (%f, %f)" %(all_flow.min(), all_flow.max()))

    # Calculate 3D flow and save it
    # flow_3d = optical_flow_ilk(reference_image, warped_image, radius=7)  # radius can be tuned
    # print("3D flow: (%f, %f)" %(flow_3d.min(), flow_3d.max()))
    # flow_img = nib.spatialimages.SpatialImage(np.transpose(flow_3d, (1,2,3,0)),  # displacements as last axis
    #                                           affine=reference_image_origin.affine, header=reference_image_origin.header)
    # nib.save(flow_img, "3d_flow.nii.gz")

    # Test motion for coronal (x-z) plane
    # for i in slice_range:
    #     ref = reference_image[:, :, i]  # axial: x-y plane
    #     warped = warped_image[:, :, i]
    #     # ref = ref_img[:, i, :]  # coronal: x-z plane
    #     # warped = warped_img[:, i, :]
    #
    #     flow = optical_flow_opencv(ref, warped)  # calculate optical flow using opencv
    #     print("Flow: ", flow.min(), flow.max())
    #     print("Range of displacements: ", flow.min(), flow.max())
    #     plot_flow(ref, flow, i, save_file=False)

    print("Finished")



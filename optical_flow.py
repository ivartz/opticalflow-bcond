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


def plot_flow(image, flow, slice_num, step=4, save_file=True):
    """Plot the 2D optical flow.

    """
    # u, v = flow[...,0], flow[...,1]
    v, u = flow[0], flow[1]
    norm = np.sqrt(v ** 2 + u ** 2)

    p = np.percentile(norm, 90)
    mask = norm > p
    v *= mask
    u *= mask
    norm *= mask
    # fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(10, 7))
    fig, ax0 = plt.subplots(1, 1, figsize=(10, 7))
    ax0.imshow(image, cmap='gray')
    ax0.set_title("Reference image, step=%d, slice %d" % (step, i))
    ax0.set_axis_off()

    nl, nc = image.shape
    y, x = np.mgrid[:nl:step, :nc:step]
    u_, v_ = u[::step, ::step], v[::step, ::step]
    # ax1.imshow(norm, cmap='gray')
    ax0.quiver(x, y, u_, v_, color='r', scale=1,
               angles='xy', scale_units='xy', lw=3)
    # ax1.set_title("Estimated flow (subsampling every %d pixels)" % step)
    # ax1.set_axis_off()
    fig.tight_layout()

    print("Slice ", i)
    if save_file:
        dir_to_save = "motion/"
        if not os.path.exists(dir_to_save):
            os.mkdir(dir_to_save)
        plt.savefig(dir_to_save+"%d.png" % slice_num)
    else:
        plt.show()


def estimate_2d_motion(ref, warped, slice_num, nvec=20, save_file=True):
    """Estimate the 2D motion using optical flow.
    """
    # v, u = optical_flow_ilk(ref, warped, radius=4)
    # v, u = optical_flow_tvl1(ref, warped)

    plot_flow(ref, np.stack((v, u), axis=-1))
    # # flow = cv2.calcOpticalFlowFarneback(ref, warped, None, 0.8,15,5,10,5,0,10)
    # # v, u = flow[:,:,0], flow[:,:,1]
    #
    # norm = np.sqrt(u ** 2 + v ** 2)
    # # p = np.percentile(norm, 50)
    # # mask = norm > p
    # # u *= mask
    # # v *= mask
    # # norm /= norm.max()
    # # u /= norm.max()
    # # v /= norm.max()
    # # norm = np.sqrt(u ** 2 + v ** 2)
    # print(norm.max(), norm.min())
    # fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(10, 7))
    # # fig, ax0 = plt.subplots(1, 1, figsize=(10, 7))
    # ax0.imshow(ref, cmap='gray')
    # # ax0.imshow(warped, cmap='jet', alpha=0.1)
    # # ax0.set_title("2-T1c, slice %d" %(slice_num))
    # ax0.set_title("reference, slice %d" %(slice_num))
    # ax0.set_axis_off()
    #
    # nl, nc = ref.shape
    # step = max(nl//nvec, nc//nvec)
    #
    # # y, x = np.mgrid[:nl:1, :nc:1]
    # # res = warp(warped, np.array([y+v, x+u]), mode='nearest')
    # # ax1.imshow(res, cmap='gray')
    # y, x = np.mgrid[:nl:step, :nc:step]
    # u_ = u[::step, ::step]
    # v_ = v[::step, ::step]
    #
    # ax1.imshow(warped, cmap='gray')
    # # ax1.imshow(norm, cmap='gray')
    # # print(x.min(),x.max(),u_.min(),v_.max())
    # # ax1.quiver(x, y, u_, v_, color='r',
    #        # angles='xy', scale_units='xy', lw=3)
    # # ax1.set_title("Optical flow magnitude and vector field")
    # ax1.set_title("Estimated optical flow")
    # ax1.set_axis_off()
    # fig.tight_layout()
    #
    # if save_file:  # save plot to disk
    #     dir_to_save = "motion/"
    #     if not os.path.exists(dir_to_save):
    #         os.mkdir(dir_to_save)
    #     plt.savefig(dir_to_save+"%d.png" %slice_num)
    # else:  # plot
    #     plt.show()

    return np.stack((u, v), axis=0)


def estimate_3d_motion_from_2d(ref_img, warped_img, slice_range=None, save_file=True):
    """Estimate the motino between two 3D volumes.
    Approach 1: Since images are registered, 3D motion can be computed by
                performing 2D optical flow for each pair of slices.
    Approach 2: Directly compute 3D optifcal flow.

    """
    if not slice_range:  # for all slices
        slice_range = range(ref_img.shape[0])

    num_vecs = max(ref_img.shape[0], ref_img.shape[1]) // 4
    all_flow = np.zeros((ref_img.shape[2], 2, *(ref_img.shape[:2])))  # store each 2D flow
    for i in slice_range:
        print(i)
        img0, img1 = ref_img[:, :, i], warped_img[:, :, i]
        # img0 = np.rot90(ref_img[:, :, i], k=-2)
        # img1 = np.rot90(warped_img[:, :, i], k=-2)
        flow = estimate_2d_motion(img0, img1, i, num_vecs, save_file=save_file)
        all_flow[i] = flow

    return all_flow


def estimate_3d_motion(ref_img, warped_img, save_file=False):
    """Estimate the motino between two 3D volumes.
    Approach 1: Since images are registered, 3D motion can be computed by
                performing 2D optical flow for each pair of slices.
    Approach 2: Directly compute 3D optifcal flow.

    """
    w, v, u = optical_flow_tvl1(ref_img, warped_img)
    
    return w, v, u


def optical_flow_opencv(ref, warped):
    """2D optical flow using opencv.
    
    """
    ref = ref.astype(np.uint16)
    warped = warped.astype(np.int16)

    # flow = cv2.calcOpticalFlowFarneback(ref, warped, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    flow = optical_flow_ilk(ref, warped, radius=5)

    return flow


if __name__ == "__main__":
    n = 70
    ref_img_org = nib.load("T1c.nii.gz")  # nib.load("2-T1c.nii.gz")
    ref_img = nib.load("T1c.nii.gz").get_fdata().astype(np.int32)  # "2-T1c.nii.gz"
    # warped_img = nib.load("3-T1c.nii.gz").get_fdata().astype(np.uint8)
    warped_img = nib.load("warped.nii.gz").get_fdata().astype(np.int32)
    # truth = nib.load("interp-field-8.0mm.nii.gz").get_fdata().astype(np.uint8) #.transpose([2,1,0,3])
    print("Reference image: ", ref_img.shape)

    # ref_img /= ref_img.max()
    # warped_img /= warped_img.max()

    slice_range = range(40, 72) # range(60, 80)# ref_img.shape[0])
    # slice_range = range(30, 90)
    # slice_range = range(115, 116)
    # slice_range = range(70, 71)

    # all_flow = estimate_3d_motion_from_2d(ref_img, warped_img, slice_range=slice_range, save_file=True)

    # flow_3d = estimate_3d_motion(ref_img, warped_img)
    # flow_img = nib.spatialimages.SpatialImage(np.transpose(flow_3d, (1,2,3,0)),
    #                                           affine=ref_img_org.affine, header=ref_img_org.header)
    # nib.save(flow_img, "3d_flow.nii.gz")

    for i in slice_range:
        ref = ref_img[:, :, i]
        warped = warped_img[:, :, i]
        # ref = ref_img[:, i, :]  # coronal
        # warped = warped_img[:, i, :]  # coronal

        flow = optical_flow_opencv(ref, warped)
        print("Flow: ", flow.min(), flow.max())
        print("Range of displacements: ", flow.min(), flow.max())
        plot_flow(ref, flow, slice_num=i, save_file=False)

    print("Finished")


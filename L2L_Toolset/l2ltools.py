import os
import sys
__file__ = 'l2ltools.py'
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import open3d as o3d
import tensorflow as tf
import numpy as np
import cv2
import json
import numpy as np
from matplotlib import pyplot as plt
from tf_bodypix.api import download_model, load_model, BodyPixModelPaths
import matplotlib.patches as mpatches
from initialize_config import initialize_config
# import args


def get_capture_frame(infile, frame_number):
    video = cv2.VideoCapture(infile)
    video.set(cv2.CAP_PROP_POS_AVI_RATIO,1) # set to end
    

    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count/fps
    frame_timing = duration / frame_count

    reader = o3d.io.AzureKinectMKVReader()
    reader.open(infile)
    meta = reader.get_metadata()
    print(meta.stream_length_usec)
    skip_time = (frame_number - 1) * (frame_timing * 1000000)
    reader.seek_timestamp(int((frame_number -1) * (frame_timing * 1000000)))
    capture = reader.next_frame()

    video.release()
    reader.close()
    return capture

def write_config(infile, outpath):
    reader = o3d.io.AzureKinectMKVReader()
    reader.open(infile)
    if not reader.is_opened():
        raise RuntimeError(f"Unable to open file {args.input}")
    if outpath is not None:
        abspath = os.path.abspath(outpath)
    
    # metadata is the intrinsic, minus the intrinsic matrix
    metadata = reader.get_metadata()
    o3d.io.write_azure_kinect_mkv_metadata(f'{abspath}/intrinsic.json', metadata)
    config = {
        'path_dataset': abspath,
        'path_intrinsic': f'{abspath}/intrinsic.json'
    }
    initialize_config(config)
    config['max_depth'] = 0.5
    with open(f'{abspath}/config.json', 'w') as f:
        json.dump(config, f, indent=4)

def get_intrinsic(outpath):
    '''
    get_intrinsic(outpath):

    retrieves intrinsic file info from infile for setting 
    Open3D.camera.PinholeCameraIntrinsic values later
    '''
    if outpath is not None:
        abspath = os.path.abspath(outpath)
    # with open(f'{abspath}/intrinsic.json') as infile:
    #     intrinsic_data = json.load(infile)
    # return intrinsic_data
    intrinsic = o3d.io.read_pinhole_camera_intrinsic(f'{abspath}/intrinsic.json')
    return intrinsic

def get_masked_pcloud(color_image, depth_image, intrinsic, model, rotate=False):

    col_rgb = np.asarray(color_image)
    depth = np.asarray(depth_image)

    if rotate:
        col_rot = cv2.rotate(col_rgb, cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        col_rot = col_rgb

    # run bodypix model on rotated frame
    result = model.predict_single(col_rot)
    mask = result.get_mask(threshold=0.1).numpy().astype(np.uint8)
    col_masked = cv2.bitwise_and(col_rot, col_rot, mask=mask)
    part_mask = result.get_colored_part_mask(mask)

    # rotate back to original dimensions
    if rotate:
        mask_ogd = cv2.rotate(mask, cv2.ROTATE_90_CLOCKWISE)
        col_masked_ogd = cv2.rotate(col_masked, cv2.ROTATE_90_CLOCKWISE)
        part_mask_ogd = cv2.rotate(part_mask, cv2.ROTATE_90_CLOCKWISE).astype(np.uint8)
    else:
        mask_ogd = mask
        col_masked_ogd = col_masked
        part_mask_ogd = part_mask.astype(np.uint8)

    # debuging print statements to get dtype right
    #print('part_mask_ogd',part_mask_ogd.dtype, part_mask_ogd.shape)
    #print('mask_ogd',mask_ogd.dtype, mask_ogd.shape)
    #print('col_mask_ogd',col_masked_ogd.dtype, col_masked_ogd.shape)

    # mask depth image
    dep_masked = cv2.bitwise_and(depth, depth, mask=mask_ogd).astype(np.uint16)

    #print('dep_masked', dep_masked.dtype, dep_masked.shape)

    # load masked images in open3d format
    o3d_colm = o3d.geometry.Image(col_masked_ogd)
    o3d_part = o3d.geometry.Image(part_mask_ogd)
    o3d_depm = o3d.geometry.Image(dep_masked)

    #print('o3d_colm', o3d_im_prop(o3d_colm))
    #print('o3d_part', o3d_im_prop(o3d_part))
    #print('o3d_depm',o3d_im_prop(o3d_depm))

    # obtain RGBD image
    # convert_rgb_to_intensity=False keeps color
    masked_rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(o3d_colm, o3d_depm, convert_rgb_to_intensity=False)
    parts_rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(o3d_part, o3d_depm, convert_rgb_to_intensity=False)
    
    # obtain point clouds
    masked_pcd = o3d.geometry.PointCloud.create_from_rgbd_image(masked_rgbd, intrinsic)
    parts_pcd = o3d.geometry.PointCloud.create_from_rgbd_image(parts_rgbd, intrinsic)

    # keep in correct orientation
    masked_pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
    parts_pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])

    return masked_pcd, parts_pcd

def run_rot_bodypix(color_file, depth_file, intrinsic, model):

    color = cv2.imread(color_file,-1)
    col_rgb = cv2.cvtColor(color, cv2.COLOR_BGR2RGB) 
    depth = cv2.imread(depth_file,-1)

    col_rot = cv2.rotate(col_rgb, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # run bodypix model on rotated frame
    result = model.predict_single(col_rot)
    mask = result.get_mask(threshold=0.1).numpy().astype(np.uint8)
    col_masked = cv2.bitwise_and(col_rot, col_rot, mask=mask)
    part_mask = result.get_colored_part_mask(mask)

    # rotate back to original dimensions
    mask_ogd = cv2.rotate(mask, cv2.ROTATE_90_CLOCKWISE)
    col_masked_ogd = cv2.rotate(col_masked, cv2.ROTATE_90_CLOCKWISE)
    part_mask_ogd = cv2.rotate(part_mask, cv2.ROTATE_90_CLOCKWISE).astype(np.uint8)

    # debuging print statements to get dtype right
    #print('part_mask_ogd',part_mask_ogd.dtype, part_mask_ogd.shape)
    #print('mask_ogd',mask_ogd.dtype, mask_ogd.shape)
    #print('col_mask_ogd',col_masked_ogd.dtype, col_masked_ogd.shape)

    # mask depth image
    dep_masked = cv2.bitwise_and(depth, depth, mask=mask_ogd).astype(np.uint16)

    #print('dep_masked', dep_masked.dtype, dep_masked.shape)

    # load masked images in open3d format
    o3d_colm = o3d.geometry.Image(col_masked_ogd)
    o3d_part = o3d.geometry.Image(part_mask_ogd)
    o3d_depm = o3d.geometry.Image(dep_masked)

    #print('o3d_colm', o3d_im_prop(o3d_colm))
    #print('o3d_part', o3d_im_prop(o3d_part))
    #print('o3d_depm',o3d_im_prop(o3d_depm))

    # obtain RGBD image
    # convert_rgb_to_intensity=False keeps color
    masked_rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(o3d_colm, o3d_depm, convert_rgb_to_intensity=False)
    parts_rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(o3d_part, o3d_depm, convert_rgb_to_intensity=False)
    
    # obtain point clouds
    masked_pcd = o3d.geometry.PointCloud.create_from_rgbd_image(masked_rgbd, intrinsic)
    parts_pcd = o3d.geometry.PointCloud.create_from_rgbd_image(parts_rgbd, intrinsic)

    # keep in correct orientation
    masked_pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
    parts_pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])

    return masked_pcd, parts_pcd
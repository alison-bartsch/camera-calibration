# import pyrealsense2 as rs
import numpy as np
# import cv2
import time
import os
# import argparse
from os.path import join
# import threading
from frankapy import FrankaArm
# from autolab_core import RigidTransform

# bash ./bash_scripts/start_control_pc.sh -i localhost
# python frankapy/scripts/basic_functions/reset_arm.py
# python frankapy/vision_module/2D_vision/scripts/collect_shaking_vid.py

# ------------------------------------------------------------------- parameters
# {HOME} = frankapy
# save_dir = "./oscil_videos"
# os.makedirs (save_dir, exist_ok=True)


# # (record when robot stopped, sleep otherwise)
# reset_duration = 5+3
# gopose_duration = 1
# sleep_duration = reset_duration + gopose_duration + 1.80


def shake_bottle (fa, rec_duration=11):
    # init_trans = np.load("./init_trans.npy")
    # init_rot = np.load("./init_rot.npy")
    translation = np.load ("../shake_trans2.npy")
    rotation = np.load ("../shake_rot2.npy")

    saved_pose = fa.get_pose ()
    print (saved_pose)

    saved_pose.rotation = rotation
    saved_pose.translation = translation
    
    # To saved position
    print ("1 To saved shake position")
    fa.goto_pose(saved_pose)
    time.sleep (60)
    
    print ("2 Shake movement")
    saved_pose.translation += np.array ([0.15, 0.0, 0.0]) # 20cm in X direction
    fa.goto_pose (saved_pose, duration=0.8) # in 0.8 - 1.0 s
    
    print ("3 Recording")
    time.sleep(rec_duration) # record
    
    # reset positions
    print ("4 Reset robot")
    fa.reset_pose()
    fa.reset_joints()
    pose = fa.get_pose()
    print (pose)

    # fa.reset_pose ()
    # pose = fa.get_pose()
    # print (pose)

    return None


grip_force = 160
num_videos = 1

if __name__ == "__main__":
    print ("Initializing FrankaArm")
    st = time.time()
    fa = FrankaArm()
    print (f"Took {(time.time()-st):1.2f} s")

    # fa.reset_pose(ignore_errors=False)
    
    # open in the beginning
    # if open:
    # print ("Opening gripper")
    # fa.open_gripper()
    # time_to_give_bottle = 5 # s
    # time.sleep (time_to_give_bottle)

    # # close gripper around bottle
    # print (f"Closing gripper (F = {grip_force} N)")
    # fa.goto_gripper(width=0.005, force=grip_force, grasp=True) # speed=0.04 m/s default, 0.025m/0.04m/s = 0.625s # 0.008, force=grip_force, 
    # time.sleep(3)
    
    # After closing the gripper (robot holding bottle)
    # robot shakes for 'num_videos' times
    for i in range (num_videos):
        print (f"Video {i}")
        shake_bottle(fa)
        time.sleep(2)
    

# Questions:
# Is there some kind of boundary for 'quaternion'? Resetting seems to work differently depending on quaternion.








import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.transform import Rotation as R


def average_transform(all_T_base_to_tag):
    sum_translation = np.zeros(3)
    eulers = []

    translations_list = [[] for _ in range(3)]  
    eulers_list = [[] for _ in range(3)] 

    for transform in all_T_base_to_tag:
        translation = transform[:3, 3]
        sum_translation += translation

        for i in range(3):
            translations_list[i].append(translation[i])

        rotation_matrix = transform[:3, :3]
        euler = R.from_matrix(rotation_matrix).as_euler('ZYX')
        eulers.append(euler)

        for i in range(3):
            eulers_list[i].append(euler[i])

    mean_translation = sum_translation / len(all_T_base_to_tag)
    mean_euler = np.mean(eulers, axis=0)

    mean_rotation_matrix = R.from_euler('ZYX', mean_euler).as_matrix()

    mean_transform = np.eye(4)
    mean_transform[:3, :3] = mean_rotation_matrix
    mean_transform[:3, 3] = mean_translation

    return mean_transform

def transformation_error(ref_transform,all_T_base_to_tag):
    mean_transform_inv = np.linalg.inv(ref_transform)

    translation_errors = []
    rotation_errors = []

    translation_errors_list = [[] for _ in range(3)]  
    rotation_errors_list = [[] for _ in range(3)]  

    for transform in all_T_base_to_tag:
        deviation = mean_transform_inv @ transform
        
        translation_error = deviation[:3, 3]
        translation_errors.append(translation_error)
        
        for i in range(3):
            translation_errors_list[i].append(translation_error[i])
        
        rotation_deviation = R.from_matrix(deviation[:3, :3])
        euler_deviation = rotation_deviation.as_euler('ZYX', degrees=True)
        rotation_errors.append(euler_deviation)
        
        for i in range(3):
            rotation_errors_list[i].append(euler_deviation[i])

    mean_translation_error = np.mean(translation_errors, axis=0)
    mean_rotation_error = np.mean(rotation_errors, axis=0)

    return mean_translation_error, mean_rotation_error

def create_homogeneous_transform(R, t):
        H=np.eye(4)
        H[0:3,0:3]= R
        H[0:3,3]=t
        return H
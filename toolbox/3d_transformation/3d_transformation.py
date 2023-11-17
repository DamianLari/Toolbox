import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.transform import Rotation as R

class transformation:
    def average_transform_3d_graph(self):
        sum_translation = np.zeros(3)
        eulers = []
        translations_list = [[] for _ in range(3)]  

        for transform in self.all_T_base_to_tag:
            translation = transform[:3, 3]
            sum_translation += translation

            for i in range(3):
                translations_list[i].append(translation[i])

            rotation_matrix = transform[:3, :3]
            euler = R.from_matrix(rotation_matrix).as_euler('ZYX')
            eulers.append(euler)

        mean_translation = sum_translation / len(self.all_T_base_to_tag)
        mean_euler = np.mean(eulers, axis=0)

        mean_rotation_matrix = R.from_euler('ZYX', mean_euler).as_matrix()

        mean_transform = np.eye(4)
        mean_transform[:3, :3] = mean_rotation_matrix
        mean_transform[:3, 3] = mean_translation
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        sc = ax.scatter(translations_list[0], translations_list[1], translations_list[2], c='b', marker='o', label='Positions')
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        ax.legend()
        sc2 = ax.scatter(mean_translation[0], mean_translation[1], mean_translation[2], c='r', marker='o', s=100, label='Mean Position')

        def update(num, sc, sc2):
            ax.view_init(elev=10., azim=num)

        ani = FuncAnimation(fig, update, frames=range(0, 360, 10), fargs=(sc, sc2), interval=50)
        ani.save('3d_scatter_rotation.mp4', writer='ffmpeg', fps=30)

   
        return mean_transform
    
    
    def average_transform_graph(self):
        sum_translation = np.zeros(3)
        eulers = []

        translations_list = [[] for _ in range(3)]  
        eulers_list = [[] for _ in range(3)] 

        for transform in self.all_T_base_to_tag:
            translation = transform[:3, 3]
            sum_translation += translation

            for i in range(3):
                translations_list[i].append(translation[i])

            rotation_matrix = transform[:3, :3]
            euler = R.from_matrix(rotation_matrix).as_euler('ZYX')
            eulers.append(euler)

            for i in range(3):
                eulers_list[i].append(euler[i])

        mean_translation = sum_translation / len(self.all_T_base_to_tag)
        mean_euler = np.mean(eulers, axis=0)

        mean_rotation_matrix = R.from_euler('ZYX', mean_euler).as_matrix()

        mean_transform = np.eye(4)
        mean_transform[:3, :3] = mean_rotation_matrix
        mean_transform[:3, 3] = mean_translation

        components = ['x', 'y', 'z']
        for i, comp in enumerate(components):
            plt.figure(figsize=(20, 5))  
            plt.plot(translations_list[i], label=f'{comp}-component')
            plt.axhline(y=mean_translation[i], color='r', linestyle='-', label=f'Mean Value:{mean_translation[i]}')
            plt.title(f'Translation in {comp.upper()}')
            plt.legend()
            plt.savefig(f'average_transform_t{comp}.png')

        
        for i, comp in enumerate(components):
            plt.figure(figsize=(20, 5))  
            plt.plot([np.degrees(angle) for angle in eulers_list[i]], label=f'{comp}-component')
            plt.axhline(y=np.degrees(mean_euler[i]), color='r', linestyle='-', label=f'Mean Value:{mean_euler[i]}')
            plt.title(f'Rotation about {comp.upper()}')
            plt.legend()
            plt.savefig(f'average_transform_r{comp}.png')

        return mean_transform
    
    def transformation_error_graph(self, ref_transform,type_graph):
        mean_transform_inv = np.linalg.inv(ref_transform)

        translation_errors = []
        rotation_errors = []

        translation_errors_list = [[] for _ in range(3)]  
        rotation_errors_list = [[] for _ in range(3)]  

        for transform in self.all_T_base_to_tag:
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
        
        components = ['x', 'y', 'z']
        for i, comp in enumerate(components):
            plt.figure(figsize=(20, 5))  
            plt.plot(translation_errors_list[i], label=f'Error in {comp}-component')
            plt.axhline(y=mean_translation_error[i], color='r', linestyle='-', label=f'Mean Error : {mean_translation_error[i]}')
            plt.title(f'Translation Error in {comp.upper()}')
            plt.legend()
            plt.savefig(f'{type_graph}_translation_error_{comp}.png')

        for i, comp in enumerate(components):
            plt.figure(figsize=(20, 5))  
            plt.plot(rotation_errors_list[i], label=f'Error in rotation about {comp}-axis')
            plt.axhline(y=mean_rotation_error[i], color='r', linestyle='-', label=f'Mean Error : {mean_rotation_error[i]}')
            plt.title(f'Rotation Error about {comp.upper()}')
            plt.legend()
            plt.savefig(f'{type_graph}_rotation_error_{comp}.png')

        return mean_translation_error, mean_rotation_error

    
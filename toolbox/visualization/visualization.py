import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.transform import Rotation as R
import matplotlib
matplotlib.use('TkAgg')

class visualisation:
    def save_anime_transformation_3d_graph(self, mean_transform, translations_list):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        sc = ax.scatter(translations_list[0], translations_list[1], translations_list[2], c='b', marker='o', label='Positions')
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        ax.legend()
        sc2 = ax.scatter(mean_transform[0, 3], mean_transform[1, 3], mean_transform[2, 3], c='r', marker='o', s=100, label='Mean Position')

        def update(num, sc, sc2):
            ax.view_init(elev=10., azim=num)

        ani = FuncAnimation(fig, update, frames=range(0, 360, 10), fargs=(sc, sc2), interval=50)
        ani.save('3d_scatter_rotation.mp4', writer='ffmpeg', fps=30)
    
    
    def transformation_graph(self, translation_errors_list, mean_translation_error, rotation_errors_list, mean_rotation_error, type_graph):
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
            
    
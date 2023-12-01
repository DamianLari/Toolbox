from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

class Hoda3DGraph:
    def __init__(self):
        self.save = False
        self.show = True
        self.fileName = ''
        self.density = False
        self.x_label = 'X Label'
        self.y_label = 'Y Label'
        self.z_label = 'Z Label'
        self.default_point_settings = {
            'color': 'blue',
            'marker': 'o',
            'label': 'Position',
            'size': 10
        }
        # Initialisation avec un ensemble de paramètres par défaut
        self.point_settings = [self.default_point_settings]
        
    
    def set_parameters(self, x_label=None, y_label=None, z_label=None , save = None, show=None, fileName=None, density=None,point_settings=None):
        # Mettre à jour les paramètres si fournis
        if save is not None:
            self.save = save
        if show is not None:
            self.show = show
        if fileName is not None:
            self.fileName = fileName
        if density is not None:
            self.density = density
        if x_label is not None:
            self.x_label = x_label
        if y_label is not None:
            self.y_label = y_label
        if z_label is not None:
            self.z_label = z_label
        if point_settings is not None:
            self.point_settings = [self._complete_settings(settings) for settings in point_settings]
            
        if self.save and self.fileName == '':
            raise ValueError('fileName must be specified if save is True')
        
        
    def _complete_settings(self, settings):
        """ Complète les paramètres des points avec les valeurs par défaut si nécessaire. """
        for key, value in self.default_point_settings.items():
            settings.setdefault(key, value)
        return settings
    
        
    def _base_3d_graph(self, points_list):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        for i, point_set in enumerate(points_list):
            settings = self.point_settings[i] if i < len(self.point_settings) else self.default_point_settings
            color = settings.get('color')
            marker = settings.get('marker')
            label = settings.get('label')
            size = settings.get('size')

            if self.density:
                xyz = np.vstack([point_set[0], point_set[1], point_set[2]])
                kde = gaussian_kde(xyz)(xyz)
                sc = ax.scatter(*point_set, c=kde, cmap='viridis', marker=marker, s=size, label=label)
                cbar = fig.colorbar(sc, ax=ax)
                cbar.set_label('Densité')
            else:
                sc = ax.scatter(*point_set, c=color, marker=marker, s=size, label=label)

        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)
        ax.set_zlabel(self.z_label)
        ax.legend()

        def update(num, sc):
            ax.view_init(elev=10., azim=num)

        return FuncAnimation(fig, update, frames=range(0, 360, 10), fargs=(sc,), interval=50), fig


    def generate_graph(self, points_list):
        ani, fig = self._base_3d_graph(points_list)

        if self.show:
            plt.show()

        if self.fileName:
            ani.save(f'{self.fileName}.mp4', writer='ffmpeg', fps=30)
            
            
    def show_3d_graph(self, points_list):
        self.set_parameters(show=True, save=False)
        self.generate_graph(points_list)

    def save_3d_graph(self, points_list, fileName):
        self.set_parameters(show=False, save=True, fileName=fileName)
        self.generate_graph(points_list)

    def show_and_save_3d_graph(self, points_list, fileName):
        self.set_parameters(show=True, save=True, fileName=fileName)
        self.generate_graph(points_list)

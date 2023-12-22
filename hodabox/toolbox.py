import os
import json
import numpy as np

def get_file_path_from_grandparent_folder(self, file_name, subfolder=''):
    #================================
    # Retourne le chemin absolu du fichier spécifié, en partant du répertoire parent du répertoire parent du répertoire courant.
    # Args:
    #   file_name: Nom du fichier.
    #   subfolder: Nom du sous-dossier. Par défaut, il est vide.
    # Returns:
    #   Chemin absolu du fichier.
    #================================
    current_script_path = os.path.realpath(__file__)
    parent_directory_path = os.path.dirname(current_script_path)
    grandparent_directory_path = os.path.dirname(parent_directory_path)

    if subfolder:
        grandparent_directory_path = os.path.join(grandparent_directory_path, subfolder)

    return os.path.join(grandparent_directory_path, file_name)

def load_calib_data(calibration_file):
        #================================
        # Charge les données de calibration depuis le fichier spécifié.
        # Args:
        #   calibration_file: Chemin vers le fichier de calibration.
        # Returns:
        #   matr: Matrice de calibration.
        #   disto: Coefficients de distorsion.
        #================================
        """
        dist = np.array(camera_infos_msg.D)
        mtx = np.array([camera_infos_msg.K[0:3], camera_infos_msg.K[3:6], camera_infos_msg.K[6:9]])
        """
        try:
            with open(calibration_file) as f:
                data = json.load(f)
            matr = data["mtx"]
            disto = data["dist"]
          
        except Exception as e:
            print("Erreur lors de la lecture du fichier de calibration :", e)
        return np.array(matr) , np.array(disto)


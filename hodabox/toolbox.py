import os
import json
import numpy as np


def get_file_path(file_name, relation, subfolder=''):
    current_script_path = os.path.realpath(__file__)
    parent_directory_path = os.path.dirname(current_script_path)
    grandparent_directory_path = os.path.dirname(parent_directory_path)

    if relation == 'parent':
        target_directory_path = parent_directory_path
    elif relation == 'child':
        # Supposons que le dossier enfant est le premier répertoire dans le répertoire courant
        child_directory_path = next(os.walk('.'))[1][0]
        target_directory_path = os.path.join(parent_directory_path, child_directory_path)
    elif relation == 'cousin':
        # Supposons que le cousin est un autre dossier au même niveau que le répertoire parent
        grandparent_children = next(os.walk(grandparent_directory_path))[1]
        cousin_directory_name = [d for d in grandparent_children if d != os.path.basename(parent_directory_path)][0]
        target_directory_path = os.path.join(grandparent_directory_path, cousin_directory_name)
    elif relation == 'uncle':
        # Supposons que l'oncle est un autre dossier au même niveau que le répertoire grandparent
        great_grandparent_path = os.path.dirname(grandparent_directory_path)
        great_grandparent_children = next(os.walk(great_grandparent_path))[1]
        uncle_directory_name = [d for d in great_grandparent_children if d != os.path.basename(grandparent_directory_path)][0]
        target_directory_path = os.path.join(great_grandparent_path, uncle_directory_name)
    elif relation == 'nephew':
        # Supposons que le neveu est un dossier sous un répertoire "child"
        child_directory_path = next(os.walk('.'))[1][0]
        child_full_path = os.path.join(parent_directory_path, child_directory_path)
        nephew_directory_name = next(os.walk(child_full_path))[1][0]
        target_directory_path = os.path.join(child_full_path, nephew_directory_name)
    elif relation == 'grandparent':
        target_directory_path = grandparent_directory_path
    else:
        raise ValueError("Relation inconnue")

    if subfolder:
        target_directory_path = os.path.join(target_directory_path, subfolder)

    return os.path.join(target_directory_path, file_name)


def get_file_path_from_grandparent_folder( file_name, subfolder=''):
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


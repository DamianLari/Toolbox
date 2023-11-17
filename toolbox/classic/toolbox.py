import os

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

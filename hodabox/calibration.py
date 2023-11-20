import cv2
import numpy as np
import json
import os
import time


class CalibrationIntrinsèqueProvider:
    #==========================================
    # Cette classe permet de fournir la matrice de calibration et les coefficients de distortion
    #==========================================
    def __init__(self, colonnes, lignes):
        #================================
        # Initialisation du CalibrationProvider
        # Args:
        #   colonnes (int): le nombre de colonnes du damier
        #   lignes (int): le nombre de lignes du damier
        #================================
        
        self.cols = colonnes 
        self.rows = lignes

        self.point_image = []
        self.point_objet = []
        
        self.objp = np.zeros((self.rows * self.cols, 3), np.float32)
        self.objp[:,:2] = np.mgrid[0:self.cols, 0:self.rows].T.reshape(-1, 2) #* self.taille_case
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        print("self.objp:",type(self.objp))

    
    def get_calibration_data(self,img,pointsobj):
        #================================
        # Trouver les coins du damier dans l'image
        # Args:
        #   img (numpy.array): l'image dans laquelle chercher le damier
        #   pointsobj (list): une liste de points objets
        #
        # Returns:
        #   corners2 (numpy.array): les coins raffinés du damier détecté
        #   pointsobj (list): la liste de points objets mise à jour
        #================================
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(gray, (self.cols,self.rows), None)
        corners2 = []
        
        if ret == True:    
            pointsobj.append(self.objp)
            # Refine the corners of the detected corners
            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),self.criteria)
            return corners2, pointsobj
        else: 
            return None,pointsobj

        
   
    def get_calibration_value(self,pointsobj,imgpoints,img_size,calibration_file):
        #================================
        # Effectuer la calibration de la caméra et enregistrer les données dans un fichier.
        # Args:
        #   pointsobj (list): Une liste de points objets.
        #   imgpoints (list): Une liste de points d'image.
        #   img_size (tuple): La taille de l'image (width, height).
        #   calibration_file (str): Le chemin du fichier dans lequel enregistrer les données de calibration.
        #
        # Returns:
        #   mtx (numpy.array): La matrice de calibration de la caméra.
        #   dist (numpy.array): Les coefficients de distortion.
        #================================
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(pointsobj, imgpoints, img_size, None, None)
    
        data = {"mtx": mtx.tolist(), "dist": dist.tolist()}

        with open(calibration_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, separators=(',', ':'), sort_keys=True, indent=4)

        print("Donnée enregistrée dans:", calibration_file)

        return mtx, dist
    

    def get_grandparent_file_path(self, file_name, subfolder=''):
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
    
    
    def do_calibration(self, calibration_file, file_name):
        #cam_number = 0
        for cam_number in range(len(calibration_file)):
            self.point_image = []
            self.point_objet = [] 
            point_image = []
            file_path = self.get_grandparent_file_path(file_name[cam_number],'datasets')
            calibration_path = self.get_grandparent_file_path(calibration_file[cam_number],'calib')
            for image in os.listdir(file_path):
                camera_image = cv2.imread(os.path.join(file_path,image))
                corners, self.point_objet = self.get_calibration_data(camera_image,self.point_objet)

                if corners is not None: 
                    point_image.append(corners)

            if len(self.point_objet) > 0 and len(point_image) > 0:
                        print("================================================")
                        print("image traitées:",len(point_image))
                        print("début du calcul de mtx et dist")
                        start_time = time.time()
                        mtx, dist = self.get_calibration_value(self.point_objet,point_image,camera_image.shape[:2],calibration_path)
                        elapsed_time = time.time() - start_time
                        print("Temps de calcul :{:.2f} secondes".format(elapsed_time))
                        print("mtx:", mtx)
                        print("dist:", dist)
                        print("================================================")

            else:
                        print("Pas assez de données pour effectuer la calibration.")
            #cam_number += 1

class CalibrationHandEyeProvider:
    def __init__(self):
        pass


""" 
calib_test = CalibrationProvider(7,7)
calib_test.do_calibration(['calib_nini.json'],['calib_images'])
"""


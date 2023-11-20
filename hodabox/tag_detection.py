
import cv2
from cv2 import aruco
import numpy as np
import scipy.spatial.transform as R
import os
import apriltag
import json
from colorama import Fore, Style
import transformation as transf
class TagPoseProvider:
    def set_calibration_params(self, mtx, dist):
        #================================
        # Définit les paramètres de calibration de la caméra.
        # Args:
        #   mtx (ndarray): la matrice de calibration.
        #   dist (ndarray): les coefficients de distorsion.
        #================================
        self.mtx = mtx
        self.dist = dist
    
    def get_calibration_params(self):
        return self.mtx, self.dist

    def set_aruco_params(self,dict,size):
        self.aruco_dict = dict
        self.aruco_size = size

    
    def set_apriltag_params(self,tag_size,tag_dict):
        self.tag_size=tag_size
        options = apriltag.DetectorOptions(families=tag_dict,
                                border=1,
                                nthreads=4,
                                quad_decimate=1.0,
                                quad_blur=0.0,
                                refine_edges=True,
                                refine_decode=False,
                                refine_pose=True,
                                debug=False,
                                quad_contours=True)
        self.detector = apriltag.Detector(options)
    


    def set_tag_config(self, tag_type,tag_size, tag_dict=None):
        self.tag_type = tag_type
        if tag_type == 'aruco':
            if tag_dict is not None:
                aruco_dict = getattr(aruco, tag_dict)
                self.set_aruco_params(aruco.Dictionary(aruco_dict,10), float(tag_size))
            else:
                print('Le nom du dictionnaire ArUco n\'est pas défini')
        elif tag_type =='apriltag':
            self.set_apriltag_params(float(tag_size),tag_dict)
        else:
            print('Erreur au moment de définir les paramètres du tag')




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




    
    
    def correct_image(self,image):
        #================================
        # Corrige l'image en utilisant les paramètres de calibration
        # Args:
        #   image (ndarray): l'image à corriger
        # Returns:
        #   corrected_img (ndarray): l'image corrigée.
        #================================
    
        h, w = image.shape[:2]
        new_mtx, roi = cv2.getOptimalNewCameraMatrix(*self.get_calibration_params() , (w, h), 1, (w, h))

        # Corriger l'image en utilisant les paramètres de calibration
        corrected_img = cv2.undistort(image, *self.get_calibration_params() , None, new_mtx)
        script_dir = os.path.dirname(os.path.realpath(__file__))
        #cv2.imwrite(os.path.join(script_dir, "image__original.jpg"), image)
        #cv2.imwrite(os.path.join(script_dir, "image__corrected.jpg"), corrected_img)


        return corrected_img



    def detect_aruco_marker(self,image):
        #================================
        # Détecte les marqueurs ArUco dans l'image.
        # Args:
        #   image (ndarray): l'image à analyser.
        #   camera_matrix (ndarray): la matrice de calibration de la caméra.
        #   dist_coeffs (ndarray): les coefficients de distorsion de la caméra.
        # Returns:
        #   corners (ndarray): les coordonnées des marqueurs ArUco.
        #   ids (list): les identifiants des marqueurs ArUco.
        #   rvecs (ndarray): les vecteurs de rotation des marqueurs ArUco.
        #   tvecs (ndarray): les vecteurs de translation des marqueurs ArUco.
        #================================
        ids = None
        corners = None
        rejected = None
     
        dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
        parameters =  cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(dictionary, parameters)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        corners, ids, rejected = detector.detectMarkers(gray_image)
      
        """
        aruco_params = aruco.DetectorParameters_create()
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        corners, ids, rejected = aruco.detectMarkers(gray_image, self.aruco_dict, parameters=aruco_params)
        """
        
        ids = [id[0] for id in ids] #DD add
        if ids is not None:
            rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, self.aruco_size, *self.get_calibration_params())
   
            return corners, ids, rvecs, tvecs
        
        else:
            return None, None, None, None
    
    def detect_apriltag_marker(self, image):
        #================================
        # Détecte les marqueurs apriltag dans l'image.
        # Args:
        #   image (ndarray): l'image à analyser.
        # Returns:
        #   corners (ndarray): les coordonnées des marqueurs apriltag.
        #   ids (list): les identifiants des marqueurs apriltag.
        #   rvecs (ndarray): les vecteurs de rotation des marqueurs apriltag.
        #   tvecs (ndarray): les vecteurs de translation des marqueurs apriltag.
        #================================
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
        detection_results = self.detector.detect(gray_image)
        ids = [detection.tag_id for detection in detection_results]
        
        if ids is not None:
            for i in range(len(ids)):
                detection=detection_results[i]
                corners=detection.corners.reshape(1,4,2) 
                rvec, tvec ,_ = cv2.aruco.estimatePoseSingleMarkers(corners, self.tag_size,*self.get_calibration_params())
                return corners, ids, rvec, tvec

        return None, None, None, None
     

    def calculate_positions_in_world_frame(self, ids, rvecs, tvecs):
        #================================
        # Calcule les positions des marqueurs apriltag.
        # Args:
        #   ids (list): les identifiants des marqueurs apriltag.
        #   rvecs (ndarray): les vecteurs de rotation des marqueurs apriltag.
        #   tvecs (ndarray): les vecteurs de translation des marqueurs apriltag.
        # Returns:
        #   ids (list): les identifiants des marqueurs apriltag.
        #   rota (list): les vecteurs de rotation des marqueurs apriltag.
        #   transla (list): les vecteurs de translation des marqueurs apriltag.
        #================================
        if ids is not None:
            rotation_matrices = [cv2.Rodrigues(rvec)[0] for rvec in rvecs]
            homogeneous_matrices = []
            for i in range(len(rotation_matrices)):
                H = np.identity(4)
                H[0:3, 0:3] = rotation_matrices[i]
                H[0:3, 3] = tvecs[i].ravel()
                homogeneous_matrices.append(H)

            transformation_matrix = np.array([
                [0, 0, 1, 0],
                [-1, 0, 0, 0],
                [0, -1, 0, 0],
                [0, 0, 0, 1]
            ])

            new_homogeneous_matrices = []
            for H in homogeneous_matrices:
                new_H = transformation_matrix.dot( H)
                new_homogeneous_matrices.append(new_H)

            rota = []
            transla = []
            for H in new_homogeneous_matrices:
                euler_angles = np.flip(R.Rotation.from_matrix(H[0:3, 0:3]).as_euler('ZYX', degrees=False) )
                rota.append(euler_angles)
                """
                rot = R.Rotation.from_matrix(H[0:3, 0:3]).as_quat()
                rota.append(np.flip(rot))
                """
                transla.append(H[0:3, 3])

            return ids, rota, transla
        else:
            return None, None, None
        
        
    def calculate_positions_in_camera_frame(self, ids, rvecs, tvecs):
        if ids is not None:
            rotation_matrices = [cv2.Rodrigues(rvec)[0] for rvec in rvecs]
            rota = []
            
            for i in range (len(rotation_matrices)):
                rot = R.Rotation.from_matrix(rotation_matrices[i])
                rota.append(rot.as_quat())
            return ids, rota, tvecs[i]
        else:
            return None, None, None
        

    def detect_marker(self, image, tag_type, tag_size, tag_dict):
        #================================
        # Détecte les marqueurs (Aruco ou AprilTag) dans l'image.
        # Args:
        #   image (ndarray): l'image à analyser.
        #   marker_type (str): le type de marqueur à détecter ('aruco' ou 'apriltag').
        # Returns:
        #   corners (ndarray): les coordonnées des marqueurs.
        #   ids (list): les identifiants des marqueurs.
        #   rvecs (ndarray): les vecteurs de rotation des marqueurs.
        #   tvecs (ndarray): les vecteurs de translation des marqueurs.
        #================================
        
        if tag_type == 'aruco':
            return self.detect_aruco_marker(image)
        elif tag_type == 'apriltag':
            self.set_apriltag_params(tag_size,tag_dict)
            return self.detect_apriltag_marker(image)
        else:
            print('Erreur: le type de marqueur doit être "aruco" ou "apriltag".')
            return None, None, None, None

class TagConfig:
    def __init__(self, tag_type, tag_size, tag_dict,tag_id = None, tag_rvec = None ,tag_tvec= None):
        self.tag_type = tag_type
        self.tag_size = tag_size
        self.tag_dict = tag_dict
        self.tag_id = tag_id
        self.tag_rvec = tag_rvec
        self.tag_tvec = tag_tvec
        #print(Fore.BLUE+ "Initialisation d'un marqueur : " + str(self.tag_type) + " " + str(self.tag_size) + " " + str(self.tag_dict)+ Style.RESET_ALL)
    
    #///////////////////////////////////////////////

    def set_tag_params(self, tag_type, tag_size, tag_dict):
        #================================
        # Définit la taille des marqueurs .
        # Args:
        #   tag_type (str): le type de marqueur .
        #   tag_size (float): la taille des marqueurs .
        #   tag_dict (str): le dictionnaire des marqueurs .
        #================================
        self.tag_type = tag_type
        self.tag_size = tag_size
        self.tag_dict = tag_dict
        

    def get_tag_params(self):
        return self.tag_type, self.tag_size, self.tag_dict

    #///////////////////////////////////////////////

    def set_tag_id(self, tag_id):
        self.tag_id = tag_id

    def get_tag_id(self):
        return self.tag_id
    
    #///////////////////////////////////////////////

    def set_tag_rvec(self, tag_rvec):
        self.tag_rvec = tag_rvec
    
    def get_tag_rvec(self):
        return self.tag_rvec
    
    
    def set_tag_tvec(self, tag_tvec):
        self.tag_tvec = tag_tvec

    def get_tag_tvec(self):
        return self.tag_tvec
    
    #///////////////////////////////////////////////

class CameraConfig:
    def __init__(self, name,image_folder,mtx, dist):
        self.name = name
        self.image_folder = image_folder
        self.mtx = mtx
        self.dist = dist
        #print(Fore.BLUE+ "Initialisation de la caméra : ",name , Style.RESET_ALL)

    #///////////////////////////////////////////////

    def set_name(self, name):
        #================================
        # Définit le nom de la caméra.
        # Args:
        #   name (str): le nom de la caméra.
        #================================
        self.name = name
    
    def get_name(self):
        return self.name
    
    #///////////////////////////////////////////////

    def set_image_folder(self, image_folder):
        #================================
        # Définit le dossier contenant les images de la caméra.
        # Args:
        #   image_folder (str): le dossier contenant les images de la caméra.
        #================================
        self.image_folder = image_folder

    def get_image_folder(self):
        return self.image_folder
    
    #///////////////////////////////////////////////

    def set_calibration_params(self, mtx, dist):
        #================================
        # Définit les paramètres de calibration de la caméra.
        # Args:
        #   mtx (ndarray): la matrice de calibration.
        #   dist (ndarray): les coefficients de distorsion.
        #================================
        self.mtx = mtx
        self.dist = dist

    def get_calibration_params(self):
        return self.mtx, self.dist


class HandEye:
    def __init__(self):
        pass

    def compute_base_to_tag(self,cam_to_gripper,gripper_pose,transla,rota):
        gripper_to_base_translation = np.array([gripper_pose[0], gripper_pose[1], gripper_pose[2]])
        gripper_to_base_rotation = R.from_euler('ZYX', np.flip(np.array([gripper_pose[3], gripper_pose[4], gripper_pose[5]])), degrees=False)
        
        tag_to_camera_translation = np.array([transla[0], transla[1], transla[2]])
        tag_to_camera_rotation = R.from_euler('ZYX',np.flip(np.array([rota[2], rota[1], rota[0]])), degrees=False)

        t_cam_to_gripper = np.array([cam_to_gripper[0], cam_to_gripper[1], cam_to_gripper[2]])
        R_cam_to_gripper = R.from_euler('ZYX', np.flip(np.array([cam_to_gripper[3], cam_to_gripper[4], cam_to_gripper[5]])), degrees=False)
        
        T_cam_to_gripper = transf.create_homogeneous_transform(R_cam_to_gripper,t_cam_to_gripper)
        T_gripper_to_base = transf.create_homogeneous_transform(gripper_to_base_rotation.as_matrix(), gripper_to_base_translation)
        T_tag_to_camera = transf.create_homogeneous_transform(tag_to_camera_rotation.as_matrix(), tag_to_camera_translation)

        T_base_to_camera =T_gripper_to_base @ T_cam_to_gripper
        T_base_to_tag=  T_gripper_to_base @ T_cam_to_gripper @ T_tag_to_camera

        
        #self.open3d_toolbox.displayTriedre([T_base_to_camera], ["Camera"], 0.05)
        #self.open3d_toolbox.displayTriedre([T_gripper_to_base], ["Robot"], 0.1)
        #self.open3d_toolbox.displayTriedre([T_base_to_tag], ["Tag"], 0.2)
        
        #self.open3d_toolbox.updateRenderer()

        self.all_T_base_to_tag.append(T_base_to_tag)
 
        time.sleep(0.5)
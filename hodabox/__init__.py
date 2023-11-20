try:
    import cv2
except ImportError:
    print("OpenCV non installé.")
    
try:
    from scipy.spatial.transform import Rotation as R
except ImportError:
    print("Scipy non installé.")
    
try:
    from matplotlib import pyplot as plt
except ImportError:
    print("Matplotlib non installé.")
    
try: 
    from mpl_toolkits import mplot3d
    print("tout va bien")
except ImportError:
    print("Mplot3d non installé.")
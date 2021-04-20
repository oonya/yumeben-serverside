import cv2
import numpy as np
from sklearn.cluster import KMeans
import base64

from colormath.color_diff import delta_e_cie2000
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color





class ImageProcess():
    def __init__(self):
        pass
    

    def np2byte(img):
        result, dst_data = cv2.imencode('.jpg', img)
        dst_base64 = base64.b64encode(dst_data)

        return dst_base64


    def byte2np(byte):
        img_data = base64.b64decode(byte)
        img_np = np.fromstring(img_data, np.uint8)
        src = cv2.imdecode(img_np, cv2.IMREAD_ANYCOLOR)

        return src

    
    def get_color_list(img_bgr, colorNum):
        img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        mask = ImageProcess.masking(img)
        mask = ImageProcess.gamma_correction(mask)
        
        pixels = ImageProcess.get_kmeans_pixels(mask, colorNum)

        colors = ImageProcess.color_categorize(pixels)
        
        rgbs = {'green':[0,255,0], 'red':[255,0,0], 'blue':[0,0,255], 'yellow':[255,255,0], 'purple':[128,0,128], 'orange':[255,165,0], 'pink':[255,102,204],'brown':[205,133,63]}
        
        res = []
        for color in colors:
            u = {"name":color, "rgb":rgbs[color]}
            res.append(u)

        return res
        # img_byte = ImageProcess.np2byte(mask).decode('utf-8')
    

    def color_categorize(pixels):
        colors = ['green', 'red', 'blue', 'yellow', 'purple', 'orange', 'pink', 'brown']
        rgbs = np.uint8([[[0,255,0], # green
                        [255, 0, 0],# red
                        [0, 0, 255],# blue
                        [255, 255, 0],#  yellow
                        [128, 0, 128],#  purple
                        [255, 165, 0],#  orange
                        [255, 102, 204],# pink
                        [205, 133, 63],# brown
                        ]])


        res = []
        for target in pixels:
            deltas = np.uint8([])
            for i, color in enumerate(colors):
                rgb = rgbs[0][i]
                deltas = np.append(deltas, ImageProcess.my_delta(rgb, target))

            res.append(colors[np.argmin(deltas)])

        return res
    

    def my_delta(rgb1, rgb2):
        lab1 = convert_color(sRGBColor(*(rgb1 / 255)),LabColor, target_illuminant='d65')
        lab2 = convert_color(sRGBColor(*(rgb2 / 255)),LabColor, target_illuminant='d65')

        return delta_e_cie2000(lab1, lab2)


    def get_kmeans_pixels(mask, k):
        data = np.reshape(mask, (mask.shape[0]*mask.shape[1], mask.shape[2])) # クラスタリングのために2次元に直す
        data = data[(data != 0).all(axis=1)]

        n_clusters= k # クラスタ数(何色に減色するか)
        model = KMeans(n_clusters=n_clusters, random_state=10).fit(data)
        labels = model.labels_


        max_saturation_pixels = []
        for l in range(0,n_clusters):
            clusters = data[labels==l, :]
            max_saturation_pixels.append(ImageProcess.getMaxSaturationPixel(clusters))

        max_saturation_pixels = np.concatenate([max_saturation_pixels])
        
        return max_saturation_pixels


    def getMaxSaturationPixel(clusters):
        hsv_c = cv2.cvtColor(np.uint8([clusters]), cv2.COLOR_RGB2HSV)
        s = hsv_c[:, :, 1]
        return clusters[np.argmax(s[0])]


    def gamma_correction(img):

        # gamma = 3.1 # gammaはパラメータで、1.0より大きいと明るく、小さいと暗くなる
        gamma = 2.2

        lookUpTable = np.zeros((256, 1), dtype = 'uint8')

        for i in range(256):
            lookUpTable[i][0] = 255 * pow(float(i) / 255, 1.0 / gamma)

        img_gamma = cv2.LUT(img, lookUpTable)

        return img_gamma


    def masking(img):
        img = ImageProcess.white_balance(img)
        mor = ImageProcess.my_bin(img)
        mor = cv2.cvtColor(mor, cv2.COLOR_GRAY2RGB)
        mask = mor & img
        return mask


    def white_balance(img):
        result = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
        avg_a = np.average(result[:, :, 1])
        avg_b = np.average(result[:, :, 2])
        result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
        result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
        result = cv2.cvtColor(result, cv2.COLOR_LAB2RGB)
        return result
        
    
    def my_bin(img):
        img_g = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)[:, :, 1]
        ret, th = cv2.threshold(img_g, 0, 255, cv2.THRESH_OTSU)
        kernel = np.ones((20, 20), np.uint8)
        mor = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel)
        return mor
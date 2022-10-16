import cv2
import numpy as np
from sklearn.cluster import KMeans
import pandas as pd
import os

# file location
dirname = os.path.dirname(__file__)

# load image from disk
def load_image(imgPath):
    img = cv2.imread(imgPath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.reshape((img.shape[0] * img.shape[1], 3))
    return(img)


# identify most important colors
def top_colors(img):

    cluster = KMeans(5).fit(img)
    cLabels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
    (proportion,_) = np.histogram(cluster.labels_, bins = cLabels)

    # proportion of the image made up by the color
    proportion = proportion.astype("float")
    proportion /= proportion.sum()
    colors = cluster.cluster_centers_
    proportion = proportion.tolist()
    colors = colors.tolist()

    return (proportion, colors)

def construct_dataframe(propList, colorList, folderList):
    # dataframe struct
    d = {
        'Item': folderList,
        'color0c': [], 
        'color1c' : [], 
        'color2c' : [],
        'color3c' : [],
        'color4c' : [],
        'color0p': [], 
        'color1p' : [], 
        'color2p' : [],
        'color3p' : [],
        'color4p' : []}

    # populate df
    for n, i in enumerate(propList):
        prop = propList[n]
        color = colorList[n]

        for pos, item in enumerate(prop):
            dictKey = 'color' + str(pos) + 'p'
            d[dictKey].append(prop[pos])

        for pos, item in enumerate(color):
            dictKey = 'color' + str(pos) + 'c'
            d[dictKey].append(color[pos])

    df = pd.DataFrame(data = d)
    return(df)

propList = []
colorList = []
folderList = []

# Images Folder
imgFolder = os.path.join(dirname, 'archiveFruit/fruits-360-original-size/fruits-360-original-size/Training/limitedselection')

# Load images
for root, dirs, files in os.walk(imgFolder):
    for dir in dirs:

        subfolder = os.path.join(imgFolder, dir)

        for filename in os.listdir(subfolder):

            img = load_image(os.path.join(subfolder, filename))
            proportions, colors = top_colors(img)

            # append to lists
            propList.append(proportions)
            colorList.append(colors)
            folderList.append(os.path.split(subfolder)[1])

df = construct_dataframe(propList, colorList, folderList)
print(df)










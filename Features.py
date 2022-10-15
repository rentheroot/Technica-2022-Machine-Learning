import cv2
import numpy as np
from sklearn.cluster import KMeans
import pandas as pd

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
    (proportion, _) = np.histogram(cluster.labels_, bins = cLabels)

    # proportion of the image made up by the color
    proportion = proportion.astype("float")
    proportion /= proportion.sum()
    colors = cluster.cluster_centers_

    return (proportion, colors)

def construct_dataframe(proportions, colors):
    df = pd.DataFrame()

# Load image
img = load_image('r0_115.jpg')
proportions, colors = top_colors(img)
print(proportions, colors)









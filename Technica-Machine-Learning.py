from PIL import Image

filepath = "Technica-Machine-Learning"
img = Image.open(filepath)

width = img.width
height = img.height

print("The height of the image is: ", height)
print("The width of the image is: ", width)

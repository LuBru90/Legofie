import matplotlib.pyplot as plt
import cv2
import random
import sys
import numpy as np
import time


if len(sys.argv) == 1:
    print("Usage:")
    print("python %s <file name (jpg)>\n<brick count x>\n<brick res (1)>\n<contrast (+-5)>\n<brightness(+-150)>\n<dpi (300)>" % sys.argv[0])

    sys.argv = list()
    [sys.argv.append(x) for x in ['', 'monalisa.jpg', 15, 2, 1.7, -70, 200]]
    print('Using defaults:', sys.argv)


name = sys.argv[1]
image = plt.imread(name)
x,y = image.shape[:2]
ratio = x/y
brickSize = int(sys.argv[2])

resImage = cv2.resize(image, (brickSize, int(ratio*brickSize)), interpolation = cv2.INTER_AREA)
recImage = cv2.resize(resImage, (int(image.shape[1]), int(ratio*image.shape[0])), interpolation = cv2.INTER_AREA)

faces = list()
faces.append("legoPost.jpg")
faces.append("legoPost1.jpg")
faces.append("legoPost2.jpg")
faces.append("legoPost3.jpg")

brickRes = int(float(sys.argv[3])*image.shape[0])//brickSize
bricks = list()
padding = 2
for face in faces:
    legoImage = cv2.imread(face, 0)
    bricks.append(cv2.resize(legoImage[padding:legoImage.shape[0]-padding, padding:legoImage.shape[1]-padding], (brickRes, brickRes), interpolation = cv2.INTER_AREA))


threshold = 5
yBricks = list()
t0 = time.time()
for y in range(len(resImage)):
    xBricks = list()
    for x in range(len(resImage[0])):
        raw_coloredBrick = cv2.cvtColor(random.choice(bricks), cv2.COLOR_GRAY2RGB)
        temp = resImage[y][x]
        coloredBrick = raw_coloredBrick//2 + temp//2
        xBricks.append(coloredBrick)
    x = cv2.hconcat(xBricks)
    yBricks.append(x)

raw_legoImage = cv2.vconcat(yBricks)
legoImage = cv2.convertScaleAbs(raw_legoImage + np.random.normal(0, 2, raw_legoImage.shape), alpha = float(sys.argv[4]), beta = float(sys.argv[5]))
legoImage = np.where(raw_legoImage > threshold, legoImage, 15)

#plt.imshow(legoImage)
#plt.savefig("%s_%s_lego.jpg" % (brickSize, name.replace(".jpg", "")), bbox_inches = 'tight', dpi=int(sys.argv[6]))

fig, ax = plt.subplots(1, 2)
ax[0].imshow(image)
ax[1].imshow(legoImage)

ax[0].axis('off')
ax[1].axis('off')
plt.savefig("%s_%s_lego.jpg" % (brickSize, name.replace(".jpg", "")), bbox_inches = 'tight', dpi=int(sys.argv[6]))
#plt.show()


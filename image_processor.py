import os
# from time import time
import cv2
import numpy as np
from imutils.object_detection import non_max_suppression


def crop_image(img_gray):
    method = cv2.TM_SQDIFF_NORMED
    template = cv2.imread('Images/OCVTemplates2/template1.png')
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(img_gray, template, method)
    mn, _, mnLoc, _ = cv2.minMaxLoc(result)
    MPx, MPy = mnLoc
    # tcols, trows = template.shape[:2]
    icols, irows = img_gray.shape[:2]
    # cv2.rectangle(img_gray, (MPx, MPy), (MPx + trows, MPy + tcols), (0, 0, 255), 2)
    return img_gray[MPy:icols, 0:irows], MPy


def check_present_msg(filepath, mcount=2):
    # start_time = time()
    img_rgb = cv2.imread(filepath)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    img_gray, MPy = crop_image(img_gray)
    templates_path = 'Images/OCVTemplates'
    for ftemplate in os.listdir(templates_path):
        temppath = os.path.join(templates_path, ftemplate)
        if os.path.isfile(temppath):
            template = cv2.imread(temppath)
            template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            h, w = template.shape[:2]
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = .8
            loc = np.where(res >= threshold)[::-1]
            # print(loc)
            rect = []
            for pt in zip(*loc):
                rect.append((pt[0], pt[1], pt[0] + w, pt[1] + h))
            pick = non_max_suppression(np.array(rect))
            count = len(pick)
            if count >= mcount:
                # print(time() - start_time)
                return count, pick, MPy
    return False, None, None


def test(filepath):
    succ, pick, MPy = check_present_msg(filepath, 1)
    img_rgb = cv2.imread(filepath)
    if succ:
        print(True)
        for (sx, sy, ex, ey) in pick:
            cv2.rectangle(img_rgb, (sx, sy + MPy), (ex, ey + MPy), (0, 0, 255), 2)
        # cv2.imshow("img", img_rgb)
        # cv2.waitKey(0)
        cv2.imwrite('Images/Test/result.png', img_rgb)
    else:
        print(False)


def test2(filepath):
    img_rgb = cv2.imread(filepath)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    img_gray = crop_image(img_gray)
    cv2.imwrite('Images/Test/result.png', img_gray)


# test('Images/Apvaadak/AttSShots/6th Sem_DMDW_18CS641-screenshot-attscn.png')
# test2('Images/Test/Apvaadak-msgpost3.png')

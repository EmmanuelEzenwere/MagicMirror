#                     Computer Vision | Architect : Nuel Ezenwere

import numpy.core.multiarray
import cv2
import dlib
import numpy as np
import os
# import datetime as dt
# from skinComplexion import plot_images
# from PIL import Image

__author__ = 'Ezenwere.Nuel'


class FaceSwap(object):
    def __init__(self, hairmodel_image, selfie_image):
        """
        :param hairmodel_image: a numpy array of the primary image ie we use hair from image1.
        :param selfie_image: a numpy array representation of an image. we use face from image2, face from image2 is replaced by face from image1
        """

        self.destination_image = hairmodel_image
        self.sourceface_image = selfie_image
        self.convex_hull_color = 1
        self.face_mask_color = 1
        self.scale_factor = 1
        self.colour_correct_blur_frac = 0.6
        self.feather_amount = 1
        self.align_points = list(range(0, 68))

    @staticmethod
    def get_landmarks(image):
        """
        :param: image, a numpy array representation of the input image to find landmarks
        :type: numpy array
        :return: landmarks, a (68 x 2) matrix of coordinates, of special features in any image, for this instance a face.
        :type: matrix of dimension (68 x 2)
        """

        detector = dlib.get_frontal_face_detector()
        rects = detector(image, 1)

        pose_predictor = os.path.dirname(__file__)+"/shape_predictor_68_face_landmarks.dat"
        predictor = dlib.shape_predictor(pose_predictor)

        landmarks = np.matrix([[int(p.x), int(p.y)] for p in predictor(image, rects[0]).parts()])

        return landmarks

    def draw_convex_hull(self, image, points):
        """
        :param image: numpy array on which to draw the convex hull (a convex polyhedral).
        :param points: coordinates of the vertices of the convex hull/ convex polyhedral to be drawn on the input image.
        :return: numpy array, with convex hull overlaid on the input image.
        """
        hull_color = self.convex_hull_color
        points = cv2.convexHull(points)
        cv2.fillConvexPoly(image, points, color=hull_color)

    @staticmethod
    def get_facemask(image, landmarks):
        """
        :param image, numpy array
        :param landmarks: matrix, default = (68x2) collection of coordinates of primary features of a face: eyes, mouth, ...
        :return: matrix with same shape as image, a rescaled version of the input image.
        """

        face_mask = np.zeros(image.shape, dtype=image.dtype)
        face_ConvexHull = np.array(cv2.convexHull(landmarks))[:, 0]
        face_ConvexHull = face_ConvexHull.astype(np.int32)
        face_mask = cv2.fillPoly(face_mask, [face_ConvexHull], (255, 255, 255))
        return face_mask

    @staticmethod
    def transformation_from_points(points1, points2):
        """
        Return an affine transformation [s * r | T] such that:
            sum ||s*r*p1,i + T - p2,i||^2
        is minimized.
        """
        # Solve the procrustes problem by subtracting centroids, scaling by the
        # standard deviation, and then using the SVD to calculate the rotation.

        points1 = points1.astype(np.float64)
        points2 = points2.astype(np.float64)

        c1 = np.mean(points1, axis=0)
        c2 = np.mean(points2, axis=0)
        points1 -= c1
        points2 -= c2

        s1 = np.std(points1)
        s2 = np.std(points2)
        points1 /= s1
        points2 /= s2

        u, s, vt = np.linalg.svd(points1.T * points2)

        # The r we seek is in fact the transpose of the one given by u * vt. This
        # is because the above formulation assumes the matrix goes on the right
        # (with row vectors) where as our solution requires the matrix to be on the
        # left (with column vectors).
        r = (u * vt).T

        return np.vstack([np.hstack(((s2 / s1) * r, c2.T - (s2 / s1) * r * c1.T)), np.matrix([0., 0., 1.])])

    @staticmethod
    def warp(image, m, dshape):
        output_image = np.zeros(dshape, dtype=image.dtype)  # this creates a black background .
        cv2.warpAffine(image, m[:2], (dshape[1], dshape[0]), dst=output_image, borderMode=cv2.BORDER_TRANSPARENT,
                       flags=cv2.WARP_INVERSE_MAP)
        return output_image

    @staticmethod
    def face_center(hairface_landmarks):
        """
        :param hairface_landmarks: np array, each row contains [x,y] co-ordinates of landmarks on the input image
        :return: (center-x, center-y) co-ordinates of the center of the image.
        """
        hairface_ConvexHull = cv2.convexHull(hairface_landmarks)[:, 0]

        rect_vertices = cv2.boundingRect(np.float32(hairface_ConvexHull))
        center = (int(rect_vertices[0]) + int(rect_vertices[2] / 2), int(rect_vertices[1]) + int(rect_vertices[3] / 2))

        return center

    def edgeRefinement(self, source_image, destination_image, sourceface_mask, hairface_landmarks):
        """
        :param source_image: np.array representation of the selfie model image
        :param destination_image: np.array representation of the hairstyle model (adjusted) image
        :param sourceface_mask: np.array (black and white image of the selfie model's face )
        :param hairface_landmarks: np.array 2d matrix of the hairmodel facial landmarks.
        :return: np.array image of the seamlessly cloned face from the source_image on the template face at the destination
                 image.
        """
        center = self.face_center(hairface_landmarks)
        edge_blended = cv2.seamlessClone(source_image, destination_image, sourceface_mask, center, cv2.NORMAL_CLONE)

        return edge_blended

    @staticmethod
    def get_lum(image, x, y, w, h, k, gray):
        """
        Note to my self (Nuel): I suspect this function returns the lumination of a region bounded by (x, y, w, h, k)
        :param image:
        :param x:
        :param y:
        :param w:
        :param h:
        :param k:
        :param gray:
        :return:
        """

        if gray == 1:
            image = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)

        i1 = range(int(-w/2), int(w/2))
        j1 = range(0, h)

        lumar = np.zeros((len(i1), len(j1)))
        for i in i1:
            for j in j1:
                lum = np.min(image[y+k*h, x+i])
                lumar[i][j] = lum

        return np.min(lumar)

    def swap(self):
        """

        :return: np.array. The selfie model with a new hairstyle from the hairmodel.
        """
        hairface_landmarks = self.get_landmarks(self.destination_image)  # hair
        sourceface_landmarks = self.get_landmarks(self.sourceface_image)  # face
        # # ********** Geometric Model ********************
        # geometric_model = cv2.fillPoly(self.sourceface_image.copy(), sourceface_landmarks, (255, 255, 255))
        # model_date = dt.datetime.now()
        # model_path = os.path.dirname(__file__) + '/file_storage/trash/test_' + str(model_date) + '.jpg'
        # cv2.imwrite(model_path, geometric_model)
        # geometric_model = Image.open(model_path)
        # # ************************************************
        # plot_images(geometric_model, 'geometric model')
        # # ************************************************
        procrustes = self.transformation_from_points(sourceface_landmarks[self.align_points], hairface_landmarks[self.align_points])
        warped_destination_image = self.warp(self.destination_image, procrustes, self.sourceface_image.shape)  # self.sourceface_image.shape)
        # warped_hairface_landmarks = self.get_landmarks(warped_destination_image)

        # obtain the landmark parameters as a list.
        p17 = tuple(sourceface_landmarks[17].tolist()[0])
        p19 = tuple(sourceface_landmarks[19].tolist()[0])
        p24 = tuple(sourceface_landmarks[24].tolist()[0])
        p26 = tuple(sourceface_landmarks[26].tolist()[0])
        p6 = tuple(sourceface_landmarks[6].tolist()[0])
        p10 = tuple(sourceface_landmarks[10].tolist()[0])

        # Calculate the distance btw (p6, p24)
        r6_24 = np.linalg.norm(np.matrix(p6) - np.matrix(p24))
        # Calculate the distance btw (p10, p17)
        r10_17 = np.linalg.norm(np.matrix(p10) - np.matrix(p17))
        # Calculate the distance btw (p6, p26)
        r6_26 = np.linalg.norm(np.matrix(p6) - np.matrix(p26))
        # Calculate the distance btw (p6, p19)
        r6_19 = np.linalg.norm(np.matrix(p6) - np.matrix(p19))

        # Calculate the translation/increment.

        # Euclidean distance from p10 to p17
        r1 = r10_17 * (1 + 1/8)
        # Euclidean distance from p6 to p68
        r2 = r6_19 * (1 + 1/8)
        # Euclidean distance from p6 to p69
        r3 = r6_24 * (1 + 1/8)
        # Euclidean distance from p6 to p70
        r4 = r6_26 * (1 + 1/8)

        # Angle between line 10,17 and x-axis
        p10x, p10y = p10
        p17x, p17y = p17
        theta1 = np.math.atan(abs((p17y - p10y) / (p17x - p10x)))

        # Angle between line 6,19 and x-axis
        p6x, p6y = p6
        p19x, p19y = p19
        theta2 = np.math.atan(abs((p19y - p6y) / (p19x - p6x)))

        # Angle between line 6,24 and x-axis
        p24x, p24y = p24
        theta3 = np.math.atan(abs((p24y - p6y) / (p24x - p6x)))

        # Angle between line 6,26 and x-axis
        p26x, p26y = p26
        theta4 = np.math.atan(abs((p26y - p6y) / (p26x - p6x)))

        p68 = (int(p6x - r2 * np.cos(theta2)), int(p6y - r2 * np.sin(theta2)))
        p69 = (int(p6x + r3 * np.cos(theta3)), int(p6y - r3 * np.sin(theta3)))
        p70 = (int(p10x - r1 * np.cos(theta1)), int(p10y - r1 * np.sin(theta1)))
        p71 = (int(p6x + r4 * np.cos(theta4)), int(p6y - r4 * np.sin(theta4)))
        # test_img = self.sourceface_image.copy()
        # cv2.circle(test_img, (p24[0], p24[1]), 3, color=(255, 153, 0))
        # cv2.circle(test_img, (p19[0], p19[1]), 3, color=(255, 153, 0))
        # cv2.circle(test_img, (p6[0], p6[1]), 3, color=(255, 153, 0))
        # cv2.circle(test_img, (p17[0], p17[1]), 3, color=(255, 153, 0))
        # cv2.circle(test_img, (p26[0], p26[1]), 3, color=(255, 153, 0))
        # cv2.circle(test_img, (p6[0], p6[1]), 3, color=(255, 153, 0))
        # cv2.circle(test_img, p68, 3, color=(255, 153, 0))
        # cv2.circle(test_img, p69, 3, color=(255, 153, 0))
        # cv2.circle(test_img, p70, 3, color=(255, 153, 0))
        # cv2.circle(test_img, p71, 3, color=(255, 153, 0))
        #
        # plot_images(test_img, 'heart')
        # for i in range(0, 68):
        #     pi = tuple(warped_hairface_landmarks[i].tolist()[0])
        #     cv2.circle(test_img, pi, 3, color=(255, 0, 0))
        # plot_images(test_img, 'heart')
        sourceface_landmarks_aug = sourceface_landmarks.copy()
        sourceface_landmarks_aug[19, 0] = p68[0]
        sourceface_landmarks_aug[19, 1] = p68[1]
        sourceface_landmarks_aug[24, 0] = p69[0]
        sourceface_landmarks_aug[24, 1] = p69[1]
        sourceface_landmarks_aug[17, 0] = p70[0]
        sourceface_landmarks_aug[17, 1] = p70[1]
        sourceface_landmarks_aug[26, 0] = p71[0]
        sourceface_landmarks_aug[26, 1] = p71[1]

        # sourceface_image_copy = self.sourceface_image.copy()
        # for i in np.array(sourceface_landmarks_aug):
        #     print(tuple(i))
        #     print(cv2.circle(sourceface_image_copy, tuple(i), 3, color=(255, 153, 0)))
        # plot_images(sourceface_image_copy, 'test1')
        # hair_facemask = self.get_facemask(warped_destination_image, warped_hairface_landmarks)
        source_facemask = self.get_facemask(self.sourceface_image, sourceface_landmarks_aug)
        # combined_facemask = np.max([source_facemask, hair_facemask], axis=0)
        combined_facemask = source_facemask
        newlook = self.edgeRefinement(self.sourceface_image, warped_destination_image, combined_facemask, sourceface_landmarks_aug)

        # re-shapen newlook
        newlook_landmark = np.array(self.get_landmarks(newlook))
        xmax, ymax = newlook_landmark.max(axis=0)
        newlook = newlook.copy()[0:ymax, 0:newlook.shape[1]]

        return newlook


# base_path = os.path.dirname(__file__)
# # /home/higgsfield/PycharmProjects/MagicMirror.ai/file_storage/trash/oval/white
# test_date = dt.datetime.now()
# save_path = base_path+'/file_storage/trash/test_'+str(test_date)+'.jpg'
# img2_path = base_path+'/file_storage/trash/heart/white/5.jpg'
# img1_path = base_path+'/file_storage/trash/heart/white/heart_ahannigan4.jpg'
# img1 = Image.open(img1_path)
# img2 = Image.open(img2_path)
# plot_images(img1, 'test1')
# plot_images(img2, 'test2')
# img = FaceSwap(cv2.imread(img2_path), cv2.imread(img1_path)).swap()
# cv2.imwrite(save_path, img)
# img = Image.open(save_path)
# plot_images(img, 'heart')

# Next research -- algorithm to change skin tone.
# Investigation the precision of the center of the hairface model supplied for seamless cloning : center = (int(rect_vertices[0]) + int(rect_vertices[2] / 2), int(rect_vertices[1]) + int(rect_ve
# Olotu square -- Incubator

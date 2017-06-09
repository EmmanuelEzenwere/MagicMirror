#                     Computer Vision | Computer Vision Expert: Nuel Ezenwere


import cv2
import dlib
import numpy as np
import os

__author__ = 'Ezenwere.Nuel'


class FaceSwap(object):
    def __init__(self, destination_image, sourceface_image):  # hair, face
        """
        :param destination_image: a numpy array of the primary image ie we use hair from image1.
        :param sourceface_image: a numpy array representation of an image. we use face from image2, face from image2 is replaced by face from image1
        """

        # ===================================== Key Regions ============================================================
        left_eye_points = list(range(42, 48))
        right_eye_points = list(range(36, 42))
        nose_points = list(range(27, 35))
        mouth_points = list(range(48, 61))
        left_brow_points = list(range(22, 27))
        right_brow_points = list(range(17, 22))
        face_points = list(range(17, 68))
        jaw_points = list(range(0, 17))

        # ==============================================================================================================

        # ============================== landmark indices; Points used to line up the images.===========================

        # Points used to line up the images.
        align_points = [left_brow_points + right_eye_points + left_eye_points + face_points + jaw_points
                        + right_brow_points + nose_points + mouth_points]

        # Points from the second image to overlay on the first. The convex hull of each element will be overlaid.
        overlay_points = [left_eye_points + right_eye_points + left_brow_points + right_brow_points + nose_points
                          + mouth_points + face_points + jaw_points]

        # ======================================================================================================================

        self.destination_image = destination_image
        self.sourceface_image = sourceface_image
        self.convex_hull_color = 1
        self.face_mask_color = 1
        self.scale_factor = 1
        self.colour_correct_blur_frac = 0.6
        self.feather_amount = 1
        self.landmark_key = {"left_eye_points": list(range(42, 48)), "right_eye_points": list(range(36, 42)),
                             "nose_points": list(range(27, 35)), "mouth_points": list(range(48, 61)),
                             "left_brow_points": list(range(22, 27)), "right_brow_points": list(range(17, 22)),
                             "face_points": list(range(17, 68)), "jaw_points": list(range(0, 17))}
        self.align_points = align_points
        self.overlay_points = overlay_points

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

        pose_predictor = "shape_predictor_68_face_landmarks.dat"
        predictor = dlib.shape_predictor(pose_predictor)

        landmarks = np.matrix([[int(p.x), int(p.y)] for p in predictor(image, rects[0]).parts()])

        return landmarks

    def rescale(self, image):
        """
        :param image: input image to find landmarks
        :type: numpy array
        :return: A rescaled version of the input image.
        :type: matrix of shape image.shape
        """

        scale_factor = self.scale_factor
        image_width = image.shape[1]
        image_height = image.shape[0]

        rescaled_image = cv2.resize(image, (image_width * scale_factor, image_height * scale_factor))

        return rescaled_image

    def draw_convex_hull(self, image, points):
        """
        :param image: numpy array on which to draw the convex hull (a convex polyhedral).
        :param points: coordinates of the vertices of the convex hull/ covex polyhedral to be drawn on the input image.
        :return: numpy array, with convex hull overlayed on the input image.
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

        facemask = np.zeros(image.shape, dtype=image.dtype)
        face_ConvexHull = np.array(cv2.convexHull(landmarks))[:, 0]
        face_ConvexHull = face_ConvexHull.astype(np.int32)
        facemask = cv2.fillPoly(facemask, [face_ConvexHull], (255, 255, 255))

        return facemask

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

    def correct_colours(self, template, source, landmarks_image1):
        """

        :param template, numpy array,  primary image, to be color corrected to blend with image2 at specified landmarks, the secondary image.
        :param source, numpy array, secondary image.
        :param landmarks_image1: matrix of dimension (68x2)
        :return: image1 with color corrected to blend with image 2 at given landmarks.

        """
        colour_correct_blur_frac = self.colour_correct_blur_frac
        landmark_key = self.landmark_key
        left_eye_points = landmark_key["left_eye_points"]
        right_eye_points = landmark_key["right_eye_points"]

        blur_amount = colour_correct_blur_frac * np.linalg.norm(
            np.mean(landmarks_image1[left_eye_points], axis=0) - np.mean(landmarks_image1[right_eye_points], axis=0))
        blur_amount = int(blur_amount)

        # If blur_amount is not even, make it even.
        if blur_amount % 2 == 0:
            blur_amount += 1

        # Smooth both images by applying a gaussian blur.
        image_1_blur = cv2.GaussianBlur(template, (blur_amount, blur_amount), 0)
        image_2_blur = cv2.GaussianBlur(source, (blur_amount, blur_amount), 0)

        # Avoid divide-by-zero errors.
        image_2_blur += (128 * (image_2_blur <= 1.0)).astype(image_2_blur.dtype)

        # Smoothed mix of both images.
        smoothed_mix = (source.astype(np.float64) * image_1_blur.astype(np.float64) / image_2_blur.astype(np.float64))

        return smoothed_mix

    def face_center(self, image):
        hairface_landmarks = self.get_landmarks(image)
        hairface_ConvexHull = cv2.convexHull(hairface_landmarks)[:, 0]

        rect_vertices = cv2.boundingRect(np.float32(hairface_ConvexHull))
        center = (int(rect_vertices[0]) + int(rect_vertices[2] / 2), int(rect_vertices[1]) + int(rect_vertices[3] / 2))

        return center

    def edgeRefinement(self, source_image, destination_image, sourceface_mask):
        """
        :param source_image:
        :param destination_image:
        :param sourceface_mask:
        :return: np.array image of the seamlessly cloned face from the source_image on the template face at the destination
                 image.
        """
        center = self.face_center(destination_image)
        edgeblended = cv2.seamlessClone(source_image, destination_image, sourceface_mask, center, cv2.NORMAL_CLONE)

        return edgeblended

    def swap(self):
        destination_image = self.destination_image
        source_image = self.sourceface_image
        align_points = self.align_points
        hairface_landmarks = self.get_landmarks(destination_image)  # hair
        sourceface_landmarks = self.get_landmarks(source_image)  # face

        procrustes = self.transformation_from_points(hairface_landmarks[align_points],
                                                     sourceface_landmarks[align_points])
        warped_source_image = self.warp(source_image, procrustes, destination_image.shape)
        warped_sourcefacelandmarks = self.get_landmarks(warped_source_image)

        hair_facemask = self.get_facemask(destination_image, hairface_landmarks)
        source_facemask = self.get_facemask(warped_source_image, warped_sourcefacelandmarks)
        combined_facemask = np.max([source_facemask, hair_facemask], axis=0)

        newlook = self.edgeRefinement(warped_source_image, destination_image, combined_facemask)

        return newlook

    def display_newlook(self):
        win = dlib.image_window()
        win.set_image(self.swap())
        dlib.hit_enter_to_continue()
        return None

    def save_newlook(self, filename):
        newlook = self.swap()
        cv2.imwrite(str(filename), newlook)
        return "saved newlook to " + str(filename) + " ..."
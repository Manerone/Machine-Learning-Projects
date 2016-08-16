import numpy as np
from numpy import linalg as LA


class Eigenface:

    @staticmethod
    def calculate_mean_face(array_of_images):
        mean = np.mean(array_of_images, axis=0, dtype=np.uint32)
        return np.array(mean, dtype=np.uint8)

    @staticmethod
    def transform_images_to_array(images_in_matrix_form):
        images = []
        for image in images_in_matrix_form:
            images.append(image.ravel())
        return np.array(images)

    @staticmethod
    def images_minus_mean_face(array_of_images, mean_face):
        images = []
        for image in array_of_images:
            images.append(image - mean_face)
        return np.array(images)

    @staticmethod
    def order_eigenvectors_by_eigenvalues(eigenvectors, eigenvalues):
        idx = eigenvalues.argsort()[::-1]
        return eigenvectors[:, idx]

    @staticmethod
    def calculate(images, number_of_eigenfaces=5):
        images = np.array(images)  # num_imgs X heigth X width
        n_of_images, heigth, width = images.shape

        mean_face = Eigenface.calculate_mean_face(images)  # heigth X width
        immf = Eigenface.images_minus_mean_face(
            images, mean_face)  # heigth X width

        images = Eigenface.transform_images_to_array(
            immf)  # num_img X (number of pixeis in images)

        covariance_matrix = np.cov(images)  # num_img x num_img
        eigenvalues, eigenvectors = LA.eig(covariance_matrix)
        eigenvectors = Eigenface.order_eigenvectors_by_eigenvalues(
            eigenvectors, eigenvalues)
        eigenvectors = eigenvectors[:number_of_eigenfaces]  # num+img X 1
        tpm = []
        for eigenvector in eigenvectors:
            tpm.append([np.real(i) for i in eigenvector])
        eigenvectors = tpm

        transposed_images = images.transpose()
        eigenfaces = []
        for eigenvector in eigenvectors:
            multiplication = np.dot(transposed_images, eigenvector)
            eigenfaces.append(multiplication.reshape(heigth, width))
        eigenfaces = np.array(eigenfaces)
        return eigenfaces
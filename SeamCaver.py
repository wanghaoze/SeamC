# This Python file use the following encoding: utf-8
from PIL import Image
import numpy as np
import os
import cv2
import argparse
from numba import jit
from scipy import ndimage as ndi

SEAM_COLOR = np.array([255, 200, 200])  # seam visualization color (BGR)
SHOULD_DOWNSIZE = True  # if True, downsize image for faster carving
DOWNSIZE_WIDTH = 500  # resized image width if SHOULD_DOWNSIZE is True
ENERGY_MASK_CONST = 100000.0  # large energy value for protective masking
MASK_THRESHOLD = 10  # minimum pixel intensity for binary mask
USE_FORWARD_ENERGY = True  # if True, use forward energy algorithm


class SeamCaver:
    def __init__(self, path, is_rgb=False, mask=None, remove_mask=None,
                 dh=30, dw=50, to_path='output/', mode='forwardEnergy'):
        self.photoPath = path
        self.im = cv2.imread(self.photoPath)  # Image.open(self.photoPath, 'r')
        self.im_reform = self.im.copy()
        # self.photoWidth = self.im.size[0]
        # self.photoHeight = self.im.size[1]
        self.photoHeight, self.photoWidth= self.im.shape[:2]
        self.name = self.photoPath.split('/')[-1]
        # print(self.photoPath)
        # print(self.photoWidth)
        # print(self.photoHeight)
        # print(self.name)
        # self.im.show('a')
        self.rgb = is_rgb
        self.toHeight = self.photoHeight+dh
        self.toWidth = self.photoWidth+dw
        self.mask = cv2.imread(mask, 0) if mask else None
        self.remove_mask = cv2.imread(remove_mask, 0) if remove_mask else None
        self.dh = dh
        self.dw = dw
        self.toPath = to_path
        self.mode = (mode is 'forwardEnergy')
        self.completeRate = 0
        self.totalWork = abs(dh) + abs(dw)

    def seamCarve(self, to_path=None, name=None):
        if to_path is not None:
            self.toPath = to_path
        if not os.path.isdir(self.toPath):
            try:
                os.mkdir(self.toPath)
            except FileNotFoundError:
                print('error in creating dir:' + self.toPath)
        if name is not None:
            self.toPath += name
        else:
            self.toPath += self.name
        a = np.array(self.im)

        # convert function starts here
        self.im = self.im.astype(np.float64)
        dx = self.dw
        dy = self.dh
        print('Total Work Cost:', self.totalWork)
        assert self.photoHeight + dy > 0 and self.photoWidth + dx > 0 and dy <= self.photoHeight and dx <= self.photoWidth

        # cv2.imshow('or', self.im.astype(np.uint8))
        # cv2.imshow('gg', self.im_reform)
        # cv2.waitKey()
        if self.mask is not None:
            self.mask = self.mask.astype(np.float64)
        if SHOULD_DOWNSIZE and self.photoWidth > DOWNSIZE_WIDTH:
            self.im = SeamCaver.resize(self.im, width=DOWNSIZE_WIDTH)
            if self.mask is not None:
                self.mask = SeamCaver.resize(self.mask, width=DOWNSIZE_WIDTH)
            if self.remove_mask is not None:
                self.remove_mask = SeamCaver.resize(self.remove_mask, width=DOWNSIZE_WIDTH)
        self.im_reform = self.im
        if dx < 0:
            # self.im_reform, mask = SeamCaver.seams_removal(self.im_reform, -dx, self.mask, vis=False)
            self.im_reform, mask = SeamCaver.seams_removal(self.im_reform, -dx, self.mask, vis=True)

        elif dx > 0:
            # self.im_reform, mask = SeamCaver.seams_insertion(self.im_reform, dx, self.mask, vis=False)
            self.im_reform, mask = SeamCaver.seams_removal(self.im_reform, dx, self.mask, vis=True)

        if dy < 0:
            self.im_reform = SeamCaver.rotate_image(self.im_reform, True)
            if self.mask is not None:
                self.mask = SeamCaver.rotate_image(self.mask, True)
            # self.im_reform, self.mask = SeamCaver.seams_removal(self.im_reform, -dy, self.mask, vis=False, rot=True)
            self.im_reform, self.mask = SeamCaver.seams_removal(self.im_reform, -dy, self.mask, vis=True, rot=True)
            self.im_reform = SeamCaver.rotate_image(self.im_reform, False)

        elif dy > 0:
            self.im_reform = SeamCaver.rotate_image(self.im_reform, True)
            if self.mask is not None:
                self.mask = SeamCaver.rotate_image(self.mask, True)
            # self.im_reform, mask = SeamCaver.seams_insertion(self.im_reform, dy, self.mask, vis=False, rot=True)
            self.im_reform, self.mask = SeamCaver.seams_removal(self.im_reform, dy, self.mask, vis=True, rot=True)
            self.im_reform = SeamCaver.rotate_image(self.im_reform, False)

        # convert function ends here
        # save the file
        # print(self.toPath)
        # self.im_reform.save(self.toPath)
        cv2.imwrite(self.toPath, self.im_reform)
        cv2.imshow('or', self.im)
        cv2.imshow('gg', self.im_reform)
        cv2.waitKey()
        return self.im_reform

    def object_removal(self, vis=False, horizontal_removal=False):
        self.im = self.im.astype(np.float64)
        self.remove_mask = self.remove_mask.astype(np.float64)
        if self.mask is not None:
            self.mask = self.mask.astype(np.float64)
        self.im_reform = self.im

        h, w = self.im.shape[:2]

        if horizontal_removal:
            self.im_reform = SeamCaver.rotate_image(self.im_reform, True)
            self.remove_mask = SeamCaver.rotate_image(self.remove_mask, True)
            if self.mask is not None:
                self.mask = self.rotate_image(self.mask, True)

        while len(np.where(self.remove_mask > MASK_THRESHOLD)[0]) > 0:
            seam_idx, bool_mask = SeamCaver.get_minimum_seam(self.im_reform, self.mask, self.remove_mask)
            if vis:
                SeamCaver.visualize(self.im_reform, bool_mask, rotate=horizontal_removal)
            self.im_reform = SeamCaver.remove_seam(self.im_reform, bool_mask)
            self.remove_mask = SeamCaver.remove_seam_grayscale(self.remove_mask, bool_mask)
            if self.mask is not None:
                self.mask = SeamCaver.remove_seam_grayscale(self.mask, bool_mask)

        num_add = (h if horizontal_removal else w) - self.im_reform.shape[1]
        self.im_reform, self.mask = SeamCaver.seams_insertion(self.im_reform, num_add, self.mask, vis, rot=horizontal_removal)
        if horizontal_removal:
            self.im_reform = SeamCaver.rotate_image(self.im_reform, False)

        return self.im_reform

    @staticmethod
    def backward_energy(image):
        xGrad = ndi.convolve1d(image, np.array([1, 0, -1]), axis=1, mode='wrap')
        yGrad = ndi.convolve1d(image, np.array([1, 0, -1]), axis=0, mode='wrap')
        grad_mag = np.sqrt(np.sum(xGrad ** 2, axis=2) + np.sum(yGrad ** 2, axis=2))
        vis = SeamCaver.visualize(grad_mag)
        cv2.imwrite("backward_energy_demo.jpg", vis)
        return grad_mag

    @staticmethod
    def forward_energy(im):
        h, w = im.shape[:2]
        im = cv2.cvtColor(im.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float64)

        energy = np.zeros((h, w))
        m = np.zeros((h, w))

        U = np.roll(im, 1, axis=0)
        L = np.roll(im, 1, axis=1)
        R = np.roll(im, -1, axis=1)

        cU = np.abs(R - L)
        cL = np.abs(U - L) + cU
        cR = np.abs(U - R) + cU

        for i in range(1, h):
            mU = m[i - 1]
            mL = np.roll(mU, 1)
            mR = np.roll(mU, -1)

            mULR = np.array([mU, mL, mR])
            cULR = np.array([cU[i], cL[i], cR[i]])
            mULR += cULR

            argmins = np.argmin(mULR, axis=0)
            m[i] = np.choose(argmins, mULR)
            energy[i] = np.choose(argmins, cULR)

        # vis = visualize(energy)
        # cv2.imwrite("forward_energy_demo.jpg", vis)

        return energy

    @staticmethod
    def visualize(im, boolmask=None, rotate=False):  # im:input img
        vis = im.astype(np.uint8)
        if boolmask is not None:
            vis[np.where(boolmask is False)] = SEAM_COLOR
        if rotate:
            vis = SeamCaver.rotate_image(im, False)
        cv2.imshow("visualization", vis)
        cv2.waitKey(1)
        return vis

    @staticmethod
    def resize(image, width):
        dim = None
        h, w = image.shape[:2]
        dim = (width, int(h * width / float(w)))
        return cv2.resize(image, dim)

    @staticmethod
    def rotate_image(image, clockwise):
        k = 1 if clockwise else 3
        return np.rot90(image, k)

    @staticmethod
    def add_seam(im, seam_idx):
        h, w = im.shape[:2]
        output = np.zeros((h, w + 1, 3))
        for row in range(h):
            col = seam_idx[row]
            for ch in range(3):
                if col == 0:
                    p = np.average(im[row, col: col + 2, ch])
                    output[row, col, ch] = im[row, col, ch]
                    output[row, col + 1, ch] = p
                    output[row, col + 1:, ch] = im[row, col:, ch]
                else:
                    p = np.average(im[row, col - 1: col + 1, ch])
                    output[row, : col, ch] = im[row, : col, ch]
                    output[row, col, ch] = p
                    output[row, col + 1:, ch] = im[row, col:, ch]

        return output

    @staticmethod
    def add_seam_grayscale(im, seam_idx):
        h, w = im.shape[:2]
        output = np.zeros((h, w + 1))
        for row in range(h):
            col = seam_idx[row]
            if col == 0:
                p = np.average(im[row, col: col + 2])
                output[row, col] = im[row, col]
                output[row, col + 1] = p
                output[row, col + 1:] = im[row, col:]
            else:
                p = np.average(im[row, col - 1: col + 1])
                output[row, : col] = im[row, : col]
                output[row, col] = p
                output[row, col + 1:] = im[row, col:]

        return output

    @staticmethod
    def remove_seam(im, boolmask):
        h, w = im.shape[:2]
        boolmask3c = np.stack([boolmask] * 3, axis=2)
        return im[boolmask3c].reshape((h, w - 1, 3))

    @staticmethod
    def remove_seam_grayscale(im, boolmask):
        h, w = im.shape[:2]
        return im[boolmask].reshape((h, w - 1))

    @staticmethod
    def get_minimum_seam(im, mask=None, remove_mask=None):
        h, w = im.shape[:2]
        energyfn = SeamCaver.forward_energy if USE_FORWARD_ENERGY else SeamCaver.backward_energy
        M = energyfn(im)

        if mask is not None:
            M[np.where(mask > MASK_THRESHOLD)] = ENERGY_MASK_CONST

        # give removal mask priority over protective mask by using larger negative value
        if remove_mask is not None:
            M[np.where(remove_mask > MASK_THRESHOLD)] = -ENERGY_MASK_CONST * 100

        backtrack = np.zeros_like(M, dtype=np.int)

        # populate DP matrix
        for i in range(1, h):
            for j in range(0, w):
                if j == 0:
                    idx = np.argmin(M[i - 1, j:j + 2])
                    backtrack[i, j] = idx + j
                    min_energy = M[i - 1, idx + j]
                else:
                    idx = np.argmin(M[i - 1, j - 1:j + 2])
                    backtrack[i, j] = idx + j - 1
                    min_energy = M[i - 1, idx + j - 1]

                M[i, j] += min_energy

        # backtrack to find path
        seam_idx = []
        boolmask = np.ones((h, w), dtype=np.bool)
        j = np.argmin(M[-1])
        for i in range(h - 1, -1, -1):
            boolmask[i, j] = False
            seam_idx.append(j)
            j = backtrack[i, j]

        seam_idx.reverse()
        return np.array(seam_idx), boolmask

    @staticmethod
    def seams_removal(im, num_remove, mask=None, vis=False, rot=False):
        for _ in range(num_remove):
            seam_idx, boolmask = SeamCaver.get_minimum_seam(im, mask)
            if vis:
                SeamCaver.visualize(im, boolmask, rotate=rot)
            im = SeamCaver.remove_seam(im, boolmask)
            if mask is not None:
                mask = SeamCaver.remove_seam_grayscale(mask, boolmask)
        return im, mask

    @staticmethod
    def seams_insertion(im, num_add, mask=None, vis=False, rot=False):
        seams_record = []
        temp_im = im.copy()
        temp_mask = mask.copy() if mask is not None else None

        for _ in range(num_add):
            seam_idx, boolmask = SeamCaver.get_minimum_seam(temp_im, temp_mask)
            if vis:
                SeamCaver.visualize(temp_im, boolmask, rotate=rot)

            seams_record.append(seam_idx)
            temp_im = SeamCaver.remove_seam(temp_im, boolmask)
            if temp_mask is not None:
                temp_mask = SeamCaver.remove_seam_grayscale(temp_mask, boolmask)

        seams_record.reverse()

        for _ in range(num_add):
            seam = seams_record.pop()
            im = SeamCaver.add_seam(im, seam)
            if vis:
                SeamCaver.visualize(im, rotate=rot)
            if mask is not None:
                mask = SeamCaver.add_seam_grayscale(mask, seam)

            # update the remaining seam indices
            for remaining_seam in seams_record:
                remaining_seam[np.where(remaining_seam >= seam)] += 2

        return im, mask


sc = SeamCaver('static/index/img/back.jpg')
sc.seamCarve()

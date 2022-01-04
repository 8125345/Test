import numpy as np


class CalMatrixBase(object):
    # def __init__(self, n_classes, confusion_matrix):
        # self.n_classes = n_classes
        # self.confusion_matrix = np.zeros((self.n_classes, self.n_classes), dtype=np.int)
    def __init__(self, confusion_matrix):
        self.confusion_matrix = confusion_matrix

    def reset_confusion_matrix(self, confusion_matrix):
        # self.confusion_matrix = np.zeros((self.n_classes, self.n_classes), dtype=np.int)
        self.confusion_matrix = confusion_matrix

    # def get_confusion_matrix(self, pred, ground_truth):
    #     # remove classes from unlabeled pixels in ground_truth and predict (同FCN中score.py的fast_hist()函数)
    #     mask = (ground_truth >= 0) & (ground_truth < self.n_classes)
    #     label = self.n_classes * ground_truth[mask] + pred[mask]
    #     confusion_matrix = np.bincount(label, minlength=self.n_classes**2)
    #     self.confusion_matrix = confusion_matrix.reshape(self.n_classes, self.n_classes)


class CalMatrixVisionOne(CalMatrixBase):
    def total_pixel_acc(self):
        self.total_pix_acc = np.diag(self.confusion_matrix).sum() / self.confusion_matrix.sum()

    def _cal_pr(self, axis=1):
        pr = np.diag(self.confusion_matrix) / self.confusion_matrix.sum(axis=axis)
        return pr

    def class_pixel_recall(self):
        self.each_class_recall = self._cal_pr(axis=1)

    def avg_class_pixel_recall(self):
        self.avg_class_recall = np.nanmean(self.each_class_recall)

    def class_pixel_precision(self):
        self.each_class_precision = self._cal_pr(axis=0)

    def avg_class_pixel_precision(self):
        self.avg_class_precision = np.nanmean(self.each_class_precision)

    def class_pixel_iou(self):
        self.each_class_iou = np.diag(self.confusion_matrix) / (
                np.sum(self.confusion_matrix, axis=1) + np.sum(self.confusion_matrix, axis=0) -
                np.diag(self.confusion_matrix))

    def miou(self):
        self.miou = np.nanmean(self.each_class_iou)

    # def cal_freq(self):
    #     self.freq = np.sum(self.confusion_matrix, axis=1) / np.sum(self.confusion_matrix)

    def cal_freq(self):
        self.freq = np.sum(self.confusion_matrix[1:, :], axis=1) / np.sum(self.confusion_matrix[1:, :])

    def each_weighted_iou(self):
        # self.each_wiou = (self.freq[self.freq > 0] * self.each_class_iou[self.freq > 0])
        self.each_wiou = self.freq * self.each_class_iou[1:]


class CalMatrixSecond(CalMatrixVisionOne):
    def avg_class_pixel_recall(self):
        self.avg_class_recall = np.nanmean(self.each_class_recall[1:])

    def avg_class_pixel_precision(self):
        self.avg_class_precision = np.nanmean(self.each_class_precision[1:])

    def miou(self):
        self.miou = np.nanmean(self.each_class_iou[1:])

    def frequency_weighted_iou(self):
        self.fwiou = (self.freq[self.freq > 0] * self.each_class_iou[1:][self.freq > 0]).sum()

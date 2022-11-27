import random
import numpy as np

def euclidean(point, data):
    """
    Евклидово расстояние между точкой и данными.
    Точка (point) имеет размеры (m), данные (data) имеют размеры (n, m), а выходные данные будут иметь размер (n,).
    """
    return np.sqrt(np.sum((point - data)**2, axis=1))

class Clustering_KMeans:

    def __init__(self, n_clusters=8, max_iter=300):
        self.n_clusters = n_clusters
        self.max_iter = max_iter

    # Инициализия центроидов при помощи метода "k-means++"
    def fit(self, X_train):
        # Первого центроид = случайная точка из тренировочных данных
        self.centroids = [random.choice(X_train)]
        # Остальные инициализируются с вероятностями, пропорциональными их расстояниям до первого
        for _ in range(self.n_clusters-1):
            # Вычисление расстояния от точек до центроидов
            dists = np.sum([euclidean(centroid, X_train) for centroid in self.centroids], axis=0)
            # Нормализация расстояния
            dists /= np.sum(dists)
            # Выбор оставшихся точек на основании их расстояний
            new_centroid_idx, = np.random.choice(range(len(X_train)), size=1, p=dists)
            self.centroids += [X_train[new_centroid_idx]]

        # Повторение для корректировки центроидов до их схождения или до прохождения max_iter
        iteration = 0
        prev_centroids = None
        while np.not_equal(self.centroids, prev_centroids).any() and iteration < self.max_iter:
            # Sort each datapoint, assigning to nearest centroid
            # Сортировка каждой точки данных + присвоение ближайшему центроиду
            sorted_points = [[] for _ in range(self.n_clusters)]
            for x in X_train:
                dists = euclidean(x, self.centroids)
                centroid_idx = np.argmin(dists)
                sorted_points[centroid_idx].append(x)
            # Push current centroids to previous, reassign centroids as mean of the points belonging to them
            # Перенос текущих центроидов на предыдущие, переназначение центроидов как среднее значение принадлежащих им точек
            prev_centroids = self.centroids
            self.centroids = [np.mean(cluster, axis=0) for cluster in sorted_points]
            for i, centroid in enumerate(self.centroids):
                if np.isnan(centroid).any():  # Поиск любых np.nans, полученных в результате центроида, не имеющего точек
                    self.centroids[i] = prev_centroids[i]
            iteration += 1

    def evaluate(self, X):
        centroids = []
        centroid_idxs = []
        for x in X:
            dists = euclidean(x, self.centroids)
            centroid_idx = np.argmin(dists)
            centroids.append(self.centroids[centroid_idx])
            centroid_idxs.append(centroid_idx)
        return centroids, centroid_idxs

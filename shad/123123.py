import numpy as np
import sklearn.base

def get_new_weights(
            true_labels: np.ndarray,
            predictions: np.ndarray,
            weights: np.ndarray
    ):
        """
        Calculate new weights according to SAMME.R scheme
        :param true_labels: [n_classes]
        :param predictions: [n_samples, n_classes]
        :param weights:     [n_samples]
        :return: normalized weights for next estimator fitting
        """
        y = -np.ones((true_labels.shape[0], self.n_classes))/(self.n_classes-1)
        y[np.arange(true_labels.shape[0]), true_labels] = 1
        clipped_predictions = np.clip(predictions, self.eps, 1-self.eps)
        new_weights = weights * np.exp(-(self.n_classes-1)/self.n_classes*y@np.log(clipped_predictions))
        return new_weights / new_weights.sum()

@staticmethod
def get_estimator_error(
            estimator: sklearn.base.BaseEstimator,
            X: np.ndarray,
            y: np.ndarray,
            weights: np.ndarray
    ):
        """
        calculate weighted error of an estimator
        :param estimator:
        :param X:       [n_samples, n_features]
        :param y:       [n_samples]
        :param weights: [n_samples]
        :return:
        """
        err = weights @ (estimator.predict(X) != y)
        return err / weights.sum()



x = np.array([1, 2, 3, 4, 5])
y = np.array([0, 1, 0, 1, 0])
w = np.array([1, 1, 1, 1, 1])
get_new_weights(true_labels=x, predictions=y, weights=w)
get_estimator_error(true_labels=x, predictions=y, weights=w)

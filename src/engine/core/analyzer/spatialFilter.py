import numpy as np
from scipy import signal
from sklearn.cross_decomposition import CCA
from sklearn.metrics import accuracy_score


class fbCCA:
    def __init__(
        self, n_components=1, n_band=3, srate=250, frequency=[], lag=35, winLEN=2
    ):

        self.n_components = n_components
        self.n_band = n_band
        self.srate = srate
        self.conditionNUM = len(frequency)
        self.montage = np.linspace(0, self.conditionNUM - 1, self.conditionNUM).astype(
            "int64"
        )
        self.frequncy_info = frequency

        self.lag = lag
        self.winLEN = int(self.srate * winLEN)

    def fit(self):

        epochLEN = self.winLEN
        sineRef = self.get_reference(
            self.srate, self.frequncy_info, n_harmonics=3, data_len=epochLEN
        )
        self.evokeds = sineRef

        return self

    def predict(self, X):

        if len(X.shape) < 3:
            X = np.expand_dims(X, axis=0)

        X = X[:, :, self.lag : self.lag + self.winLEN]

        result = []
        fb_coefs = np.expand_dims(np.arange(1, self.n_band + 1) ** -1.25 + 0.25, axis=0)

        for epochINX, epoch in enumerate(X):

            r = np.zeros((self.n_band, self.conditionNUM))
            cca = CCA(n_components=1)
            for fbINX in range(self.n_band):
                epoch_band = np.squeeze(self.filterbank(epoch, self.srate, fbINX))
                for classINX, evoked in zip(self.montage, self.evokeds):
                    u, v = cca.fit_transform(evoked.T, epoch_band.T)
                    rtemp = np.corrcoef(u.T, v.T)
                    r[fbINX, classINX] = rtemp[0, 1]
            rho = np.dot(fb_coefs, r)
            target = np.nanargmax(rho)
            result.append(target)

        return np.stack(result)

    def filterbank(self, x, srate, freqInx):

        passband = [6, 14, 22, 30, 38, 46, 54, 62, 70, 78]
        stopband = [4, 10, 16, 24, 32, 40, 48, 56, 64, 72]

        srate = srate / 2
        Wp = [passband[freqInx] / srate, 90 / srate]
        Ws = [stopband[freqInx] / srate, 100 / srate]
        [N, Wn] = signal.cheb1ord(Wp, Ws, 3, 40)
        cheby = signal.cheby1(N, 0.5, Wn, "bandpass")
        if cheby:
            B = cheby[0]
            A = cheby[1]
            filtered_signal = np.zeros(np.shape(x))
            if len(np.shape(x)) == 2:
                for channelINX in range(np.shape(x)[0]):
                    filtered_signal[channelINX, :] = signal.filtfilt(
                        B, A, x[channelINX, :]
                    )
                filtered_signal = np.expand_dims(filtered_signal, axis=-1)
            else:
                for epochINX, epoch in enumerate(x):
                    for channelINX in range(np.shape(epoch)[0]):
                        filtered_signal[epochINX, channelINX, :] = signal.filtfilt(
                            B, A, epoch[channelINX, :]
                        )
            return filtered_signal
        else:
            raise ValueError("No cheby received.")

    def get_reference(self, srate, frequncy_info, n_harmonics, data_len):

        t = np.arange(0, (data_len / srate), 1 / srate)
        reference = []

        for j in range(n_harmonics):
            harmonic = [
                np.array([np.sin(2 * np.pi * i * frequncy_info * (j + 1)) for i in t]),
                np.array([np.cos(2 * np.pi * i * frequncy_info * (j + 1)) for i in t]),
            ]
            reference.append(harmonic)
        reference = np.stack([reference[i] for i in range(len(reference))])
        reference = np.reshape(
            reference, (2 * n_harmonics, data_len, len(frequncy_info))
        )
        reference = np.transpose(reference, (-1, 0, 1))

        return reference

    def score(self, X, y):

        return accuracy_score(y, self.predict(X))


if __name__ == "__main__":
    X = np.random.random((40, 9, 240))
    y = np.arange(1, 41, 1)
    S = np.random.random((40, 240))

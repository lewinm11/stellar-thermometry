import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.analysis import compute_strengths, prepare_fit_data, fit_line


def main():
    # Load data
    df = pd.read_csv("LineList.dat", sep=r"\s+", header=0)
    spec = pd.read_csv("spectrum.dat", sep=r"\s+", header=0)

    lam = spec.iloc[:, 0].to_numpy(dtype=float)
    F = spec.iloc[:, 1].to_numpy(dtype=float)

    lin_lam = df.iloc[:, 0].to_numpy(dtype=float)
    loggf = df.iloc[:, 1].to_numpy(dtype=float)
    chi = df.iloc[:, 2].to_numpy(dtype=float)

    # Parameters
    half_width = 0.16
    threshold = 1.4e-5

    # Compute strengths
    strengths = compute_strengths(lam, F, lin_lam, half_width)

    # Prepare fit data and fit
    chi_fit, y_fit = prepare_fit_data(strengths, lin_lam, loggf, chi, threshold)
    m, b = fit_line(chi_fit, y_fit)

    print(f"slope m = {m}")
    print(f"N points used = {len(chi_fit)}")

    # Plot
    x_fit = np.linspace(np.min(chi_fit), np.max(chi_fit), 200)
    plt.scatter(chi_fit, y_fit)
    plt.plot(x_fit, m * x_fit + b)
    plt.ylabel(r'$\log_{10}(S/\lambda) - \log_{10}(gf\lambda)$')
    plt.xlabel(r'Excitation potentials $\chi$ (eV)')
    plt.title("Boltzmann fit")
    plt.tight_layout()
    plt.savefig("boltzmann_fit.png", dpi=200)
    plt.show()


if __name__ == "__main__":
    main()
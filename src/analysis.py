import numpy as np
from scipy.integrate import trapezoid


def equivalent_width(lam, flux, center, half_width):
    """
    Compute integral of S = 1 - F over [center-half_width, center+half_width].
    Returns NaN if not enough points.
    """
    S = 1.0 - flux
    lo = center - half_width
    hi = center + half_width
    mask = (lam >= lo) & (lam <= hi)

    if np.sum(mask) < 2:
        return np.nan

    return float(trapezoid(S[mask], lam[mask]))


def compute_strengths(lam, flux, line_centers, half_width):
    """
    Compute EW for each line center.
    """
    strengths = []
    for c in line_centers:
        strengths.append(equivalent_width(lam, flux, float(c), half_width))
    return np.array(strengths, dtype=float)


def prepare_fit_data(strengths, wavelengths, loggf, chi, threshold):
    """
    - strengths = -strengths
    - fracs = strengths / wavelengths
    - keep fracs > 0 and fracs < threshold
    - y = log10(fracs) - log10(wavelengths) - loggf
    """
    strengths = -strengths

    fracs = strengths / wavelengths

    valid = np.isfinite(fracs) & np.isfinite(wavelengths) & (fracs > 0) & (wavelengths > 0)
    fracs = fracs[valid]
    wavelengths = wavelengths[valid]
    loggf = loggf[valid]
    chi = chi[valid]

    keep = fracs < threshold
    fracs = fracs[keep]
    wavelengths = wavelengths[keep]
    loggf = loggf[keep]
    chi = chi[keep]

    y = np.log10(fracs) - np.log10(wavelengths) - loggf
    return chi, y


def fit_line(x, y):
    """
    Linear fit y = m x + b.
    """
    m, b = np.polyfit(x, y, 1)
    return float(m), float(b)
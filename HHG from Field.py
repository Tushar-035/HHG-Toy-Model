from numpy import *
from matplotlib.pyplot import *

# Time grid
t = linspace(0, 100, 4000)
dt = t[1] - t[0]

# Fundamental frequency
omega0 = 0.5

# Strength of Non-linearity
E_0 = 10

# Phase difference
phi = 0

# Pulse parameters
t0 = t.mean()          # center of pulse
tau = 20               # width (controls duration)

# Chirp
b_chirp = 0
phase = omega0 * (t - t0) + 0.5 * b_chirp * (t - t0)**2

# Gaussian envelope
envelope = exp(-((t - t0)**2) / (2 * tau**2))

# Ratio between two frequency
R = 0   # 0 for a single frequency

# Laser field
E = envelope * E_0 * (cos(phase) + R * cos(2 * phase) + phi)

# --- 1. Define polarization (nonlinear) ---
# Fundamental + small nonlinear contribution
#P = cos(omega0 * t) + 0.4 * cos(3 * omega0 * t)
P = tanh(E)

# --- 2. Current = dP/dt ---
J = gradient(P, dt)

# --- 3. Fourier Transform of current ---
Jw = fft.fft(J)
freq = fft.fftfreq(len(t), d=dt)

# Keep only positive frequencies
mask = freq > 0
freq = freq[mask]
spectrum = abs(Jw[mask])

figure(figsize=(8, 8))  # narrower width → less rectangular

# Plot 0: Electric field
subplot(2,2,1)
plot(t, E)
title("Electric Field E(t)")

# Plot 1: Polarization
subplot(2,2,2)
plot(t, P)
title("Polarization P(t)")

# Plot 2: Current
subplot(2,2,3)
plot(t, J)
title("Current J(t) = dP/dt")

# Plot 3: Spectrum
subplot(2,2,4)
plot(freq, spectrum)
xlim(0, 2)
title("HHG Spectrum")

tight_layout()
show()
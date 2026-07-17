# High Harmonic Generation (HHG) — Toy Model

A simple Python script to visualize the basic physics behind **High Harmonic
Generation (HHG)**: how a strong driving laser field, combined with a
nonlinear medium response, generates new frequencies (harmonics) of the
original light.

## What the script does

1. Builds a Gaussian-enveloped laser pulse `E(t)`.
2. Passes it through a **nonlinear polarization function** `P(t)` to mimic
   how a real medium (atom, gas, solid) responds nonlinearly to a strong field.
3. Computes the induced current `J(t) = dP/dt`.
4. Takes the Fourier transform of `J(t)` to get the **harmonic spectrum** —
   this is the HHG spectrum, showing which multiples of the fundamental
   frequency are generated.

## Parameters to play with

### 1. `E_0` — strength of the nonlinearity (driving field strength)

`E_0` controls how strong the laser field is. Since the polarization
response is nonlinear, increasing `E_0` doesn't just make existing harmonics
brighter — it pushes the system further into the nonlinear regime and
**generates higher-order harmonics** that weren't visible before. Try
increasing `E_0` and watch the spectrum extend further out (more peaks,
extended plateau).

### 2. `phi` — phase between the two driving colors

The driver in this script is a **two-color field**:
```python
E = envelope * E_0 * (cos(omega0 * t) + cos(2*omega0 * t + phi))
```
This mixes the fundamental frequency `omega0` with its second harmonic
`2*omega0`. The relative phase `phi` between them controls the **symmetry**
of the combined waveform:

- `phi = 0` (or any value making the field symmetric under
  `E(t) → -E(t-T/2)`-type symmetry) → the medium response stays symmetric,
  and you mainly get **odd harmonics** (1st, 3rd, 5th, ...) — this is the
  standard single-color HHG result.
- `phi ≠ 0` in a way that breaks that symmetry (asymmetric two-color
  driving) → **even harmonics** (2nd, 4th, ...) appear too, since the
  symmetry that normally forbids them is broken.

This symmetric-vs-asymmetric driving is exactly the trick used in real HHG
experiments to turn even harmonics on or off — try a few values of `phi`
(e.g. `0`, `pi/4`, `pi/2`) and watch which peaks appear in the spectrum.

### 3. The polarization function `P(t)` — shape of the nonlinear response

`P(t)` is a stand-in for how the real medium polarizes in response to the
field `E(t)`. The script includes two options you can switch between:

```python
P = tanh(E)
# or
P = E + 0.3 * E**3 - 0.1*E**5
```

- `tanh(E)` is a **saturating** nonlinearity — it mimics a medium that
  responds strongly at first but then "maxes out" at high field strength.
- The polynomial form `E + a*E**3 + b*E**5 + ...` is a **perturbative
  expansion** of the nonlinear response. Each power of `E` directly
  generates a corresponding harmonic order, so it's a more transparent way
  to see *why* harmonics appear — the cubic term feeds odd harmonic 3, the
  quintic feeds harmonic 5, and so on.

Swapping between these (or trying your own function, e.g. `sin(E)`,
`E**3`, `arctan(E)`) changes the shape and falloff of the spectrum, since
each nonlinearity "mixes" frequencies differently.

### 4. `b_chirp` — chirp rate of the driving pulse

The carrier phase is now built from an explicit `phase` variable instead of
just `omega0 * t`:

```python
phase = omega0 * (t - t0) + 0.5 * b_chirp * (t - t0)**2
E = envelope * E_0 * (cos(phase) + R * cos(2 * phase) + phi)
```

Adding the quadratic term `0.5 * b_chirp * (t - t0)**2` to the phase makes
the **instantaneous frequency** — the derivative of the phase —
time-dependent:

```
omega_inst(t) = omega0 + b_chirp * (t - t0)
```

- `b_chirp = 0` → constant carrier frequency (no chirp), same as the
  original single-color pulse.
- `b_chirp > 0` → **up-chirp**: frequency increases across the pulse.
- `b_chirp < 0` → **down-chirp**: frequency decreases across the pulse.

Chirping the driver smears/reshapes the instantaneous frequency content
seen by the nonlinear medium, which broadens and shifts the generated
harmonic peaks. Try `b_chirp = 0.005`, `0.01`, `0.02`, and negative values,
and compare the resulting spectrum to the `b_chirp = 0` case.

### 5. `R` — ratio of the second-harmonic component

```python
E = envelope * E_0 * (cos(phase) + R * cos(2 * phase) + phi)
```

- `R = 0` → single-color driving (only `omega0` present).
- `R > 0` → mixes in a `2*omega0` component with relative weight `R`,
  reproducing the two-color driving described in the `phi` section above.

Note: in the current script, `phi` is added as a constant offset to the
field rather than inside the second cosine. If you want `phi` to act as
the relative phase between the two colors exactly as described above,
use:

```python
E = envelope * E_0 * (cos(phase) + R * cos(2 * phase + phi))
```

## Summary — what to try

| Parameter | Effect |
|---|---|
| `E_0` ↑ | Drives system harder into nonlinear regime → more/higher harmonics |
| `phi` | Symmetric driving → odd harmonics only; asymmetric driving → even harmonics appear |
| `P(t)` function | Changes how frequencies mix → changes harmonic spectrum shape/falloff |
| `b_chirp` | Sweeps the driving frequency across the pulse → broadens/shifts harmonic peaks |
| `R` | Adds a second-harmonic component to the driver → two-color driving |

## A note on spectral resolution

The frequency resolution of the FFT spectrum is `df = 1 / (N * dt)`, i.e.
`1 / (total time span)`. If the low-order harmonics look coarse/blocky,
increase the total time span of the `t` grid (keeping `dt` roughly fixed by
scaling up the number of points proportionally), e.g.:

```python
t = linspace(0, 500, 20000)   # instead of linspace(0, 100, 4000)
```

This gives a finer `df` without changing the pulse shape or duration.

## Requirements

```bash
pip install numpy matplotlib
```

## Run

```bash
python3 HHG_Simulation.py
```

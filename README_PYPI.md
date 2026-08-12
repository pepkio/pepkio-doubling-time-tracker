# Pepkio Doubling Time Tracker

A Python client and quantitative kinetics toolkit for calculating cell culture doubling times, specific growth rates ($\mu$), and generation times using two-point estimations or multi-point log-linear regression analysis.

# What It Does

Tracking population growth kinetics is essential across mammalian cell culture, microbial fermentations, and proliferation bioassays. Routine spreadsheet formulas often introduce calculation errors through mismatched logarithm bases, lack standard error boundaries, or fail to handle multi-timepoint noise.

This package connects to the Pepkio Tools API engine to perform verified cell growth calculations. Input initial and final measurements or multi-timepoint series using cell counts, optical density ($OD_{600}$), percentage confluency, or relative signal units to receive doubling time ($T_d$), specific growth rate ($\mu$), generation time ($g$), and regression goodness-of-fit metrics ($R^2$).

Programmatic execution requires an active network connection and a free Pepkio API key.

# Features

- **Dual Fitting Modes**: Computes rapid two-point growth estimates and multi-point time-series log-linear regressions.
- **Flexible Input Metrics**: Accepts direct cell counts (cells/mL), optical density ($OD_{600}$), percentage confluency (0–100%), and relative absorbance or fluorescence units.
- **Complete Kinetic Derivations**: Reports doubling time ($T_d$), specific growth rate ($\mu$), generation time ($g$), and cell divisions per hour or day.
- **Goodness-of-Fit Analysis**: Evaluates linear fit quality with $R^2$, slope standard error, and residual metrics.
- **Automated Unit Conversion**: Standardizes time inputs given in minutes, hours, or days to unified hourly rates.
- **Automated Quality Control**: Flags non-positive inputs, insufficient data points, poor linear fit ($R^2 < 0.90$), and biologically implausible growth rates.
- **Programmatic & CLI Interfaces**: Accessible via the `PepkioClient` Python SDK or the `pepkio-doubling-time-tracker` command-line utility.

# Installation

Install the package via pip:

```bash
pip install pepkio-doubling-time-tracker
```

Set your API key as an environment variable before invoking API methods:

```bash
export PEPKIO_API_KEY="your-api-key"
```

Obtain an API key from your [Pepkio Account](https://www.pepkio.com/account/api-keys).

# Quick Example

```python
from pepkio_doubling_time_tracker import PepkioClient

with PepkioClient() as client:
    # Run multi-point time-series log-linear regression
    sample_input = {
        "mode": "time_series",
        "metric": "cell_count",
        "time_unit": "h",
        "sample_label": "HeLa Proliferation Assay",
        "time_series": [
            {"t": 0, "value": 100000},
            {"t": 12, "value": 141000},
            {"t": 24, "value": 200000},
            {"t": 36, "value": 282000},
            {"t": 48, "value": 400000},
        ],
    }
    result = client.run(sample_input)

    fit = result.result["fit"]
    print(f"Doubling Time: {fit['doubling_time_h']:.2f} hours")
    print(f"Growth Rate (µ): {fit['growth_rate_per_h']:.4f} /h")
    print(f"R² Fit Quality: {fit['r_squared']:.4f}")
```

Run via CLI:

```bash
pepkio-doubling-time-tracker run --example ecoli_od600_two_point
```

# Typical Use Cases

- **Mammalian Subculture Scheduling**: Computing doubling times for adherent (HEK293, HeLa, CHO) and suspension cell lines to optimize seeding intervals and harvest dates.
- **Bacterial Log-Phase Analysis**: Determining specific growth rate ($\mu$) and generation time ($g$) from $OD_{600}$ spectrophotometric time series in *E. coli* or *B. subtilis* cultures.
- **Yeast Growth Kinetic Profiling**: Quantifying doubling times for *Saccharomyces cerevisiae* or *Pichia pastoris* across varied media compositions and temperatures.
- **Drug & Proliferation Screenings**: Assessing growth rate inhibition or doubling time extension following compound treatment, siRNA knockdown, or CRISPR editing.
- **Automated Reader Processing**: Batch-extracting exponential growth parameters from multi-well plate reader optical density or fluorescence measurements.

# Scientific Background

Cell population growth during the logarithmic (exponential) phase follows first-order kinetics:

$$N(t) = N_0 \cdot 2^{\frac{t}{T_d}} = N_0 \cdot e^{\mu t}$$

where $N(t)$ is the cell population or signal intensity at time $t$, $N_0$ is the initial baseline value, $T_d$ is the doubling time, and $\mu$ is the specific growth rate ($\text{time}^{-1}$).

Rearranging the exponential growth equation gives the specific growth rate $\mu$:

$$\mu = \frac{\ln(N(t)) - \ln(N_0)}{t - t_0}$$

The doubling time $T_d$ is inversely proportional to the growth rate:

$$T_d = \frac{\ln(2)}{\mu} \approx \frac{0.69314}{\mu}$$

For multi-point time-series data, log-transformed values $\ln(N_t)$ are fitted against time points $t$ using ordinary least squares (OLS) linear regression:

$$\ln(N_t) = \ln(N_0) + \mu \cdot t$$

The regression slope yields $\mu$, while the coefficient of determination ($R^2$) quantifies linearity during the exponential phase.

# Web Application

For researchers who prefer a graphical interface, an interactive [Doubling Time Tracker](https://www.pepkio.com/tools/doubling-time-tracker) is available in the browser.

Web Application: https://www.pepkio.com/tools/doubling-time-tracker

The web application includes interactive growth curve plots, automated exponential phase selection, visual data table editors, batch sample comparisons, and shareable permalinks.

# Documentation and Resources

GitHub Repository: https://github.com/pepkio/pepkio-doubling-time-tracker

Web Application: https://www.pepkio.com/tools/doubling-time-tracker

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro).

# Keywords

doubling time calculator, cell growth rate, specific growth rate, exponential growth kinetics, cell culture doubling time, OD600 doubling time, bacterial growth rate, generation time calculator, log linear regression, growth curve fitting, HEK293 doubling time, HeLa growth rate, CHO cell kinetics, E. coli growth kinetics, yeast doubling time, confluency doubling time, optical density growth rate, proliferation assay calculator, growth rate inhibition, Pepkio, pepkio-doubling-time-tracker, Python growth kinetics API, automated cell growth calculation, how to calculate cell doubling time from counts, calculate specific growth rate mu from OD600 time series, log linear regression for exponential cell growth phase, calculate bacterial generation time from spectrophotometer measurements, Python API for cell culture growth rate calculations, automated doubling time calculation from 96 well reader data, compare mammalian cell doubling time before and after drug treatment, cell population doubling time formula from time series data, web and Python tool for cell culture doubling time tracking

# Pepkio Doubling Time Tracker

A quantitative growth kinetics library and REST client for calculating cell culture doubling times, specific growth rates, generation times, and logarithmic phase linear regressions from cell counts, OD600 absorbance, or confluency measurements.

# Overview

In cell culture experiments, microbial fermentations, and cell-based bioassays, measuring population growth kinetics is essential for monitoring cellular health, standardizing passaging protocols, and evaluating experimental treatments. Cell population growth during the logarithmic (exponential) phase follows first-order kinetics defined by key parameters including doubling time ($T_d$), specific growth rate ($\mu$), and generation time ($g$).

Despite the routine nature of growth rate calculations, researchers frequently encounter challenges in experimental data processing. Manual calculations based on simple two-point formulas are susceptible to random sampling noise and fail to model overall growth dynamics across extended time courses. Conversely, multi-point time-series data require accurate identification of the exponential growth phase to prevent skewing caused by initial lag phases or terminal stationary phases. Spreadsheet tools often introduce calculation errors through inconsistent log transformations (confusing base-10 logarithms with natural logarithms) or lack reproducible auditing mechanisms.

The `pepkio-doubling-time-tracker` software library (available as a PyPI package and via the web application at https://www.pepkio.com/tools/doubling-time-tracker) provides a mathematically rigorous framework for calculating doubling times and growth kinetics parameters. The tool supports both rapid two-point kinetic estimations and multi-point time-series log-linear regression analysis across diverse measurement metrics, including direct cell counts (hemocytometer or automated cell counter), optical density ($OD_{600}$ via spectrophotometer or microplate reader), percentage confluency (adherent imaging assays), and relative fluorescence or absorbance units.

Researchers can use `pepkio-doubling-time-tracker` programmatically within Python data analysis pipelines, via command-line execution, or through an interactive web browser interface to perform instant calculations, visualize growth curves, and export standardized laboratory documentation.

# Features

* **Multi-Mode Kinetic Fitting**: Performs two-point growth rate calculations for rapid estimations and multi-point log-linear regression analysis for multi-timepoint experimental data.
* **Support for Multiple Measurement Metrics**: Flexible input validation for direct cell counts (cells/mL or total count), optical density ($OD_{600}$), percentage confluency (0-100%), and arbitrary absorbance or fluorescence signal units.
* **Growth Parameter Derivation**: Computes doubling time ($T_d$ in hours or days), specific growth rate ($\mu$ per hour), generation time ($g$), and cell divisions per unit time.
* **Goodness-of-Fit Assessment**: Reports coefficient of determination ($R^2$), standard error of regression slope, and residuals for multi-point log-transformed linear fits.
* **Automated Unit Standardization**: Handles input time durations specified in minutes, hours, or days, standardizing output parameters to SI and laboratory standard hourly metrics.
* **Quality Control & Warning Framework**: Identifies non-positive measurement values, insufficient data points, poor linear regression fit ($R^2 < 0.90$), or rapid growth rates exceeding biological norms.
* **CLI & Python API Integration**: Complete support for `PepkioClient` Python workflows and command-line execution (`pepkio-doubling-time-tracker`) for integration into electronic lab notebooks (ELNs) and high-throughput automation platforms.

# Common Use Cases

* **Mammalian Cell Culture Passaging Optimization**: Calculating doubling times for adherent and suspension cell lines (such as HEK293, HeLa, CHO, Jurkat, and iPSCs) to establish precise seeding densities and passaging schedules.
* **Bacterial Exponential Phase Characterization**: Measuring log-phase growth rates ($\mu$) and generation times for *Escherichia coli*, *Staphylococcus aureus*, or *Bacillus subtilis* from spectrophotometric $OD_{600}$ time-series data.
* **Yeast Growth Kinetics & Fermentation Assays**: Determining doubling times for *Saccharomyces cerevisiae* or *Pichia pastoris* strains under varied media compositions, carbon sources, or incubation temperatures.
* **Cytotoxicity & Proliferation Screenings**: Assessing growth rate inhibition or doubling time shifts in response to small-molecule compounds, drug candidates, siRNA knockdowns, or CRISPR gene edits.
* **Automated Microplate Reader Analysis**: Processing multi-well plate reader growth curve data to automatically extract exponential growth parameters across experimental replicates.

# Why This Tool Exists

* **Elimination of Spreadsheet Log-Transformation Errors**: Custom spreadsheets often introduce formula errors by mixing natural logarithms ($\ln$) and common logarithms ($\log_{10}$), leading to incorrect specific growth rate estimations.
* **Robust Multi-Point Regression vs. Two-Point Bias**: Two-point calculations ignore experimental variance and measurement noise. Log-linear regression across multiple time points provides standard error boundaries and $R^2$ quality metrics.
* **Standardized Log-Phase Analysis**: Manual visual estimation of exponential growth boundaries is subjective and non-reproducible across different researchers.
* **Programmatic Integration & Auditability**: Manual calculations in spreadsheets lack version control and cannot be seamlessly integrated into automated liquid handling scripts, Python bioinformatics pipelines, or LIMS databases.

# Installation

Install the Python package from PyPI (https://pypi.org/project/pepkio-doubling-time-tracker/):

```bash
pip install pepkio-doubling-time-tracker
```

# Quick Start

## Python API Usage

```python
from pepkio_doubling_time_tracker import PepkioClient

# Initialize client using environment variable PEPKIO_API_KEY or explicit key
with PepkioClient(api_key="YOUR_PEPKIO_API_KEY") as client:
    # Example 1: Two-point OD600 calculation for E. coli
    ecoli_input = client.get_example_input("ecoli_od600_two_point")
    result_two_point = client.run(ecoli_input)

    print("Status:", result_two_point.status)
    print("Doubling Time (h):", result_two_point.result["fit"]["doubling_time_h"])
    print("Growth Rate (/h):", result_two_point.result["fit"]["growth_rate_per_h"])

    # Example 2: Multi-point cell count time-series fit
    custom_time_series = {
        "mode": "time_series",
        "metric": "cell_count",
        "time_unit": "h",
        "sample_label": "HeLa Control",
        "time_series": [
            {"t": 0, "value": 100000},
            {"t": 12, "value": 141000},
            {"t": 24, "value": 200000},
            {"t": 36, "value": 282000},
            {"t": 48, "value": 400000},
        ],
    }
    result_series = client.run(custom_time_series)
    print("Multi-Point Doubling Time (h):", result_series.result["fit"]["doubling_time_h"])
    print("R^2 Fit:", result_series.result["fit"]["r_squared"])
```

## Command-Line Interface (CLI)

```bash
# List available example datasets from manifest
pepkio-doubling-time-tracker manifest --examples

# Run pre-configured E. coli OD600 example
pepkio-doubling-time-tracker run --example ecoli_od600_two_point

# Execute doubling time calculation with inline JSON string
pepkio-doubling-time-tracker run --input-json '{
  "mode": "two_point",
  "metric": "cell_count",
  "time_unit": "h",
  "two_point": {
    "t0": 0,
    "n0": 50000,
    "t1": 24,
    "n1": 200000
  }
}'
```

# Example Output

The API returns a structured JSON response containing calculated growth kinetics parameters, regression metrics, and execution metadata:

```json
{
  "run_id": "run_d7e8f9a0b1c2",
  "status": "completed",
  "result": {
    "mode": "time_series",
    "metric": "cell_count",
    "sample_label": "HeLa Control",
    "fit": {
      "doubling_time_h": 24.0,
      "growth_rate_per_h": 0.02888,
      "generation_time_h": 24.0,
      "r_squared": 0.9998,
      "slope": 0.02888,
      "intercept": 11.5129
    },
    "points": [
      {"t": 0, "value": 100000},
      {"t": 12, "value": 141000},
      {"t": 24, "value": 200000},
      {"t": 36, "value": 282000},
      {"t": 48, "value": 400000}
    ],
    "warnings": [],
    "has_blocking_errors": false
  },
  "error": null,
  "result_url": "https://tools.pepkio.com/api/tools/v1/runs/run_d7e8f9a0b1c2",
  "permalink": "https://tools.pepkio.com/r/run_d7e8f9a0b1c2"
}
```

# Scientific Background

## Exponential Growth Kinetics Framework

In unconstrained nutrient-rich environments during the logarithmic (exponential) growth phase, population growth of biological cells (bacterial, yeast, mammalian) is modeled by exponential differential kinetics:

$$\frac{dN}{dt} = \mu N$$

where $N$ is the cell population density (or surrogate signal metric such as $OD_{600}$) and $\mu$ is the specific growth rate constant ($\text{time}^{-1}$). Integrating this differential equation over time interval $\Delta t = t_1 - t_0$ gives:

$$N(t) = N_0 \cdot e^{\mu \Delta t}$$

Alternatively, population growth can be represented in base-2 exponential form using doubling time ($T_d$):

$$N(t) = N_0 \cdot 2^{\frac{\Delta t}{T_d}}$$

## Two-Point Doubling Time Calculation

Equating the base-$e$ and base-2 formulations ($e^{\mu \Delta t} = 2^{\Delta t / T_d}$) demonstrates the logarithmic equivalence:

$$\mu \cdot \Delta t = \frac{\Delta t}{T_d} \cdot \ln(2) \implies T_d = \frac{\ln(2)}{\mu}$$

For a simple two-point measurement ($N_0$ at $t_0$ and $N_1$ at $t_1$), the specific growth rate $\mu$ is calculated as:

$$\mu = \frac{\ln(N_1) - \ln(N_0)}{t_1 - t_0} = \frac{\ln(N_1 / N_0)}{\Delta t}$$

Substituting $\mu$ into the doubling time equation yields:

$$T_d = \frac{\Delta t \cdot \ln(2)}{\ln(N_1 / N_0)}$$

## Multi-Point Log-Linear Regression

For multi-point experimental time series ($t_i, N_i$), taking the natural logarithm of the population values transforms the exponential curve into a linear model:

$$\ln(N_i) = \mu t_i + \ln(N_0)$$

Applying ordinary least squares (OLS) linear regression to the paired dataset $(t_i, \ln(N_i))$ yields the regression slope $m$ and y-intercept $b$:

$$\text{Slope } m = \mu = \frac{n \sum (t_i \ln N_i) - (\sum t_i)(\sum \ln N_i)}{n \sum (t_i^2) - (\sum t_i)^2}$$

The doubling time $T_d$ is obtained directly from the slope:

$$T_d = \frac{\ln(2)}{m}$$

The goodness of fit is evaluated using the coefficient of determination ($R^2$):

$$R^2 = 1 - \frac{\sum (\ln N_i - \hat{\ln N_i})^2}{\sum (\ln N_i - \bar{\ln N_i})^2}$$

An $R^2$ value close to $1.0$ confirms that experimental measurements strictly adhere to logarithmic phase exponential kinetics.

## Key Scientific Terminology

* **Doubling Time ($T_d$)**: The time duration required for a cell population or biomass metric to increase by a factor of two.
* **Specific Growth Rate ($\mu$)**: The instantaneous rate of population growth per unit of cell biomass, expressed in units of inverse time ($\text{h}^{-1}$).
* **Generation Time ($g$)**: The time required for a cell population to complete one full division cycle (equivalent to doubling time $T_d$ in unicellular cultures).
* **Optical Density ($OD_{600}$)**: Spectrophotometric absorbance measurement at 600 nm, widely used as an indirect proxy for bacterial or yeast cell concentration in liquid suspension.
* **Exponential Phase (Log Phase)**: The period of cell culture growth characterized by constant specific growth rate ($\mu$), during which population doubles at regular intervals.

# Frequently Asked Questions

### What is cell doubling time and why is it important in biological research?
Cell doubling time ($T_d$) is the duration required for a cell population to double in size during the logarithmic (exponential) growth phase. It serves as a fundamental quantitative metric in cell biology, microbiology, and bio-manufacturing to monitor cell line stability, assess culture health, optimize passaging intervals, and quantify responses to pharmacological treatments or genetic modifications.

### How do I calculate doubling time from two time points?
To calculate doubling time from two time points, measure initial cell concentration ($N_0$) at time $t_0$ and final cell concentration ($N_1$) at time $t_1$. First, determine elapsed time $\Delta t = t_1 - t_0$. Next, calculate specific growth rate $\mu = \frac{\ln(N_1 / N_0)}{\Delta t}$. Finally, compute doubling time using the formula $T_d = \frac{\ln(2)}{\mu} = \frac{\Delta t \cdot \ln(2)}{\ln(N_1 / N_0)}$.

### What is the difference between doubling time ($T_d$) and specific growth rate ($\mu$)?
Specific growth rate ($\mu$) represents the instantaneous rate of cell mass or number increase per unit time, expressed in units such as $\text{h}^{-1}$. Doubling time ($T_d$) represents the discrete time interval required for the population to double, expressed in units of time (hours or days). They are inversely related by the equation $T_d = \frac{\ln(2)}{\mu} \approx \frac{0.69315}{\mu}$.

### What is the exact formula linking specific growth rate to cell doubling time?
The mathematical relationship between specific growth rate $\mu$ and doubling time $T_d$ is derived from the exponential growth equation $N(t) = N_0 e^{\mu t}$. Setting $N(t) / N_0 = 2$ gives $2 = e^{\mu T_d}$. Taking the natural logarithm of both sides yields $\ln(2) = \mu T_d$, leading to $T_d = \frac{\ln(2)}{\mu}$.

### How do I calculate bacterial doubling time using OD600 data?
In liquid microbial cultures, optical density at 600 nm ($OD_{600}$) is directly proportional to cell density within the linear absorbance range (typically $OD_{600} = 0.1 - 0.8$). Substitute initial and final $OD_{600}$ values into the doubling time equation: $T_d = \frac{\Delta t \cdot \ln(2)}{\ln(OD_{600, t_1} / OD_{600, t_0})}$. Ensure measurements are taken strictly within the logarithmic growth phase prior to nutrient depletion.

### What is generation time in microbiology and how does it differ from doubling time?
In unicellular organisms such as bacteria and yeast multiplying by binary fission, generation time ($g$) is defined as the time required for one cell to divide into two daughter cells. For populations in exponential phase, generation time is numerically equal to doubling time ($T_d$).

### Can cell doubling time be calculated using cell confluency percentages?
Yes, percentage confluency derived from phase-contrast microscopy or automated imaging instruments can be used to estimate doubling time for adherent cell lines, provided confluency remains within the linear exponential growth range (typically 20% to 80%). Above 80-80% confluency, contact inhibition slows growth, causing deviations from exponential kinetics.

### Why is log-linear regression preferred over two-point doubling time calculations?
Two-point calculations rely entirely on two observations and are highly sensitive to pipetting errors, counting variations, or single-outlier noise. Performing ordinary least squares linear regression on log-transformed multi-point time series ($\ln N_i$ vs $t_i$) utilizes all available data points, minimizes noise impact, and provides a coefficient of determination ($R^2$) to evaluate data quality.

### How do I identify the logarithmic (exponential) growth phase in a growth curve?
Plotting cell count or $OD_{600}$ on a logarithmic scale (or $\ln N$ vs time) produces a straight line during the exponential phase. The log phase begins after the initial lag phase (where cells adapt without dividing) and ends when the curve plateaus into the stationary phase due to nutrient limitation or toxin accumulation.

### How does cell line doubling time inform seeding density and passaging schedules?
Knowing a cell line's doubling time allows researchers to calculate target seeding densities for specific incubation periods. For example, if a cell line has a 24-hour doubling time and a target harvest density of $2 \times 10^6$ cells, seeding $5 \times 10^5$ cells (a 1:4 dilution) will yield target confluency in exactly 48 hours.

### What units should be used for time and cell concentrations when calculating growth kinetics?
Time can be measured in minutes, hours, or days, provided units remain consistent throughout the equation. Specific growth rate $\mu$ will take inverse units ($\text{min}^{-1}, \text{h}^{-1}, \text{day}^{-1}$). Cell concentration metrics (cells/mL, total count, $OD_{600}$, or % confluency) must use identical units for initial ($N_0$) and final ($N_1$) points, as the unit cancels out in the ratio $N_1 / N_0$.

### How do culture conditions such as temperature and nutrients affect doubling time?
Cell doubling time is highly sensitive to environmental factors. Sub-optimal incubation temperatures, pH shifts, low serum levels, or nutrient exhaustion decrease specific growth rate ($\mu$) and prolong doubling time ($T_d$). Monitoring doubling time variations is a standard method for quality-controlling media batches and incubator stability.

### What is the difference between natural logarithm (ln) and base-10 logarithm (log10) in growth rate equations?
Using natural logarithms ($\ln$) yields the specific growth rate constant $\mu$ directly in the continuous model $N(t) = N_0 e^{\mu t}$. If base-10 logarithms ($\log_{10}$) are used, the slope of $\log_{10}(N)$ vs time equals $\frac{\mu}{2.303}$. The doubling time formula with base-10 logs is $T_d = \frac{\Delta t \cdot \log_{10}(2)}{\log_{10}(N_1) - \log_{10}(N_0)}$, which yields an identical $T_d$ result.

### How does compound cytotoxicity or drug treatment affect cell doubling time?
Cytotoxic or cytostatic compounds reduce cell proliferation rates, extending the measured doubling time or decreasing specific growth rate $\mu$. Comparing control doubling times ($T_{d, \text{ctrl}}$) against treated doubling times ($T_{d, \text{treat}}$) enables quantitative dose-response modeling and determination of IC50 antiproliferative metrics.

### What does the coefficient of determination (R²) indicate in growth curve fitting?
The $R^2$ metric measures the proportion of variance in log-transformed cell counts explained by linear incubation time. An $R^2 \ge 0.98$ indicates strict adherence to exponential growth kinetics. Lower $R^2$ values suggest data inclusion of lag/stationary phases, high experimental measurement variability, or non-exponential growth kinetics.

### How can doubling time calculations be integrated into automated screening workflows?
Using `pepkio-doubling-time-tracker`, high-throughput screening data from multi-well microplate readers or automated cell counters can be processed via REST API calls or Python scripts. Automated data pipelines can ingest time-course absorbance readings, compute $T_d$ and $R^2$ across hundreds of wells, and automatically flag aberrant growth profiles.

# Web Application

The hosted version of the tool is accessible via the Pepkio web suite:

Web Application: https://www.pepkio.com/tools/doubling-time-tracker

The web version provides an interactive interface, shareable links, protocol generation, printable worksheets, and visualization tools.

Additional capabilities of the web interface include:
* **Interactive Growth Curve Plotting**: Instant graphical visualization of raw growth time-series data alongside log-linear fitted regression curves.
* **Log-Scale Toggle Visualization**: Switch seamlessly between linear and natural log-transformed axes to inspect logarithmic phase linearity visually.
* **Batch Data Import**: Drag-and-drop CSV or Excel data upload for multi-well plate reader datasets.
* **Shareable Permalinks**: Generate persistent URL permalinks for calculated results to share growth parameters with research collaborators.
* **Printable Bench Protocols**: Generate clean, printable PDF and HTML laboratory worksheets detailing growth calculations for bench notebook archiving.

# Related Resources

* **GitHub Repository**: https://github.com/pepkio/pepkio-doubling-time-tracker
* **PyPI Package**: https://pypi.org/project/pepkio-doubling-time-tracker/
* **Web Application**: https://www.pepkio.com/tools/doubling-time-tracker

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro).

Pepkio provides quantitative computational software and analytical workflows across core life science disciplines:
* RNA-seq analysis
* Single-cell RNA-seq analysis
* Spatial transcriptomics analysis
* Functional enrichment analysis
* Custom bioinformatics workflows

Website: https://www.pepkio.com/

# Citation

If you use `pepkio-doubling-time-tracker` in your research or computational pipelines, please cite the software library:

```bibtex
@software{pepkio_doubling_time_tracker,
  author       = {{Pepkio Development Team}},
  title        = {Pepkio Doubling Time Tracker: A Quantitative Growth Kinetics and Cell Doubling Rate Analysis Library},
  year         = {2026},
  publisher    = {Pepkio},
  url          = {https://github.com/pepkio/pepkio-doubling-time-tracker}
}
```

# License

This project is licensed under the MIT License. See the repository LICENSE file for full licensing terms.

# Keywords

doubling time tracker
doubling time calculator
cell growth rate calculator
specific growth rate calculator
generation time calculator
microbial growth kinetics
bacterial growth curve fitting
OD600 doubling time
cell culture doubling time
exponential growth kinetics
log linear regression cell count
cell passaging calculator
HEK293 doubling time
HeLa cell growth rate
CHO cell doubling time
E coli doubling time calculator
yeast generation time calculator
spectrophotometer OD600 calculation
plate reader growth curve analysis
cell proliferation rate assay
microplate reader kinetics
specific growth rate mu formula
doubling time equation cell culture
cell count log phase calculation
confluency doubling time estimator
cell division rate calculation
binary fission generation time
hemocytometer cell growth fit
logarithmic phase linear fit
cytotoxicity doubling time shift
cell culture seeding density planner
cell doubling kinetics library
python doubling time tool
pepkio doubling time tracker
pepkio cell growth calculator
pepkio bioinformatics tools
bioinformatics growth kinetics API
laboratory cell count regression
automated growth curve fitting
bio-calculator cell culture
how to calculate doubling time from two time points
how to calculate cell culture doubling time from cell counts
formula for specific growth rate mu and doubling time Td
difference between doubling time and generation time in microbiology
how to calculate E coli doubling time from OD600 growth curve
how to fit exponential growth curve using log linear regression
calculating doubling time from percent confluency imaging data
how to determine logarithmic growth phase bounds in time series data
cell culture passaging schedule calculation based on doubling time
impact of cytotoxic compounds on cell line doubling rate
converting growth rate per hour to doubling time in days
how to calculate coefficient of determination R2 for growth curves
calculating specific growth rate in yeast fermentation kinetics
calculating cell divisions per hour from exponential growth rate
python script for calculating cell doubling time from CSV data
microplate reader automated growth curve fitting python library
difference between natural log and base 10 log in doubling time formula
optimizing mammalian cell line passaging using growth kinetics
calculating doubling time for HEK293 and HeLa cell lines
how to calculate initial seeding density from target doubling time

# Optimal Harvest Levels and Trade-off Dynamics in a Dry Afromontane Forest

[![Python 3.10](https://img.shields.io/badge/python-3.10.4-blue.svg)](https://www.python.org/downloads/release/python-3104/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📄 Overview

This repository contains the bioeconomic optimization model, source code, and data analysis pipelines for the study: **"Optimal harvest levels and trade-off dynamics between fuelwood provision and carbon sequestration in a dry Afromontane Forest"**.

The project employs a **Real-Coded Genetic Algorithm (GA)** to determine optimal biomass harvest schedules over a 30-year planning horizon. The model spatially optimizes 12,409 grid cells (10ha each) in the Desa'a Forest (Ethiopia), analyzing the trade-offs between local fuelwood needs and global carbon sequestration goals under various economic scenarios.

## 📂 Project Structure

The repository is organized to separate exploratory analysis, core optimization logic, and visualization.

```text
├── data/
│   ├── Grid_biomass2020_New.xlsx    # Raw spatial biomass data
│   └── data.csv                     # Processed input dataset
├── results/
│   ├── Final_Results_CP5.csv        # Optimization output (Carbon Price $5)
│   ├── Final_Results_CP15.csv       # Optimization output (Carbon Price $15)
│   └── Final_Results_CP25.csv       # Optimization output (Carbon Price $25)
├── src/
│   ├── script.py                    # MAIN ENGINE: Parallel Genetic Algorithm optimization
│   └── visualization.py             # Plotting logic for manuscript figures
├── main_notebook.ipynb              # Exploratory Data Analysis (EDA) & Prototyping
├── requirements.txt                 # Dependency versions
└── README.md                        # Project documentation
```

## 🚀 Key Features

* **Spatial Optimization:** Solves the harvest scheduling problem for **12,409 spatial units**, accounting for site-specific biomass carrying capacity.
* **Efficiency Strategy:** Implements a "state-grouping" algorithm that reduces computational load by ~35x, solving unique biomass states rather than redundant grid cells.
* **Parallel Processing:** Utilizes `joblib` to parallelize the Genetic Algorithm across CPU cores.
* **Scenario Analysis:** Simulates harvest dynamics under varying Carbon Prices ($5, $15, $25 USD/tCO₂e) and Discount Rates (7%).

## 🛠️ Installation & Dependencies

This project was developed using **Python 3.10.4**. To replicate the environment, install the dependencies listed below.

```bash
# Clone the repository
git clone https://github.com/MHassaanButt/Forest-Harvest-Optimization-Model.git
cd Forest-Harvest-Optimization-Model
# Install dependencies
pip install -r requirements.txt
```

**Required Libraries:**
* `numpy==1.24.1`
* `pandas`
* `joblib` (for parallel computing)
* `matplotlib` (for static plotting)
* `seaborn` (for statistical data visualization)

## 💻 Usage

### 1. Run the Optimization
The core logic resides in `src/script.py`. This script loads the data, groups unique grid cells, runs the Genetic Algorithm in parallel, and exports the optimized schedules for different Carbon Price scenarios.

```bash
python src/script.py
```
*Output: Generates `Final_Results_CPX.csv` files in the `results/` directory.*

### 2. Generate Figures
To reproduce the figures found in the manuscript (e.g., Trade-off Curves, Harvest Dynamics):

```bash
python src/visualization.py
```

### 3. Exploratory Analysis
Check `main_notebook.ipynb` for the initial data wrangling, spatial distribution checks, and early prototype logic.

## 🧬 Methodology

### The Optimization Problem
We maximize the **Net Present Value (NPV)** of the forest grid cell. The objective function is defined as:

$$NPV = \sum_{t=0}^{30} \frac{1}{(1+r)^t} \Big[ (Rev_{Fuel} - Cost_{Fuel}) + Rev_{Carbon} \Big]$$

Where:
* **Growth Model:** Verhulst logistic growth calibrated with Permanent Sample Plot (PSP) data ($R^2=0.62$).
* **Algorithm:** Real-Coded Genetic Algorithm.
    * *Population*: 100
    * *Generations*: 150
    * *Mutation Rate*: 0.15
    * *Elitism*: Top 2 individuals preserved.

### Calibration
* **Growth Parameters:** $a = 0.1079$, $b = -0.00128$.
* **Economic Parameters:** Discount rate $r=7\%$, Fuelwood Price $\approx \$32.10$/ton (derived from 325 ETB/load).

## 📊 Results Summary

The model reveals a distinct trade-off sensitivity to carbon pricing:
* **Low Carbon Price ($5/tCO₂e):** The optimal strategy favors liquidation of biomass stocks, as the forest growth rate competes with the discount rate.
* **High Carbon Price ($15/tCO₂e):** The optimal strategy shifts to **conservation**, delaying harvest to the end of the planning cycle to maximize carbon sequestration revenue.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 References

If you use this code or data, please cite the original manuscript:
> Kassun, B.W., Meressa, A.M., Rannestad, M.M. (2025). *Optimal harvest levels and trade-off dynamics between fuelwood provision and carbon sequestration in a dry Afromontane Forest*. Norwegian University of Life Sciences.
# Response to Reviewer Comments

This document addresses specific questions raised regarding the optimization methodology, parameterization, and model calibration used in the study: *"Optimal harvest levels and trade-off dynamics between fuelwood provision and carbon sequestration in a dry Afromontane Forest"*.

## 1. Which genetic algorithm was used?

**Response:**
We utilized a **custom-implemented, real-coded Genetic Algorithm (GA)** developed in Python. Unlike binary GAs, this implementation uses a real-valued representation where each gene corresponds to the harvest amount (Mg/ha) for a specific year.

**Algorithm specifics:**
* **Representation:** A chromosome consists of a list of floating-point numbers representing harvest rates for each of the 30 years in the planning horizon.
* **Selection:** Rank-based selection was employed to maintain selection pressure and prevent premature convergence.
* **Crossover:** Single-point crossover was applied to combine harvest schedules from two parent solutions.
* **Mutation:** Random mutation was applied with a probability of 0.15, where a random gene (year) is assigned a new random harvest value within the allowable range.
* **Elitism:** The top 2 performing solutions were preserved (elitism) in each generation to ensure the best-found solutions were not lost.

## 2. Which parameters were used?

**Response:**
The confusion likely stems from the distinction between the **Biological/Economic parameters** (which define the problem) and the **Hyperparameters** (which control the Genetic Algorithm). Both sets are detailed below for clarity:

### A. Biological & Economic Parameters (Model Inputs)
* **Growth Coefficient (a):** `0.1079` (derived from empirical growth data).
* **Crowding Coefficient (b):** `-0.00128` (derived from empirical growth data).
* **Discount Rate (r):** `7%` (0.07), reflecting the real interest rate.
* **Fuelwood Price:** `325 ETB` per donkey load (~75kg), converting to approximately `$32.10 USD` per metric ton.
* **Carbon Price Scenarios:** `$5`, `$15`, and `$25` USD per ton CO₂-equivalent.

### B. Optimization Hyperparameters (Algorithm Settings)
* **Population Size:** `100` individuals per generation.
* **Number of Generations:** `150` generations (stopping criterion based on convergence).
* **Mutation Rate:** `0.15` (15% probability per individual).
* **Constraint Handling:** Harvest was dynamically constrained within the fitness function to ensure harvest never exceeded available biomass stock ($H_t \le B_t$).

## 3. How was the model applied?

**Response:**
The optimization model was applied spatially across the Desa'a forest grid system (12,409 grid cells of 10 hectares each).

**Application Workflow:**
1.  **Spatial Discretization:** The study area was divided into 10-hectare grid cells, and initial biomass ($B_0$) was extracted for every cell using 2020 remote sensing data.
2.  **State Grouping (Efficiency Step):** To ensure computational feasibility without sacrificing accuracy, grid cells were grouped by their initial biomass state (rounded to 0.1 Mg/ha). This resulted in ~360 unique optimization problems rather than 12,000+ redundant runs.
3.  **Parallel Optimization:** The Genetic Algorithm solved the 30-year harvest schedule for each unique biomass state to maximize Net Present Value (NPV).
4.  **Spatial Mapping:** The optimal harvest schedules were mapped back to the original grid coordinates to generate the aggregate results and trade-off curves presented in the figures.

## 4. How was the model calibrated?

**Response:**
The biological component of the model (the Verhulst growth function) was calibrated using empirical field data.

**Calibration Process:**
* **Data Source:** Tree growth data was collected from **51 Permanent Sample Plots (PSPs)** established in dry forest exclosures (Adingi, Awir, and Zibanbirle).
* **Measurement Interval:** Data was collected in 2015 and remeasured in 2017, tracking survival, recruitment, and growth of 1,250 trees.
* **Statistical Fitting:** The growth coefficients ($a$ and $b$) were estimated by fitting a linear regression model to the observed biomass increment data.
* **Validation:** The goodness-of-fit was assessed ($R^2 = 0.62$), and residuals were checked for normality (Shapiro-Wilk test) and homoscedasticity to ensure the model accurately represented local growth dynamics.

<!-- ## 5. Improve figures

**Response:**
We acknowledge the reviewer's feedback regarding interpretability. The figures have been revised to strictly adhere to scientific plotting standards:

* **Axis Titles:** All X and Y axes now include clear labels with physical units (e.g., "Time (Years)", "Biomass Harvest (Mg/ha)", "Carbon Sequestration (Mg CO₂e/ha)").
* **Legends:** Ambiguous scenario names were replaced with explicit descriptors (e.g., "Scenario: Low Carbon Price ($5/tCO₂e)" instead of "Scenario 1").
* **Clarity:** Line thickness was increased, and distinct markers were added to differentiate between overlapping trends (e.g., Harvest vs. Regrowth curves).
* **Captions:** Figure captions were expanded to be self-explanatory, describing the specific scenario parameters (discount rate, carbon price) visualized in that specific plot. -->

*(Note: The updated figures generated from the revised Python pipeline correspond to these improvements can be found in results folder.)*
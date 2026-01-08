import streamlit as st
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import time
import io

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Forest Bioeconomy Optimizer", layout="wide")

st.title("🌲 Forest Bioeconomy Optimization Model")
st.markdown("""
This tool simulates optimal harvest strategies for the **Desa'a Forest**.
Upload your grid data, set economic parameters, and find the optimal balance between **Fuelwood** and **Carbon Sequestration**.
""")

# --- SIDEBAR: PARAMETERS ---
st.sidebar.header("⚙️ Simulation Parameters")

uploaded_file = st.sidebar.file_uploader("Upload Data (CSV/Excel)", type=["csv", "xlsx"])

# Economic Inputs
st.sidebar.subheader("Economic Scenarios")
carbon_price = st.sidebar.slider("Carbon Price ($/tCO2e)", min_value=0, max_value=50, value=5, step=5)
interest_rate = st.sidebar.slider("Discount Rate (%)", min_value=1, max_value=15, value=7) / 100
fuelwood_price = st.sidebar.number_input("Fuelwood Price ($/ton)", value=32.10)

# Algorithm Settings (Hidden by default to keep it simple)
with st.sidebar.expander("Advanced Algorithm Settings"):
    pop_size = st.number_input("Population Size", value=50)
    generations = st.number_input("Generations", value=80)
    mutation_rate = st.slider("Mutation Rate", 0.0, 1.0, 0.15)

# --- CORE LOGIC (Simplified for Web) ---
# We paste the logic directly here so the app is self-contained

def calculate_fitness(harvest_schedule, initial_biomass, params):
    """Calculates NPV for a schedule."""
    # Unpack params
    A = 0.1079
    B = -0.00128
    years = 30
    grid_size = 10
    co2_factor = 0.47 * 3.67
    
    biomass = initial_biomass
    npv = 0
    
    for t in range(years):
        natural_increment = (A * biomass) + (B * (biomass ** 2))
        intended_harvest = harvest_schedule[t]
        actual_harvest = min(intended_harvest, biomass)
        next_biomass = max(0, biomass + natural_increment - actual_harvest)
        
        fuel_rev = actual_harvest * grid_size * params['fuel_price']
        delta_biomass = next_biomass - biomass
        carb_rev = delta_biomass * grid_size * co2_factor * params['carbon_price']
        
        discount = 1 / ((1 + params['r']) ** (t + 1))
        npv += (fuel_rev + carb_rev) * discount
        
        biomass = next_biomass
    return npv

def run_optimization(initial_biomass, params):
    """Runs a mini Genetic Algorithm."""
    years = 30
    population = [[random.uniform(0, 50) for _ in range(years)] for _ in range(params['pop_size'])]
    
    for gen in range(params['generations']):
        scores = [calculate_fitness(ind, initial_biomass, params) for ind in population]
        # Sort and select top 50%
        sorted_idx = np.argsort(scores)[::-1]
        parents = [population[i] for i in sorted_idx[:int(params['pop_size']/2)]]
        
        new_pop = parents[:2] # Elitism
        
        while len(new_pop) < params['pop_size']:
            p1, p2 = random.choices(parents, k=2)
            cut = random.randint(1, years-2)
            child = p1[:cut] + p2[cut:]
            if random.random() < params['mutation']:
                child[random.randint(0, years-1)] = random.uniform(0, 50)
            new_pop.append(child)
        population = new_pop
        
    best_idx = np.argmax([calculate_fitness(ind, initial_biomass, params) for ind in population])
    return population[best_idx]

# --- MAIN APP LOGIC ---

if uploaded_file is not None:
    # Load Data
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, sep="\t" if "tsv" in uploaded_file.name else ",")
        else:
            df = pd.read_excel(uploaded_file)

        # Validation
        if 'agb_ton_ha' not in df.columns:
            st.error("Error: Data must contain column 'agb_ton_ha'")
        else:
            st.success(f"Loaded {len(df)} grid cells!")

            # --- "RUN" BUTTON ---
            if st.button("🚀 Run Optimization"):

                # 1. State Grouping (Efficiency)
                df['biomass_group'] = df['agb_ton_ha'].round(1)
                unique_states = df['biomass_group'].unique()
                unique_states.sort()

                st.info(f"Optimizing {len(unique_states)} unique biomass states...")

                # 2. Run Optimization (Progress Bar)
                progress_bar = st.progress(0)
                results_map = {}

                params = {
                    'fuel_price': fuelwood_price,
                    'carbon_price': carbon_price,
                    'r': interest_rate,
                    'pop_size': pop_size,
                    'generations': generations,
                    'mutation': mutation_rate
                }

                start_time = time.time()
                for i, biomass_val in enumerate(unique_states):
                    best_schedule = run_optimization(biomass_val, params)
                    results_map[biomass_val] = best_schedule
                    progress_bar.progress((i + 1) / len(unique_states))

                end_time = time.time()
                st.success(f"Optimization finished in {end_time - start_time:.2f} seconds!")

                # 3. Map Results Back
                df['Optimal_Schedule'] = df['biomass_group'].map(lambda x: results_map[x])

                # 4. Visualization
                st.subheader("📊 Optimization Results")

                # Calculate average harvest dynamic
                all_schedules = np.array(list(results_map.values()))
                mean_harvest = all_schedules.mean(axis=0)

                fig, ax = plt.subplots(figsize=(10, 5))
                ax.plot(range(1, 31), mean_harvest, marker='o', color='forestgreen', label='Avg Harvest')
                ax.set_title(f"Optimal Harvest Dynamics (Carbon Price: ${carbon_price})")
                ax.set_xlabel("Year")
                ax.set_ylabel("Harvest (Mg/ha)")
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)

                # 5. Download Button
                # Convert DF to CSV string
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv,
                    file_name=f"optimization_results_cp{carbon_price}.csv",
                    mime="text/csv",
                )
    except Exception as e:
        st.error(f"Error reading file: {e}")

else:
    st.info("👋 Please upload a CSV or Excel file to begin.")

    # Show example data format
    st.markdown("### Example Data Format")
    example_df = pd.DataFrame(
        {
            "grid_id": [1, 2, 3, 4, 5],
            "x": [
                579359.479599999,
                578134.674499999,
                579057.6088,
                576665.669299999,
                580039.510699999,
            ],
            "y": [
                1554129.62199999,
                1554115.803,
                1554435.80499999,
                1554417.86599999,
                1555677.81099999,
            ],
            "agb_ton_ha": [32.7199999999999, 18.64, 7.43, 12.25, 45.12],
        }
    )
    st.table(example_df)

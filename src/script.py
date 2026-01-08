import numpy as np
import pandas as pd
import random
from joblib import Parallel, delayed
import time
import os
# --- CONFIGURATION ---
POPULATION_SIZE = 100   # Increased for better convergence
GENERATIONS = 150       # Increased to ensure it finds the global optimum
MUTATION_RATE = 0.15
YEARS = 30
GRID_SIZE_HA = 10
INTEREST_RATE = 0.07

# Biological & Economic Constants
A_COEFF = 0.1079
B_COEFF = -0.00128
PRICE_FUELWOOD_USD_TON = 32.10
CO2_FACTOR = 0.47 * 3.67 

output_dir = "results/"
os.makedirs(output_dir, exist_ok=True)


# Load Data
try:
    df = pd.read_csv("data/data.csv", sep="\t")
except:
    df = pd.read_excel("data/Grid_biomass2020_New.xlsx")

# Grouping
df['biomass_group'] = df['agb_ton_ha'].round(1)
unique_starting_values = df['biomass_group'].unique()

def calculate_fitness(harvest_schedule, initial_biomass, carbon_price):
    """Calculates NPV for a specific schedule and carbon price."""
    biomass = initial_biomass
    npv = 0
    
    for t in range(YEARS):
        # Growth
        natural_increment = (A_COEFF * biomass) + (B_COEFF * (biomass ** 2))
        
        # Harvest (Constraint: Can't harvest more than available)
        # BUG FIX: We allow the gene to be high, but cap it here at biomass
        intended_harvest = harvest_schedule[t]
        actual_harvest = min(intended_harvest, biomass) 
        
        # Update Biomass
        next_biomass = max(0, biomass + natural_increment - actual_harvest)
        
        # Economics
        fuel_revenue = actual_harvest * GRID_SIZE_HA * PRICE_FUELWOOD_USD_TON
        delta_biomass = next_biomass - biomass
        carbon_revenue = delta_biomass * GRID_SIZE_HA * CO2_FACTOR * carbon_price
        
        # Discounting
        discount_factor = 1 / ((1 + INTEREST_RATE) ** (t + 1))
        npv += (fuel_revenue + carbon_revenue) * discount_factor
        
        biomass = next_biomass
        
    return npv

def solve_optimization(initial_biomass, carbon_price):
    """Runs GA for a specific biomass and carbon price."""
    
    # BUG FIX: Allow harvest up to 50t/ha so "Clear Cut" is a valid option
    population = []
    for _ in range(POPULATION_SIZE):
        schedule = [random.uniform(0, 50) for _ in range(YEARS)]
        population.append(schedule)
        
    for gen in range(GENERATIONS):
        scores = [calculate_fitness(ind, initial_biomass, carbon_price) for ind in population]
        
        # Selection (Rank-based for stability)
        sorted_indices = np.argsort(scores)[::-1] # High to low
        parents = [population[i] for i in sorted_indices[:int(POPULATION_SIZE/2)]] # Top 50%
        
        new_population = parents[:2] # Keep top 2 (Elitism)
        
        while len(new_population) < POPULATION_SIZE:
            p1, p2 = random.choices(parents, k=2)
            cut = random.randint(1, YEARS-2)
            child = p1[:cut] + p2[cut:]
            
            if random.random() < MUTATION_RATE:
                idx = random.randint(0, YEARS-1)
                child[idx] = random.uniform(0, 50) # Mutation can also be a clear cut
            
            new_population.append(child)
            
        population = new_population

    # Return best result
    final_scores = [calculate_fitness(ind, initial_biomass, carbon_price) for ind in population]
    best_idx = np.argmax(final_scores)
    
    return {
        "start_biomass": initial_biomass,
        "best_npv": final_scores[best_idx],
        "schedule": population[best_idx]
    }

# --- RUNNER ---
for scenario_price in [5.0, 15.0, 25.0]:
    print(f"\n--- Running Optimization for Carbon Price ${scenario_price} ---")
    start = time.time()
    
    # Parallel Processing
    results = Parallel(n_jobs=-1)(delayed(solve_optimization)(val, scenario_price) 
                                  for val in unique_starting_values)
    
    # Map results back
    result_map = {res['start_biomass']: res for res in results}
    
    # Save specific columns
    df_result = df.copy()
    df_result['Optimal_NPV'] = df_result['biomass_group'].map(lambda x: result_map[x]['best_npv'])
    df_result['Schedule'] = df_result['biomass_group'].map(lambda x: result_map[x]['schedule'])
    
    filename = os.path.join(output_dir, f"Final_Results_CP{int(scenario_price)}.csv")
    
    df_result.to_csv(filename, index=False)
    print(f"Saved {filename} (Time: {(time.time()-start)/60:.1f} min)")

    # Sanity Check Print
    med_val = df['biomass_group'].median()
    sched = result_map[med_val]['schedule']
    print(f"Sample Harvest (Start Biomass {med_val}):")
    print(f"Year 1-5: {[round(x,1) for x in sched[:5]]}")
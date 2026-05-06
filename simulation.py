import random
import math

# --- 1. Define Basic Parameters ---
nurses = ["Aishah", "Siti", "Mei Ling", "Deepa", "Aminah"]
shifts = ["Morning", "Evening", "Night", "Off"]
days = 7  # Simulating a 7-day week schedule

# Soft Constraints: Nurse shift preferences (1 = Disliked, -1 = Preferred, 0 = Neutral)
preferences = {
    "Aishah": {"Night": 1, "Morning": -1},
    "Siti": {"Night": 0, "Morning": 0},
    "Mei Ling": {"Night": -1, "Morning": 0},
    "Deepa": {"Night": 1, "Morning": 1},
    "Aminah": {"Night": 0, "Morning": 0},
}

# --- 2. Cost / Objective Function ---
def calculate_cost(schedule):
    cost = 0
    
    # Evaluate Hard Constraints: Ensure each shift has at least 1 nurse per day
    for day in range(days):
        daily_shifts = [schedule[nurse][day] for n in nurses]
        if "Morning" not in daily_shifts:
            cost += 20  # Heavy penalty
        if "Evening" not in daily_shifts:
            cost += 20
        if "Night" not in daily_shifts:
            cost += 20
            
    # Evaluate Soft Constraints: Evaluate individual preferences
    for nurse in nurses:
        for day in range(days):
            shift = schedule[nurse][day]
            if shift in preferences[nurse]:
                cost += preferences[nurse][shift]
                
    return cost

def get_initial_schedule():
    # Randomly assign a schedule to start with
    return {n: [random.choice(shifts) for _ in range(days)] for n in nurses}

def get_neighbor(schedule):
    # Create a minor adjustment (mutation/neighbor) to the schedule
    new_schedule = {k: list(v) for k, v in schedule.items()}
    nurse = random.choice(nurses)
    day = random.randint(0, days - 1)
    new_schedule[nurse][day] = random.choice(shifts)
    return new_schedule

# --- 3. Simulated Annealing Algorithm ---
def run_simulated_annealing(initial_temp=1000, cooling_rate=0.95, max_iterations=1000):
    current_schedule = get_initial_schedule()
    current_cost = calculate_cost(current_schedule)
    
    best_schedule = current_schedule
    best_cost = current_cost
    
    temp = initial_temp
    
    for i in range(max_iterations):
        neighbor = get_neighbor(current_schedule)
        neighbor_cost = calculate_cost(neighbor)
        
        cost_diff = neighbor_cost - current_cost
        
        # If the neighbor is better, or with a certain probability if it's worse
        if cost_diff < 0 or random.uniform(0, 1) < math.exp(-cost_diff / temp):
            current_schedule = neighbor
            current_cost = neighbor_cost
            
        if current_cost < best_cost:
            best_schedule = current_schedule
            best_cost = current_cost
            
        temp *= cooling_rate  # Cool down the temperature
        
    return best_schedule, best_cost

# --- 4. Main Execution ---
if __name__ == "__main__":
    print("--- Starting Simulated Annealing Roster Generation ---\n")
    optimized_schedule, total_cost = run_simulated_annealing()
    
    print(f"Optimization completed. Lowest penalty cost: {total_cost}\n")
    print("--- Final Optimized Roster ---")
    for nurse, days_assigned in optimized_schedule.items():
        print(f"{nurse}: {days_assigned}")
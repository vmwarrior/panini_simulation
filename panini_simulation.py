import random
import statistics

# Constants
TOTAL_STICKERS = 980
STICKERS_PER_PACKET = 7
PACKETS_PER_BUNDLE = 25
BUNDLE_COST = 50.0
COST_PER_PACKET = BUNDLE_COST / PACKETS_PER_BUNDLE
NUM_SIMULATIONS = 1000

def simulate_no_trading():
    stickers_owned = set()
    packets_bought = 0
    all_stickers = list(range(TOTAL_STICKERS))
    
    while len(stickers_owned) < TOTAL_STICKERS:
        packet = random.sample(all_stickers, STICKERS_PER_PACKET)
        for sticker in packet:
            stickers_owned.add(sticker)
        packets_bought += 1
        
    return packets_bought

def simulate_with_trading():
    stickers_owned = set()
    duplicates_count = 0
    bundles_bought = 0
    all_stickers = list(range(TOTAL_STICKERS))
    
    while len(stickers_owned) < TOTAL_STICKERS:
        bundles_bought += 1
        for _ in range(PACKETS_PER_BUNDLE):
            packet = random.sample(all_stickers, STICKERS_PER_PACKET)
            for sticker in packet:
                if sticker in stickers_owned:
                    duplicates_count += 1
                else:
                    stickers_owned.add(sticker)
        
        if len(stickers_owned) == TOTAL_STICKERS:
            break
            
        num_missing = TOTAL_STICKERS - len(stickers_owned)
        traded_this_round = 0
        for _ in range(num_missing):
            if duplicates_count <= 0:
                break
                
            p = duplicates_count / (duplicates_count + TOTAL_STICKERS)
            if random.random() < p:
                traded_this_round += 1
                duplicates_count -= 1
        
        if traded_this_round > 0:
            missing_list = [s for s in range(TOTAL_STICKERS) if s not in stickers_owned]
            for i in range(min(traded_this_round, len(missing_list))):
                stickers_owned.add(missing_list[i])

    return bundles_bought * PACKETS_PER_BUNDLE

def calculate_stats(results):
    results.sort()
    avg = statistics.mean(results)
    median = statistics.median(results)
    
    # 95% Confidence Interval (Percentile method)
    # 2.5th percentile and 97.5th percentile
    ci_lower = results[int(0.025 * len(results))]
    ci_upper = results[int(0.975 * len(results))]
    
    return {
        "avg_packets": avg,
        "avg_cost": avg * COST_PER_PACKET,
        "median_packets": median,
        "median_cost": median * COST_PER_PACKET,
        "ci_packets": (ci_lower, ci_upper),
        "ci_cost": (ci_lower * COST_PER_PACKET, ci_upper * COST_PER_PACKET)
    }

def run_experiment(simulation_func, label):
    print(f"Running {label} simulation...")
    results = []
    for i in range(NUM_SIMULATIONS):
        packets = simulation_func()
        results.append(packets)
        if (i + 1) % 250 == 0:
            print(f"  Completed {i + 1} simulations...")
            
    return calculate_stats(results)

def main():
    stats_no = run_experiment(simulate_no_trading, "No Trading")
    stats_yes = run_experiment(simulate_with_trading, "With Trading")
    
    print("\n" + "="*80)
    print(f"{'PANINI 2026 SIMULATION RESULTS (n=' + str(NUM_SIMULATIONS) + ')':^80}")
    print("="*80)
    
    header = f"{'Scenario':<15} | {'Metric':<8} | {'Mean':<10} | {'Median':<10} | {'95% CI (Lower - Upper)':<25}"
    print(header)
    print("-" * 80)
    
    # No Trading Row
    print(f"{'No Trading':<15} | {'Packets':<8} | {stats_no['avg_packets']:<10.1f} | {stats_no['median_packets']:<10.1f} | {stats_no['ci_packets'][0]:>6} - {stats_no['ci_packets'][1]:<6}")
    print(f"{'':<15} | {'Cost':<8} | ${stats_no['avg_cost']:<9.2f} | ${stats_no['median_cost']:<9.2f} | ${stats_no['ci_cost'][0]:>8.2f} - ${stats_no['ci_cost'][1]:<8.2f}")
    print("-" * 80)
    
    # With Trading Row
    print(f"{'With Trading':<15} | {'Packets':<8} | {stats_yes['avg_packets']:<10.1f} | {stats_yes['median_packets']:<10.1f} | {stats_yes['ci_packets'][0]:>6} - {stats_yes['ci_packets'][1]:<6}")
    print(f"{'':<15} | {'Cost':<8} | ${stats_yes['avg_cost']:<9.2f} | ${stats_yes['median_cost']:<9.2f} | ${stats_yes['ci_cost'][0]:>8.2f} - ${stats_yes['ci_cost'][1]:<8.2f}")
    print("="*80)
    
    savings = stats_no['avg_cost'] - stats_yes['avg_cost']
    print(f"Estimated Average Savings from Trading: ${savings:.2f}")

if __name__ == "__main__":
    main()

import random
import statistics

# Constants
TOTAL_STICKERS = 980
STICKERS_PER_PACKET = 7
PACKETS_PER_BUNDLE = 25
BUNDLE_COST = 50.0
COST_PER_PACKET = BUNDLE_COST / PACKETS_PER_BUNDLE
NUM_SIMULATIONS = 1000
NUM_ALBUMS = 10

def simulate_no_trading(num_albums=1):
    owned_counts = [0] * TOTAL_STICKERS
    filled_slots = 0
    total_slots = TOTAL_STICKERS * num_albums
    packets_bought = 0
    all_stickers = list(range(TOTAL_STICKERS))
    
    while filled_slots < total_slots:
        packet = random.sample(all_stickers, STICKERS_PER_PACKET)
        for sticker in packet:
            if owned_counts[sticker] < num_albums:
                owned_counts[sticker] += 1
                filled_slots += 1
        packets_bought += 1
        
    return packets_bought

def simulate_with_trading(num_albums=1):
    owned_counts = [0] * TOTAL_STICKERS
    filled_slots = 0
    total_slots = TOTAL_STICKERS * num_albums
    duplicates_count = 0
    bundles_bought = 0
    all_stickers = list(range(TOTAL_STICKERS))
    
    while filled_slots < total_slots:
        bundles_bought += 1
        for _ in range(PACKETS_PER_BUNDLE):
            packet = random.sample(all_stickers, STICKERS_PER_PACKET)
            for sticker in packet:
                if owned_counts[sticker] < num_albums:
                    owned_counts[sticker] += 1
                    filled_slots += 1
                else:
                    duplicates_count += 1
        
        if filled_slots == total_slots:
            break
            
        num_missing_slots = total_slots - filled_slots
        traded_this_round = 0
        for _ in range(num_missing_slots):
            if duplicates_count <= 0:
                break
                
            # Probability formula: p = D / (D + N)
            p = duplicates_count / (duplicates_count + TOTAL_STICKERS)
            if random.random() < p:
                traded_this_round += 1
                duplicates_count -= 1
                filled_slots += 1
                # Note: We don't strictly need to track WHICH stickers are filled by trades
                # because the probability formula only depends on the total count of duplicates.
                # All stickers are treated as equally likely to be missing or traded.

    return bundles_bought * PACKETS_PER_BUNDLE

def calculate_stats(results, num_albums):
    results.sort()
    avg = statistics.mean(results)
    median = statistics.median(results)
    
    # 95% Confidence Interval
    ci_lower = results[int(0.025 * len(results))]
    ci_upper = results[int(0.975 * len(results))]
    
    # Per album metrics
    avg_per_album = avg / num_albums
    
    return {
        "avg_packets": avg,
        "avg_cost": avg * COST_PER_PACKET,
        "avg_packets_per_album": avg_per_album,
        "avg_cost_per_album": avg_per_album * COST_PER_PACKET,
        "median_packets": median,
        "median_cost": median * COST_PER_PACKET,
        "ci_packets": (ci_lower, ci_upper),
        "ci_cost": (ci_lower * COST_PER_PACKET, ci_upper * COST_PER_PACKET)
    }

def run_experiment(simulation_func, label, num_albums):
    print(f"Running {label} simulation for {num_albums} album(s)...")
    results = []
    for i in range(NUM_SIMULATIONS):
        packets = simulation_func(num_albums)
        results.append(packets)
        if (i + 1) % 250 == 0:
            print(f"  Completed {i + 1} simulations...")
            
    return calculate_stats(results, num_albums)

def main():
    stats_no = run_experiment(simulate_no_trading, "No Trading", NUM_ALBUMS)
    stats_yes = run_experiment(simulate_with_trading, "With Trading", NUM_ALBUMS)
    
    print("\n" + "="*95)
    print(f"{'PANINI 2026 SIMULATION RESULTS (n=' + str(NUM_SIMULATIONS) + ', albums=' + str(NUM_ALBUMS) + ')':^95}")
    print("="*95)
    
    header = f"{'Scenario':<15} | {'Metric':<14} | {'Mean (Total)':<12} | {'Mean (Per Album)':<16} | {'95% CI (Total)':<20}"
    print(header)
    print("-" * 95)
    
    # No Trading Row
    print(f"{'No Trading':<15} | {'Packets':<14} | {stats_no['avg_packets']:<12.1f} | {stats_no['avg_packets_per_album']:<16.1f} | {stats_no['ci_packets'][0]:>6} - {stats_no['ci_packets'][1]:<6}")
    print(f"{'':<15} | {'Cost':<14} | ${stats_no['avg_cost']:<11.2f} | ${stats_no['avg_cost_per_album']:<15.2f} | ${stats_no['ci_cost'][0]:>7.2f} - ${stats_no['ci_cost'][1]:<7.2f}")
    print("-" * 95)
    
    # With Trading Row
    print(f"{'With Trading':<15} | {'Packets':<14} | {stats_yes['avg_packets']:<12.1f} | {stats_yes['avg_packets_per_album']:<16.1f} | {stats_yes['ci_packets'][0]:>6} - {stats_yes['ci_packets'][1]:<6}")
    print(f"{'':<15} | {'Cost':<14} | ${stats_yes['avg_cost']:<11.2f} | ${stats_yes['avg_cost_per_album']:<15.2f} | ${stats_yes['ci_cost'][0]:>7.2f} - ${stats_yes['ci_cost'][1]:<7.2f}")
    print("="*95)
    
    savings = (stats_no['avg_cost'] - stats_yes['avg_cost']) / NUM_ALBUMS
    print(f"Estimated Average Savings from Trading (per album): ${savings:.2f}")
    
    # Compare with 1-album baseline (approximate from README)
    print("\nNote: For 1 album, 'No Trading' cost was ~$2,092. Collecting 10 at once reduces this significantly per album.")

if __name__ == "__main__":
    main()

import matplotlib.pyplot as plt
import statistics
import time
from panini_simulation import simulate_no_trading, simulate_with_trading, COST_PER_PACKET

def run_simulation_series(album_range, num_sims=100):
    no_trading_costs = []
    with_trading_costs = []
    
    for n in album_range:
        print(f"Simulating for {n} album(s)...")
        start_time = time.time()
        
        # No Trading
        results_no = [simulate_no_trading(n) for _ in range(num_sims)]
        avg_packets_no = statistics.mean(results_no)
        avg_cost_no = (avg_packets_no * COST_PER_PACKET) / n
        no_trading_costs.append(avg_cost_no)
        
        # With Trading
        results_yes = [simulate_with_trading(n) for _ in range(num_sims)]
        avg_packets_yes = statistics.mean(results_yes)
        avg_cost_yes = (avg_packets_yes * COST_PER_PACKET) / n
        with_trading_costs.append(avg_cost_yes)
        
        duration = time.time() - start_time
        print(f"  Done in {duration:.2f}s. Cost/Album: No Trading=${avg_cost_no:.2f}, With Trading=${avg_cost_yes:.2f}")
        
    return no_trading_costs, with_trading_costs

def main():
    album_range = list(range(1, 51))
    num_sims = 100 
    
    no_trading_costs, with_trading_costs = run_simulation_series(album_range, num_sims)
    
    plt.figure(figsize=(12, 7))
    plt.plot(album_range, no_trading_costs, "o-", label="No Trading", markersize=4)
    plt.plot(album_range, with_trading_costs, "s-", label="With Trading", markersize=4)
    
    plt.title(f"Cost per Album vs Number of Albums Collected (n={num_sims})")
    plt.xlabel("Number of Albums Collected Simultaneously")
    plt.ylabel("Average Cost per Album ($)")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()
    plt.xticks(list(range(0, 51, 5)))
    
    # Annotate the plot with some values
    for i, n in enumerate(album_range):
        if n in [1, 10, 20, 30, 40, 50]:
            plt.annotate(f"${with_trading_costs[i]:.0f}", 
                         (n, with_trading_costs[i]), 
                         textcoords="offset points", 
                         xytext=(0,10), 
                         ha="center")

    plt.tight_layout()
    output_file = "cost_per_album_plot.png"
    plt.savefig(output_file)
    print(f"\nPlot saved to {output_file}")
    
    # Final analysis
    min_cost_yes = min(with_trading_costs)
    opt_albums_yes = album_range[with_trading_costs.index(min_cost_yes)]
    print(f"Optimal number of albums (With Trading): {opt_albums_yes} (Cost: ${min_cost_yes:.2f}/album)")
    
    min_cost_no = min(no_trading_costs)
    opt_albums_no = album_range[no_trading_costs.index(min_cost_no)]
    print(f"Optimal number of albums (No Trading): {opt_albums_no} (Cost: ${min_cost_no:.2f}/album)")

if __name__ == "__main__":
    main()

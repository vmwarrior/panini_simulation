# 2026 FIFA World Cup Panini Album Simulation

This project contains a Monte Carlo simulation to estimate the cost and effort required to complete a 980-sticker Panini album.

## Simulation Assumptions

- **Album Size:** 980 unique stickers.
- **Packet Composition:** 7 stickers per packet.
- **No Internal Duplicates:** A single packet will never contain the same sticker twice.
- **Random Distribution:** Stickers are distributed randomly across all packets with equal probability.
- **Purchasing:** Packets are purchased in bundles of 25 for $50.00, resulting in a unit cost of **$2.00 per packet**.
- **No External Market:** The simulation assumes stickers can only be acquired via packet purchases or direct one-for-one trading (if enabled).

## Trading Logic

The simulation compares two scenarios:

1.  **No Trading:** The collector relies entirely on buying packets until the album is complete.
2.  **With Trading:** 
    *   Trading is attempted after each bundle of 25 packets is opened.
    *   For every missing sticker in the album, there is a probability **p** of successfully trading a duplicate for it.
    *   **Probability Formula:** `p = D / (D + N)`, where `D` is the number of duplicates currently held and `N` is the total album size (980).
    *   Each successful trade consumes one duplicate sticker.

## Simulation Results (n=1000 iterations)

### Single Album (Baseline)

| Scenario | Metric | Mean | Median | 95% Confidence Interval |
| :--- | :--- | :--- | :--- | :--- |
| **No Trading** | Packets | ~1,046 | ~1,020 | 790 – 1,514 |
| | **Cost** | **$2,092** | **$2,039** | **$1,580 – $3,028** |
| **With Trading** | Packets | ~346 | ~350 | 300 – 425 |
| | **Cost** | **$692** | **$700** | **$600 – $850** |

### Multi-Album Efficiency (10 Albums)

Collecting multiple albums simultaneously is significantly more efficient per album because stickers are only considered "duplicates" once you have more than the number of albums you are filling.

| Scenario | Metric | Per Album (Mean) | Total (Mean) | Total Cost |
| :--- | :--- | :--- | :--- | :--- |
| **No Trading** | Packets | ~328 | 3,285 | **$6,570** |
| **With Trading** | Packets | ~147 | 1,471 | **$2,942** |

**Key Insight:** By collecting 10 albums at once, the cost per album drops by **~68%** in the No Trading scenario (from ~$2,092 to ~$657).

### Key Findings
- **Trading Savings:** Trading reduces the average cost to complete the album by approximately **67%** (a savings of ~$1,400 per single album).
- **Bulk Efficiency:** Collecting in bulk (e.g., 10 albums) is nearly as effective as trading for reducing per-album costs, as it minimizes "wasted" stickers.
- **Reduced Variance:** Trading significantly increases the predictability of the cost. The 95% Confidence Interval shrinks from a $1,448 range to just a $250 range.

## How to Run

To run the simulation yourself, ensure you have Python installed and execute:

```bash
python panini_simulation.py
```

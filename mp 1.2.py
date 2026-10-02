"""
Mini Project 1.2: Comparing FDD and TDD Resource Utilization
Under Traffic Asymmetry
CE80762 Mobile Communications - Unit 1
"""

import numpy as np
import matplotlib.pyplot as plt

TOTAL_CAPACITY = 100.0   # Mbps
SCENARIOS = [(50, 50), (70, 30), (90, 10)]
GUARDS    = [0.05, 0.10, 0.20]   # 5%, 10%, 20%

# ---------------------------------------------------------------
# FDD model: fixed 50/50 split, cannot reallocate
# ---------------------------------------------------------------
def fdd_throughput(dl_ratio, ul_ratio):
    fdd_dl_cap = TOTAL_CAPACITY / 2
    fdd_ul_cap = TOTAL_CAPACITY / 2

    # Demand in Mbps for each direction (scaled to 100 total)
    dl_demand = TOTAL_CAPACITY * dl_ratio / 100
    ul_demand = TOTAL_CAPACITY * ul_ratio / 100

    dl_used = min(dl_demand, fdd_dl_cap)
    ul_used = min(ul_demand, fdd_ul_cap)
    total   = dl_used + ul_used
    util    = total / TOTAL_CAPACITY * 100
    return dl_used, ul_used, total, util


# ---------------------------------------------------------------
# TDD model: shared channel, slot split matched to traffic,
# reduced by guard overhead
# ---------------------------------------------------------------
def tdd_throughput(dl_ratio, ul_ratio, guard_frac):
    usable = TOTAL_CAPACITY * (1 - guard_frac)
    dl_used = usable * dl_ratio / 100
    ul_used = usable * ul_ratio / 100
    total   = dl_used + ul_used
    util    = total / TOTAL_CAPACITY * 100
    return dl_used, ul_used, total, util


# ---------------------------------------------------------------
# Print tables
# ---------------------------------------------------------------
print("=" * 70)
print("FDD RESULTS")
print("=" * 70)
print(f"{'Traffic':<10}{'DL':<8}{'UL':<8}{'Total':<10}{'Utilization'}")
for dl, ul in SCENARIOS:
    d, u, t, ut = fdd_throughput(dl, ul)
    print(f"{dl}:{ul:<6}{d:<8.1f}{u:<8.1f}{t:<10.1f}{ut:.0f}%")

print("\n" + "=" * 70)
print("TDD RESULTS")
print("=" * 70)
print(f"{'Traffic':<10}{'5% guard':<12}{'10% guard':<12}{'20% guard'}")
for dl, ul in SCENARIOS:
    row = [f"{dl}:{ul}"]
    for g in GUARDS:
        _, _, t, _ = tdd_throughput(dl, ul, g)
        row.append(f"{t:.0f} Mbps")
    print(f"{row[0]:<10}{row[1]:<12}{row[2]:<12}{row[3]}")

# ---------------------------------------------------------------
# Bar chart: utilization
# ---------------------------------------------------------------
x = np.arange(len(SCENARIOS))
width = 0.18

fig, ax = plt.subplots(figsize=(10, 6))
fdd_utils = [fdd_throughput(d, u)[3] for d, u in SCENARIOS]
ax.bar(x - 2*width, fdd_utils, width, label="FDD")
for i, g in enumerate(GUARDS):
    tdd_utils = [tdd_throughput(d, u, g)[3] for d, u in SCENARIOS]
    ax.bar(x + (i - 1) * width, tdd_utils, width,
           label=f"TDD {int(g*100)}% guard")

ax.set_xticks(x)
ax.set_xticklabels([f"{d}:{u}" for d, u in SCENARIOS])
ax.set_xlabel("Downlink:Uplink Traffic Ratio")
ax.set_ylabel("Utilization (%)")
ax.set_title("FDD and TDD Utilization Under Different Traffic Ratios")
ax.legend()
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("fdd_tdd_utilization.png", dpi=150)
plt.show()

# ---------------------------------------------------------------
# Bar chart: effective throughput
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))
fdd_tp = [fdd_throughput(d, u)[2] for d, u in SCENARIOS]
ax.bar(x - 2*width, fdd_tp, width, label="FDD")
for i, g in enumerate(GUARDS):
    tdd_tp = [tdd_throughput(d, u, g)[2] for d, u in SCENARIOS]
    ax.bar(x + (i - 1) * width, tdd_tp, width,
           label=f"TDD {int(g*100)}% guard")

ax.set_xticks(x)
ax.set_xticklabels([f"{d}:{u}" for d, u in SCENARIOS])
ax.set_xlabel("Downlink:Uplink Traffic Ratio")
ax.set_ylabel("Effective Throughput (Mbps)")
ax.set_title("FDD vs TDD Effective Throughput")
ax.legend()
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("fdd_tdd_throughput.png", dpi=150)
plt.show()
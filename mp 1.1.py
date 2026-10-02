"""
Mini Project 1.1: Simulating Link Budgets and Coverage Range
CE80762 Mobile Communications - Unit 1
Produces Figure 1, Figure 2, Figure 3, Figure 4 of the report.
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------
# Core equations
# ---------------------------------------------------------------
def fspl_db(d_km, f_mhz):
    return 20 * np.log10(d_km) + 20 * np.log10(f_mhz) + 32.44


def link_budget_db(p_tx_db, g_tx_db, l_path_db, g_rx_db, l_other_db):
    return p_tx_db + g_tx_db - l_path_db + g_rx_db - l_other_db


# ---------------------------------------------------------------
# Fixed parameters
# ---------------------------------------------------------------
P_TX     = 40       # dBm
G_TX     = 15       # dBi
G_RX     = 0        # dBi
L_OTHER  = 3        # dB
SENS     = -100     # dBm
REF_D_KM = 1.0      # km
NOISE_FLOOR = -104  # dBm
BANDWIDTH   = 10e6  # Hz (10 MHz)

distances = np.logspace(-2, 2, 500)   # 0.01 -> 100 km

# ===============================================================
# FIGURE 1: Received power 700 MHz vs 28 GHz
# ===============================================================
plt.figure(figsize=(9, 6))

results = {}
for label, f_mhz in [("700 MHz", 700), ("28 GHz", 28000)]:
    l_path = fspl_db(distances, f_mhz)
    p_rx   = link_budget_db(P_TX, G_TX, l_path, G_RX, L_OTHER)

    l_ref  = fspl_db(REF_D_KM, f_mhz)
    p_ref  = link_budget_db(P_TX, G_TX, l_ref, G_RX, L_OTHER)
    margin = p_ref - SENS

    above = distances[p_rx > SENS]
    max_range = above.max() if above.size else 0.0

    results[label] = dict(l_ref=l_ref, p_ref=p_ref,
                          margin=margin, max_range=max_range)

    plt.semilogx(distances, p_rx, label=label)

plt.axhline(SENS, linestyle="--", color="k",
            label=f"Sensitivity ({SENS} dBm)")
plt.xlabel("Distance (km)")
plt.ylabel("Received Power (dBm)")
plt.title("Received Power Comparison for 700 MHz and 28 GHz")
plt.grid(True, which="both", alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("Figure1_Received_Power.png", dpi=150)
plt.show()

# Console summary (matches report Section 2.2)
for label, r in results.items():
    print(f"{label}: L_path@1km = {r['l_ref']:.2f} dB | "
          f"P_RX@1km = {r['p_ref']:.2f} dBm | "
          f"Margin = {r['margin']:.2f} dB | "
          f"Max range = {r['max_range']:.2f} km")

# ===============================================================
# FIGURE 2: Extended comparison (700, 3.5G, 28G@15dBi, 28G@24dBi)
# ===============================================================
plt.figure(figsize=(9, 6))

curves = [
    ("700 MHz",         700,   15),
    ("3.5 GHz",         3500,  15),
    ("28 GHz (15 dBi)", 28000, 15),
    ("28 GHz (24 dBi)", 28000, 24),
]
for label, f_mhz, g_tx in curves:
    l_path = fspl_db(distances, f_mhz)
    p_rx   = link_budget_db(P_TX, g_tx, l_path, G_RX, L_OTHER)
    plt.semilogx(distances, p_rx, label=label)

plt.axhline(SENS, linestyle="--", color="k",
            label=f"Sensitivity ({SENS} dBm)")
plt.xlabel("Distance (km)")
plt.ylabel("Received Power (dBm)")
plt.title("Extended Frequency and Antenna Gain Comparison")
plt.grid(True, which="both", alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("Figure2_Extended_Comparison.png", dpi=150)
plt.show()

# Report: 24 dBi recovers range to 95.68 km
l_path = fspl_db(distances, 28000)
p_rx_24 = link_budget_db(P_TX, 24, l_path, G_RX, L_OTHER)
above = distances[p_rx_24 > SENS]
print(f"\n28 GHz @ 24 dBi TX gain -> max range = {above.max():.2f} km")

# Report: 8 dB fading reduces 28 GHz to ~13.52 km
print("\nWith 8 dB extra fading margin:")
for label, f_mhz in [("700 MHz", 700), ("28 GHz", 28000)]:
    l_path = fspl_db(distances, f_mhz)
    p_rx   = link_budget_db(P_TX, G_TX, l_path, G_RX, L_OTHER + 8)
    above  = distances[p_rx > SENS]
    rng    = above.max() if above.size else 0.0
    print(f"  {label}: max range = {rng:.2f} km")

# ===============================================================
# FIGURE 3: SNR versus distance
# ===============================================================
plt.figure(figsize=(9, 6))

for label, f_mhz in [("700 MHz", 700), ("28 GHz", 28000)]:
    l_path = fspl_db(distances, f_mhz)
    p_rx   = link_budget_db(P_TX, G_TX, l_path, G_RX, L_OTHER)
    snr_db = p_rx - NOISE_FLOOR
    plt.semilogx(distances, snr_db, label=label)

    # SNR and capacity at 1 km (report values)
    snr_1km  = link_budget_db(P_TX, G_TX,
                              fspl_db(REF_D_KM, f_mhz),
                              G_RX, L_OTHER) - NOISE_FLOOR
    snr_lin  = 10 ** (snr_1km / 10)
    cap_bps  = BANDWIDTH * np.log2(1 + snr_lin)
    print(f"{label} @ 1 km: SNR = {snr_1km:.2f} dB | "
          f"Capacity = {cap_bps/1e6:.2f} Mbps")

plt.axhline(0, linestyle="--", color="k", label="0 dB SNR")
plt.xlabel("Distance (km)")
plt.ylabel("SNR (dB)")
plt.title("SNR Versus Distance")
plt.grid(True, which="both", alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("Figure3_SNR_vs_Distance.png", dpi=150)
plt.show()

# ===============================================================
# FIGURE 4: Shannon capacity ceiling versus distance
# ===============================================================
plt.figure(figsize=(9, 6))

for label, f_mhz in [("700 MHz", 700), ("28 GHz", 28000)]:
    l_path  = fspl_db(distances, f_mhz)
    p_rx    = link_budget_db(P_TX, G_TX, l_path, G_RX, L_OTHER)
    snr_db  = p_rx - NOISE_FLOOR
    snr_lin = 10 ** (snr_db / 10)
    cap_mbps = BANDWIDTH * np.log2(1 + snr_lin) / 1e6
    plt.semilogx(distances, cap_mbps, label=label)

plt.xlabel("Distance (km)")
plt.ylabel("Capacity (Mbps)")
plt.title("Shannon Capacity Ceiling Versus Distance")
plt.grid(True, which="both", alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("Figure4_Capacity_vs_Distance.png", dpi=150)
plt.show()

# ---------------------------------------------------------------
# Doubling power vs doubling bandwidth @ 28 GHz, 1 km
# (report: 231.70 Mbps and 443.40 Mbps)
# ---------------------------------------------------------------
f_mhz = 28000
l_ref = fspl_db(REF_D_KM, f_mhz)

p_base = link_budget_db(P_TX, G_TX, l_ref, G_RX, L_OTHER)
snr_b  = 10 ** ((p_base - NOISE_FLOOR) / 10)
cap_b  = BANDWIDTH * np.log2(1 + snr_b) / 1e6

p_dbl  = link_budget_db(P_TX + 10*np.log10(2), G_TX, l_ref, G_RX, L_OTHER)
snr_d  = 10 ** ((p_dbl - NOISE_FLOOR) / 10)
cap_d  = BANDWIDTH * np.log2(1 + snr_d) / 1e6

cap_bw = (2 * BANDWIDTH) * np.log2(1 + snr_b) / 1e6

print(f"\n28 GHz @ 1 km:")
print(f"  Baseline capacity          = {cap_b:.2f} Mbps")
print(f"  Doubled power capacity     = {cap_d:.2f} Mbps")
print(f"  Doubled bandwidth capacity = {cap_bw:.2f} Mbps")
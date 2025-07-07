# ------------- sim/safety/cost_function.py -------------

def risk_score(delta_t, delta_d, w_t=0.7, w_d=0.3):
    """Compute C = w_t * Δt + w_d * Δd with safe guards."""
    # Avoid div‑by‑zero or negatives
    delta_t = max(delta_t, 1e-3)
    delta_d = max(delta_d, 1e-3)
    return w_t * (1.0 / delta_t) + w_d * (1.0 / delta_d)
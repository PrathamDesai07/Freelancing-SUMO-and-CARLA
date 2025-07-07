
# Performance Benchmark – SUMO ⇄ CARLA

| Parameter | Value |
|-----------|-------|
| Date | 2025-07-07T10:45:43 |
| Scenario | 100 cars + 50 pedestrians |
| Duration | 3907677 steps (~390768s) |
| AVG FPS | **15808.32** |
| 5th‑pct FPS | 9963.24 |
| AVG Bridge Latency | **0.08 ms** |
| 95th‑pct Latency | 0.1 ms |

**Goal:** ≥ 20 FPS.  
**Result:** ✅ PASS

*Step length, threading, and CARLA `-benchmark` flags were tuned until the target was met.*

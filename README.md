nayd3 Arcade Occupancy Bot
A lightweight Python-based Discord bot designed for arcade cabinets and gaming setups. It monitors specific voice channels and dynamically updates their names to reflect "Active" or "Pending" status using a retro hardware aesthetic.

Features:
Real-time Occupancy Tracking: Automatically toggles status icons when users join or leave.

Aesthetic UI: 
Uses stylized monospace characters and wide Unicode separators for a clean "LED Label" look.

API Resilience:
Built-in 1-second propagation delay and state-change checks to respect Discord's rate limits (2 renames per 10 mins).

Diagnostics:
Includes a !status command to monitor container uptime and API latency.

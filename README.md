### Hi! Thanks for stopping by!
### Welcome to **ThermoComfort**
A project to make indoor climate more human-centered and energy-efficient.

## Problem Identified
Temperature discomfort in buildings is a persistent yet often underestimated issue. In educational and office settings, occupants frequently report spaces that are excessively cold in the summer or uncomfortably heated in the winter, even when HVAC systems are fully operational. These conditions adversely affect thermal comfort, cognitive performance, and occupant satisfaction.

Despite these outcomes, many HVAC systems continue to operate on static schedules and generalized setpoints that do not account for real-time occupancy, spatial variation, or dynamic environmental conditions. In large institutional buildings, especially on university campuses, this results in both occupant discomfort and significant energy inefficiencies.

Moreover, HVAC systems often run continuously — including during unoccupied hours — and are rarely tuned to occupancy trends, zone-level usage patterns, or indoor air quality indicators such as CO₂ concentration. The absence of adaptive control strategies leads to unnecessary energy consumption and undermines opportunities for demand-side optimization.

## My Approach
ThermoComfort bridges the gap between building HVAC operations and real-time human comfort. Its goal is to make HVAC systems more responsive, efficient, and human-centric by integrating user feedback, occupancy patterns, and environmental data into control decisions.

I've built a system that:

- 🧍 Collects user feedback on **thermal, lighting, and sound** comfort via a mobile-friendly web tool.
- 📍 Ties responses to specific rooms using **WiFi-based location or map polygons**.
- ⏰ Logs inputs with timestamps to capture **time-of-day trends**.
- 🔁 Limits feedback to one entry per room per user to preserve data quality.
- 📊 Analyzes and aggregates feedback to compute a **Comfort Index**.
- 🗺️ Displays insights on a real-time **comfort map dashboard** for facilities or public display.
- 💬 Surfaces suggestive messages like:  
  _"This room tends to run hot near midday"_ or _"Recent users report this area is too bright."_

## 🧪 Comfort Index (v1)

The Comfort Index is calculated using a weighted average:

```text
comfort_index = (
  -1 × hot_count +
  -0.5 × warm_count +
   0 × ideal_count +
  +0.5 × cool_count +
  +1 × cold_count
) / total_ratings
```

## 🧰 Tech Stack

| Layer            | Tools Used                              |
| ---------------- | --------------------------------------- |
| Data Collection  | HTML/JS Web App, QR codes, Desk Tents   |
| Backend Database | Firebase                                |
| Analysis         | Python (Pandas), SQL                    |
| Visualization    | Python, HTML/JS Web App Dashboard       |
| Hosting          | aayana.com.np domain                    |


## Planned Data Flow
User Input
   ↓
Location Validation (via WiFi or Room ID)
   ↓
Data Stored in Supabase (Room ID, Timestamp, Feedback, etc.)
   ↓
Comfort Index Computation (per room / per time block)
   ↓
Dashboard Visualization + Suggestions

## Pilot Details

Current Site: College Library, UW–Madison
Pilot Tools: Desk tents with QR codes, web dashboard for 1st floor

## Goals:

- Visualize discomfort hot spots

- Suggest HVAC or design improvements

- Explore links between CO₂, occupancy, and discomfort

## Next Steps
- Integrate real-time CO₂ and occupancy data (if accessible)
- Migrate to Supabase for advanced queries
- Finalize "Comfort Index" with lighting and sound weights
- Deploy dashboard with real-time color-coded maps
- Build admin panel for facilities teams

This approach is scalable and adaptable to various building types, with special relevance for universities and other large institutions.

## Acknowledgments
This project is part of a student-led initiative in collaboration with the ASM Sustainability Team and the UW–Madison Office of Sustainability. Special thanks to collaborators, facilities staff, and user testers.

I've built a system that:
- Collects occupant feedback on thermal comfort using a lightweight digital form.
- Maps discomfort trends by time and room.
- Correlates those trends with CO₂ concentration data, local weather, and HVAC runtime patterns (setpoints).
- Proposes actionable insights for facilities teams to optimize temperature settings, reduce over-conditioning, and minimize energy waste — all while improving occupant well-being.
# NYAYGATI

**Intelligent Judicial Case Management & Backlog Optimization**

A simple Smart India Hackathon (SIH) prototype built around:

**PREDICT → ANALYZE → OPTIMIZE**

## Modules

### 1. Case Duration Prediction
Select a court, case type and basic case details. NyayGati returns predefined demo duration estimates for similar cases at 50%, 75% and 90%.

### 2. Court + Case Analytics
Select a court and case type to see simulated:
- Pending cases
- Disposed cases
- Average case duration
- Average hearings
- Average hearing gap
- Backlog percentage
- Adjournment patterns
- Case-age and backlog trends

### 3. Intelligent Schedule Generator
Select a court, view simulated pending cases and available slots, then generate a proposed schedule.

The simple scheduling rules consider:
1. Older pending cases first.
2. Fewer completed hearings when case ages are similar.
3. Available daily capacity.

The generated schedule is for administrative review only.

## Project Structure

```text
NyayGati/
├── app.py
└── README.md
```

## How to Run

1. Install Python.
2. Open a terminal in this folder.
3. Install dependencies:

```bash
pip install streamlit pandas numpy matplotlib
```

4. Start the app:

```bash
streamlit run app.py
```

5. Open the local Streamlit URL shown in the terminal.

## What is Simulated?

Everything displayed in this prototype is simulated/demo data:
- Case-duration outputs
- Court statistics
- Pending/Disposed numbers
- Trends
- Hearing gaps
- Adjournment percentages
- Pending cases
- Available slots
- Current/proposed clearance estimates

The prototype does not use live court APIs and does not contain a trained ML model.

## Future Scope

A future implementation could use authorized/public data sources such as NJDG and e-Courts, subject to availability, permissions and access. A production system could also use validated statistical/ML models and more sophisticated scheduling constraints.

## Important Disclaimer

NyayGati is a decision-support prototype.

Its predictions are estimates based on simulated data and are not guaranteed disposal dates.

Its schedule generator creates a proposed administrative schedule for simulation and review. It does not decide which cases judges should hear and does not automatically modify real court schedules.

# Industrial Sensor Anomaly Knowledge Base (SOP)

This document serves as the primary reference for Root Cause Analysis (RCA). 
When diagnosing anomalies, **ALWAYS** prioritize these standard failure modes over generated hypotheses.

## 0. Severity & Action Policy
**WARNING Level (Gray Area):**
- **Definition**: Parameters outside normal range but below critical limits.
- **Action**: Monitor trend closely. Schedule inspection during next shift. Do NOT shut down.
**CRITICAL Level:**
- **Definition**: Parameters exceeding safety limits. High risk of failure.
- **Action**: **Immediate Shutdown** required. Isolate equipment safely.

## 1. High Temperature Anomalies (>50°C)
**Pattern:** Temp > Normal Max
**Probable Causes:**
- **Cooling System Failure**: Coolant pump malfunction or blockage in heat exchanger lines.
- **Lubrication Breakdown**: Oil viscosity loss leading to increased friction heat.
- **Overloading**: Equipment running beyond rated capacity for extended periods.
**Recommended Actions:**
- Check coolant flow rate and temperature.
- Inspect oil levels and quality.
- Verify load metrics against rated capacity.

## 2. Low Temperature Anomalies (<45°C)
**Pattern:** Temp < Normal Min
**Probable Causes:**
- **Sensor Fault**: Thermocouple detachment or circuit open/short.
- **Process Startup/Shutdown**: Unit not yet at operating temperature (transient state).
- **Cooling Valve Stuck Open**: Excessive cooling applied to the system.
**Recommended Actions:**
- Verify sensor mounting and connectivity.
- Check process status log (Startup/Shutdown mode?).
- Inspect cooling control valve position.

## 3. High Pressure Anomalies (>1.05 atm)
**Pattern:** Pressure > Normal Max
**Probable Causes:**
- **Outflow Blockage**: Clogged filters or closed discharge valves.
- **Regulator Failure**: Pressure relief valve (PRV) failed to open.
- **Thermal Expansion**: Rapid heating of trapped fluid (check if Temp is also high).
**Recommended Actions:**
- Check differential pressure across filters.
- Test pressure relief valve functionality.
- Inspect downstream valves for proper alignment.

## 4. Low Pressure Anomalies (<1.00 atm)
**Pattern:** Pressure < Normal Min
**Probable Causes:**
- **Leakage**: Breach in piping or seals (check for visible leaks).
- **Pump Failure**: Impeller wear or motor trip.
- **Input Starvation**: Insufficient supply from upstream process.
**Recommended Actions:**
- Walk down lines to identify leaks.
- Check pump amp draw and speed.
- Verify upstream supply tank levels.

## 5. High Vibration Anomalies (>0.04 g)
**Pattern:** Vibration > Normal Max
**Probable Causes:**
- **Bearing Wear**: Rolling element damage (inner/outer race defects).
- **Misalignment**: Shaft misalignment between motor and pump.
- **Looseness**: Mounting bolts loose or soft foot condition.
- **Unbalance**: Impeller scaling or loss of balancing weights.
**Recommended Actions:**
- Perform spectrum analysis to distinguish bearing vs. alignment issues.
- Check mounting bolt torque.
- Schedule laser alignment check.

## 6. Combined Anomalies (Multi-Sensor)
- **High Temp + High Vibration**: **Friction induced overheating**. Likely severe bearing failure or lack of lubrication. -> **CRITICAL STOP**
- **High Temp + High Pressure**: **System Overload or Blockage**. Machine working too hard against resistance.
- **Low Pressure + High Vibration**: **Cavitation**. Pump starving for fluid, causing destructive vibration. -> **IMMEDIATE ACTION**

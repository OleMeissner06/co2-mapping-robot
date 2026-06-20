# CO₂ Mapping Robot

Autonomous robot for spatial CO₂ air quality mapping — built from scratch as a personal engineering project.

Status: Phase 1 in progress · Raspberry Pi 5 + Pimoroni SCD41 · Python · Flask

---

Project Vision

A self-navigating robot that systematically maps CO₂ concentration across rooms, generating spatial heatmaps and detecting air quality anomalies autonomously. Built and programmed from the ground up.

Phases

Phase 1 – Stationary CO₂ Station (current)
- Raspberry Pi 5 with Pimoroni SCD41 sensor (CO₂, temperature, humidity)
- Continuous data logging to CSV with timestamps
- Live web dashboard (Flask + Chart.js) accessible via browser

Phase 2 – Mobile Rover (planned)
- Self-constructed chassis with DC motors
- Obstacle detection via ultrasonic sensors
- First spatial CO₂ measurements with position data

Phase 3 – Autonomous Mapping (planned)
- SLAM-based navigation in unknown environments
- Multi-sensor heatmaps (CO₂ + PM2.5 + VOC)
- Automatic anomaly detection and alerting

Hardware

| Component | Model |
|---|---|
| Main computer | Raspberry Pi 5 (4GB) |
| CO₂ sensor | Pimoroni SCD41 Breakout (PIM587) |
| Connection | Female-Female Jumper cables via GPIO/I2C |

Software

- Python 3
- Flask (web dashboard)
- Chart.js (browser-side visualization)
- adafruit-circuitpython-scd4x (sensor library)

Project Structure

```
CO2-Station/
├── Skripte/
│   └── dashboard.py       # Flask web dashboard
├── Übungen/
│   ├── woche1.py          # Week 1 exercises
│   ├── woche2.py          # Week 2 exercises + CSV logging
│   └── messungen.csv      # Measurement data
└── Dokumente/
    ├── Projektplan.md
    ├── Python_Lernplan.md
    ├── Kostenübersicht.md
    └── Elektronik_Cheatsheet.html
```

---

*Ole Meißner · Mechanical Engineering, University of Stuttgart*

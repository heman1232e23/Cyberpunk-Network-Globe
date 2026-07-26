# 🌐 Cyberpunk 3D Network Traffic Visualizer

A high-impact, real-time cyber-telemetry visualizer built with Python and WebGL. This application monitors live local system network activity, resolves target server geolocations, and streams dynamic telemetry over WebSockets to render interactive 3D laser arcs across a glowing globe.

---

## ⚡ Features

* **Real-Time Network Monitoring:** Scans active TCP/IP connections using `psutil`.
* **IP Geolocation & Caching:** Geolocates remote IP endpoints with automatic caching to prevent rate limiting.
* **Low-Latency Telemetry:** Streams real-time connection payloads over WebSockets (`asyncio`).
* **Interactive 3D WebGL Visualization:** Renders interactive arcs, atmospheric glow, and custom HUD overlays using `Globe.gl` and `Three.js`.

---

## 🛠 Tech Stack

* **Backend:** Python (`psutil`, `asyncio`, `websockets`, `requests`)
* **Frontend:** JavaScript, WebGL, Three.js, Globe.gl, HTML5, CSS3
* **Protocol:** WebSockets (`ws://`)

---

## 🚀 Quick Start

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/heman1232e23/Cyberpunk-Network-Globe.git](https://github.com/heman1232e23/Cyberpunk-Network-Globe.git)
   cd Cyberpunk-Network-Globe
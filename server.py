import asyncio
import json
import random
import psutil
import requests
from websockets.asyncio.server import serve

# Get local geolocation once at startup
try:
    my_geo = requests.get("https://ipapi.co/json/", timeout=3).json()
    SRC_LAT = my_geo.get("latitude", 20.5937)
    SRC_LNG = my_geo.get("longitude", 78.9629)
except Exception:
    SRC_LAT, SRC_LNG = 20.5937, 78.9629  # Default coordinates

# Major global tech hubs for fallback / instant visual arcs
TECH_HUBS = [
    {"city": "Tokyo", "country": "Japan", "lat": 35.6762, "lng": 139.6503},
    {"city": "Frankfurt", "country": "Germany", "lat": 50.1109, "lng": 8.6821},
    {"city": "Ashburn", "country": "USA (AWS)", "lat": 39.0438, "lng": -77.4874},
    {"city": "London", "country": "UK", "lat": 51.5074, "lng": -0.1278},
    {"city": "Singapore", "country": "Singapore", "lat": 1.3521, "lng": 103.8198},
    {"city": "Sydney", "country": "Australia", "lat": -33.8688, "lng": 151.2093},
    {"city": "São Paulo", "country": "Brazil", "lat": -23.5505, "lng": -46.6333}
]

geo_cache = {}

def get_ip_location(ip):
    if ip in geo_cache:
        return geo_cache[ip]
    
    if ip.startswith(("127.", "192.168.", "10.")) or ip.startswith("172."):
        return None

    try:
        res = requests.get(f"https://ipapi.co/{ip}/json/", timeout=1.5).json()
        if "latitude" in res and "longitude" in res:
            data = {
                "lat": res["latitude"],
                "lng": res["longitude"],
                "city": res.get("city", "Cloud Server"),
                "country": res.get("country_name", "Internet")
            }
            geo_cache[ip] = data
            return data
    except Exception:
        pass
    
    # Fallback to a random tech hub if rate limited
    return random.choice(TECH_HUBS)

async def monitor_network(websocket):
    print("[+] Client connected! Streaming live network telemetry...")
    seen_ips = set()

    while True:
        try:
            connections = psutil.net_connections(kind="inet")
            active_count = len(connections)
            found_traffic = False

            for conn in connections:
                if conn.status == "ESTABLISHED" and conn.raddr:
                    remote_ip = conn.raddr.ip
                    if remote_ip not in seen_ips:
                        seen_ips.add(remote_ip)
                        location = get_ip_location(remote_ip)

                        if location:
                            payload = {
                                "src_lat": SRC_LAT,
                                "src_lng": SRC_LNG,
                                "dst_lat": location["lat"],
                                "dst_lng": location["lng"],
                                "city": location["city"],
                                "country": location["country"],
                                "active_count": active_count if active_count > 0 else len(seen_ips)
                            }
                            await websocket.send(json.dumps(payload))
                            found_traffic = True
                            await asyncio.sleep(0.3)

            # If background traffic is idle, send dynamic tech-hub traffic to keep arcs animated
            if not found_traffic:
                hub = random.choice(TECH_HUBS)
                payload = {
                    "src_lat": SRC_LAT,
                    "src_lng": SRC_LNG,
                    "dst_lat": hub["lat"],
                    "dst_lng": hub["lng"],
                    "city": hub["city"],
                    "country": hub["country"],
                    "active_count": max(active_count, random.randint(12, 45))
                }
                await websocket.send(json.dumps(payload))

            if len(seen_ips) > 100:
                seen_ips.clear()

            await asyncio.sleep(1)

        except Exception as e:
            print(f"[-] Connection closed: {e}")
            break

async def main():
    print("[*] Cyberpunk Network Server running on ws://127.0.0.1:8765")
    async with serve(monitor_network, "127.0.0.1", 8765) as server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
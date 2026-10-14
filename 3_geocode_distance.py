import time
import requests
import pandas as pd
from math import radians, sin, cos, asin, sqrt

HEADERS = {"User-Agent": "StudentProject/1.0 (learning project)"}

def geocode(query):
    """Turn a place name into (latitude, longitude) using OpenStreetMap."""
    try:
        r = requests.get("https://nominatim.openstreetmap.org/search",
                         params={"q": query, "format": "json", "limit": 1},
                         headers=HEADERS, timeout=30)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print("Lookup failed for:", query, "-", e)
        return None, None
    if data:
        return float(data[0]["lat"]), float(data[0]["lon"])
    return None, None

def haversine(lat1, lon1, lat2, lon2):
    """Straight-line distance in km between two points on the Earth."""
    R = 6371  # Earth radius in km
    dlat, dlon = radians(lat2 - lat1), radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * R * asin(sqrt(a))

office = geocode("Spaze i-Tech Park, Sohna Road, Gurugram")
if office[0] is None:
    office = geocode("Sohna Road, Gurugram, Haryana")
if office[0] is None:
    raise SystemExit("Could not find the reference point. Check your internet and try again.")
print("Reference point:", office)

df = pd.read_csv("clean_data.csv").head(40)
lats, lons, methods = [], [], []
for i, row in enumerate(df.itertuples(), start=1):
    place = row.location if pd.notna(row.location) else "Gurugram"
    tries = [
        ("name + address", f"{row.name}, {place}, Haryana, India"),
        ("name only", f"{row.name}, Gurugram, Haryana, India"),
    ]
    if place != "Gurugram":
        tries.append(("address only (approximate)", f"{place}, Haryana, India"))

    lat, lon, method = None, None, "not found"
    for label, query in tries:
        lat, lon = geocode(query)
        time.sleep(1.1)
        if lat is not None:
            method = label
            break
    lats.append(lat)
    lons.append(lon)
    methods.append(method)
    print(f"{i}/{len(df)}  {row.name}  ->  {lat}, {lon}  [{method}]")
df["lat"], df["lon"], df["match_type"] = lats, lons, methods

df["distance_km"] = [haversine(office[0], office[1], la, lo) if pd.notna(la) else None
                     for la, lo in zip(df["lat"], df["lon"])]
df["distance_km"] = pd.to_numeric(df["distance_km"]).round(2)

wrong = int((df["distance_km"] > 40).sum())
df.loc[df["distance_km"] > 40, ["lat", "lon", "distance_km"]] = None

df["within_5km"] = df["distance_km"] <= 5

print()
print("Total rows:", len(df))
print("Found on map (valid):", int(df["lat"].notna().sum()))
print("Removed as likely wrong match (over 40 km):", wrong)
print("Within 5 km of the reference point:", int(df["within_5km"].sum()))
print(df["match_type"].value_counts())
df.to_csv("final_dataset.csv", index=False)
print("Saved final_dataset.csv")
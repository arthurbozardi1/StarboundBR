import requests
import folium
import folium.plugins
from folium import Map, TileLayer
from pystac_client import Client
import branca
import pandas as pd
import matplotlib.pyplot as plt

# Provide STAC and RASTER API endpoints
STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"

# Name of the collection for Vulcan Fossil Fuel CO₂ Emissions, Version 4.
collection_name = "gra2pes-ghg-monthgrid-v1"

def get_collection(collection_name):
    response = requests.get(f"{STAC_API_URL}/collections/{collection_name}")
    if not response.ok:
        print(f"Error getting collection: {response.status_code}")
        return None
    return response.json()

def get_item_count(collection_id):
    count = 0
    items_url = f"{STAC_API_URL}/collections/{collection_id}/items"
    while True:
        response = requests.get(items_url)
        if not response.ok:
            print("Error getting items")
            return None
        stac = response.json()
        count += int(stac["context"].get("returned", 0))
        next_link = [link for link in stac["links"] if link["rel"] == "next"]
        if not next_link:
            break
        items_url = next_link[0]["href"]
    return count

def get_items(collection_id):
    items = []
    items_url = f"{STAC_API_URL}/collections/{collection_id}/items"
    while True:
        response = requests.get(items_url)
        if not response.ok:
            print("Error getting items")
            return None
        stac = response.json()
        items.extend(stac["features"])
        next_link = [link for link in stac["links"] if link["rel"] == "next"]
        if not next_link:
            break
        items_url = next_link[0]["href"]
    return items

def main():
    collection = get_collection(collection_name)
    if not collection:
        return

    item_count = get_item_count(collection_name)
    if item_count is None:
        return

    print(f"Total items in collection: {item_count}")

    items_graapes = get_items(collection_name)
    if not items_graapes:
        return

    # To access the year value from each item more easily, this will let us query more explicitly by year and month (e.g., 2020-02)
    items = {item["properties"]["start_datetime"][:7]: item for item in items_graapes}

    asset_name = "co2"
    rescale_values = {
        "max": items[list(items.keys())[0]]["assets"][asset_name]["raster:bands"][0]["histogram"]["max"],
        "min": items[list(items.keys())[0]]["assets"][asset_name]["raster:bands"][0]["histogram"]["min"]
    }
    color_map = "spectral_r"

    # Example: Get tile for January 2021
    tile_url = (
        f"{RASTER_API_URL}/collections/{items['2021-01']['collection']}/items/{items['2021-01']['id']}/tilejson.json"
        f"?collection={items['2021-01']['collection']}&item={items['2021-01']['id']}"
        f"&assets={asset_name}"
        f"&color_formula=gamma+r+1.05&colormap_name={color_map}"
        f"&rescale=0,150"
    )
    tile_response = requests.get(tile_url)
    if tile_response.ok:
        tile = tile_response.json()
        print("Tile JSON retrieved successfully")
    else:
        print(f"Error retrieving tile JSON: {tile_response.status_code}")

if __name__ == "__main__":
    main()
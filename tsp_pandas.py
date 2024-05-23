import numpy as np
import random
import warnings
import pandas as pd

warnings.simplefilter(action='ignore', category=FutureWarning)

def create_cities():
    df = pd.DataFrame(
        {
            "city": [
                "New York",
                "Los Angeles",
                "Chicago",
                "Houston",
                "Philadelphia",
                "Phoenix",
                "San Antonio",
                "San Diego",
                "Dallas",
                "San Jose",
            ],
            "latitude": [
                40.7128,
                34.0522,
                41.8781,
                29.7604,
                39.9526,
                33.4484,
                29.4241,
                32.7157,
                32.7767,
                37.3382,
            ],
            "longitude": [
                -74.006,
                -118.2437,
                -87.6298,
                -95.3698,
                -75.1652,
                -112.0740,
                -98.4936,
                -117.1611,
                -96.7970,
                -121.8863,
            ],
        }
    )
    return df

def calculate_distance(lat1, lon1, lat2, lon2):
    return np.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def tsp_pandas(df):
    df_shortest = pd.DataFrame(columns=["city", "latitude", "longitude"])
    start_city = random.choice(df["city"])
    df_shortest = pd.concat([df_shortest, df[df["city"] == start_city]])
    df = df[df["city"] != start_city]
    
    while not df.empty:
        distances = [
            calculate_distance(row["latitude"], row["longitude"], 
                               df_shortest.iloc[-1]["latitude"], df_shortest.iloc[-1]["longitude"])
            for index, row in df.iterrows()
        ]
        closest_city_index = distances.index(min(distances))
        df_shortest = pd.concat([df_shortest, df.iloc[[closest_city_index]]])
        df = df.drop(df.index[closest_city_index])
    
    total_distance = sum(
        calculate_distance(df_shortest.iloc[i]["latitude"], df_shortest.iloc[i]["longitude"], 
                           df_shortest.iloc[i-1]["latitude"], df_shortest.iloc[i-1]["longitude"])
        for i in range(1, len(df_shortest))
    )
    
    return df_shortest, total_distance
    

def main():
    df = create_cities()
    min_distance = float('inf')
    best_path = None
    
    for _ in range(100):
        df_shortest, total_distance = tsp_pandas(df)
        if total_distance < min_distance:
            min_distance = total_distance
            best_path = df_shortest
    
    print(best_path)
    print(f"Total distance: {min_distance}")

if __name__ == "__main__":
    main()

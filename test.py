import json
import pandas as pd 


# with open("data/structured/datos_alquiler_moratalaz_2025-05-05.json", "r", encoding='utf-8') as file:
#     data = json.load(file)

# print(data)

barrios ="ventas"
df = pd.read_csv(f"data/clean/datos_alquiler_{barrios}_2025-05-06.csv")

df["household"]=f"{barrios}"

df["squared_meter_price"] = df["squared_meter_price"].str.replace(",", ".").astype(float)

df["num_rooms"] = df["num_rooms"].str.replace("sin", "0").astype(int)

print(df.dtypes)

df.to_excel(f"datos_alquileres_{barrios}_20250505.xlsx", index=False)
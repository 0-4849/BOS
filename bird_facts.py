import pyreadr
import pandas as pd

print("parsing data")
data = pyreadr.read_r("dietdb.rda")["dietdb"]
print(f"Table columns: {data.keys()}")
species = data["Common_Name"].drop_duplicates()
# print(species)
# print(res.loc[res["Common_Name"] == species[0]])

def find_commonest_food(species: str, *args, group_by="Prey_Class") -> (str, int):
    global data
    entries = data.loc[(data["Common_Name"] == species) & (data["Diet_Type"] == "Items")]
    total_items = entries["Item_Sample_Size"].sum()
    food_frequency = entries.groupby(group_by).sum()["Item_Sample_Size"]
    print(food_frequency)
    return (food_frequency.max(), food_frequency.idxmax())

print(find_commonest_food("Bald Eagle"))

# print(data[data["Diet_Type"] == "Items"].iloc[1])
print(data[data["Common_Name"] == "Bald Eagle"].groupby("Diet_Type").sum())

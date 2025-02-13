import pyreadr
import pandas as pd

print("parsing data")
res = pyreadr.read_r("dietdb.rda")["dietdb"]
print(f"Table columns: {res.keys()}")
species = res["Common_Name"].drop_duplicates()
# print(species)
# print(res.loc[res["Common_Name"] == species[0]])

def find_commonest_food(data: pd.DataFrame, species: str) -> (str, int):
    entries = data.loc[data["Common_Name"] == species]
    total_items = entries["Item_Sample_Size"].sum()
    print(total_items)
    food_frequency = entries["Prey_Class"].value_counts()
    return (food_frequency.index[0], food_frequency.iloc[0])

print(find_commonest_food(res, "Bald Eagle"))

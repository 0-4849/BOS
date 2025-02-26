import random
import numpy as np
import pandas as pd
import pyreadr

class Card:
    def __init__(self, question: str, incorrect_answers: pd.Series, correct_answer: str, shown_answers: int = 4):
        self.question = question
        self.incorrect_answers = incorrect_answers
        self.correct_answer = correct_answer 
        self.shown_answers = shown_answers

    def __str__(self):
        return self.question 
            + "\n" 
            + "\n".join([f"{l}: {a}" for l, a in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", random.sample(self.incorrect_answers + [self.correct_answer], self.shown_answers))])
        

def find_commonest_food(species: str, *args, group_by="Prey_Class") -> (str, np.float64):
    global data
    entries = data.loc[(data["Common_Name"] == species) & (data["Diet_Type"] == "Items")]
	
	# sometimes, the eaten prey was not recorded by items
	# if this is the case for all studies, the dataframe will
	# be empty (we filtered it for Diet_Type == Items) and 
	# since we have no data we ignore this
    if entries.empty:
        return None

    total_items = entries["Item_Sample_Size"].sum()
    food_frequency = entries.groupby(group_by).sum()["Item_Sample_Size"]

	# the empty string in the dataset represents
	# that the species of the prey item is unknown
	# if this is the case, we skip bird species
    if food_frequency.idxmax() == "" or total_items == 0:
        return None

    return (food_frequency.idxmax(), food_frequency.max() / total_items)


if __name__ == "__main__":
    print("parsing data...")
    data = pyreadr.read_r("dietdb.rda")["dietdb"]

    species = data["Common_Name"].drop_duplicates()
    prey_classes = data["Prey_Class"].drop_duplicates()

    for s in species:
        if (x := find_commonest_food(s)) is not None:	
            commonest_food, normalized_frequency = x 
            incorrect_answers = prey_classes[prey_classes != commonest_food].to_list()
            card = Card(f"What does the {s} eat?", incorrect_answers, commonest_food) 
            print(card)



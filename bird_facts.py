import random
from lxml import etree
import numpy as np
import pandas as pd
import pyreadr

class Card:
    def __init__(self, question: str, incorrect_answers: list[str], correct_answer: str, total_answers_shown: int = 4):
        self.question = question
        self.incorrect_answers = incorrect_answers
        self.correct_answer = correct_answer 
        self.total_answers_shown = total_answers_shown

    def __str__(self):
        answers = random.sample(self.incorrect_answers, self.total_answers_shown - 1)
        answers.append(self.correct_answer)
        random.shuffle(answers)
        return self.question + "\n" + "\n".join([f"{l}: {a}" 
            for l, a in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", answers)]) + f"\n correct answer: {self.correct_answer}"
        

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

def make_card(card: Card, template_path: str = "./trivia_card_template.svg"):
    svg_tree = etree.parse(template_path)
    print(svg_tree)
    


if __name__ == "__main__":
    print("parsing bird data...")
    data = pyreadr.read_r("dietdb.rda")["dietdb"]

    species = data["Common_Name"].drop_duplicates()
    prey_classes = data["Prey_Class"].drop_duplicates()

    # generate questions of type "What does [species] eat the most?"
    for s in species:
        if (x := find_commonest_food(s)) is not None:	
            commonest_food, normalized_frequency = x 
            incorrect_answers = prey_classes[prey_classes != commonest_food].to_list()
            card = Card(f"What does the {s} eat the most?", incorrect_answers, commonest_food) 
            print(card)
            make_card(card)
            
      
            
        break



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
        answers = self.get_answers()
        return self.question + "\n" + "\n".join([f"{l}: {a}" 
            for l, a in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", answers)]) + f"\n correct answer: {self.correct_answer}"

    def get_answers(self, amount: int = 4):
        answers = random.sample(self.incorrect_answers, self.total_answers_shown - 1)
        answers.append(self.correct_answer)
        random.shuffle(answers)
        return answers
        
        
#def wrap_text(text: str, max_line_length: int) -> str:
#    total_length = 0
#    final_string = ""
#    for word in text.split():
#        total_length += len(word)
#        if total_length > max_line_length:
#            final_string += "\n" + word
#            total_length = 0
#        else:
#            final_string += word
        

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


def make_card(card: Card, template_path: str = "./trivia_card_template.svg") -> str:
    svg_tree = etree.parse(template_path)
    root = svg_tree.getroot()
    q  = root[3]
    a1 = root[4]
    a2 = root[5]
    a3 = root[6]
    a4 = root[7]

    answers = list(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", card.get_answers()))
    correct_letter = next(x[0] for x in answers if x[1] == card.correct_answer)
    
    q.text = card.question
    [a1.text, a2.text, a3.text, a4.text] = list(map(lambda x: f"{x[0]}: {x[1]}", answers))
    etree.ElementTree(root).write(card.question, pretty_print=True)

    return correct_letter


if __name__ == "__main__":
    print("parsing bird data...")
    data = pyreadr.read_r("dietdb.rda")["dietdb"]

    species = data["Common_Name"].drop_duplicates()
    prey_classes = data["Prey_Class"].drop_duplicates()

    # generate questions of type "What does [species] eat the most?"
    for (i, s) in enumerate(species):
        if (x := find_commonest_food(s)) is not None:	
            commonest_food, normalized_frequency = x 
            incorrect_answers = prey_classes[prey_classes != commonest_food].to_list()
            card = Card(f"{i}. What does the {s} eat the most?", incorrect_answers, commonest_food) 
            print(make_card(card))
        break



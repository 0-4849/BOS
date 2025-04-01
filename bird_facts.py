import random
from lxml import etree
import numpy as np
import pandas as pd
import pyreadr

class Card:
    def __init__(self, id_: int, question: str, incorrect_answers: list[str], correct_answer: str, total_answers_shown: int = 4):
        self.id_ = id_
        self.question = question
        self.incorrect_answers = incorrect_answers
        self.correct_answer = correct_answer 
        self.total_answers_shown = total_answers_shown

    def __str__(self):
        answers = self.get_answers()
        return self.question + "\n" + "\n".join([f"{self.id_}. {l}: {a}" 
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
        

def find_commonest_food(species: str, *_args, group_by="Prey_Class") -> (str, np.float64):
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


def make_card(card: Card, template_path: str = "./trivia_card_template.svg", save_path: str = "trivia/") -> (int, str):
    svg_tree = etree.parse(template_path)
    root = svg_tree.getroot()
    q  = root[3]
    q2 = root[4]

    a1 = root[5]
    a2 = root[6]
    a3 = root[7]
    a4 = root[8]

    answers = list(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", card.get_answers()))
    correct_letter = next(x[0] for x in answers if x[1] == card.correct_answer)
    
    q.text = f"{str(card.id_)}. What does {card.question}"
    q2.text = "eat the most?"
    [a1.text, a2.text, a3.text, a4.text] = list(map(lambda x: f"{x[0]}. {x[1]}", answers))
    etree.ElementTree(root).write(save_path + str(card.id_), pretty_print=True)

    return (card.id_, correct_letter)


if __name__ == "__main__":
    class_common_name = {
        "Teleostei": "Ray-finned fish",
        "Aves": "Birds",
        "Mammalia": "Mammals",
        "Chondrichthyes": "Cartilaginous fish",
        "Reptilia": "Reptiles",
        "Malacostraca": "Crabs, shrimp, etc.",
        "Bivalvia": "Clams, mussels, etc.",
        "Insecta": "Insects",
        "Amphibia": "Amphibians",
        "Chromadorea": "Roundworms",
        "Cephalopoda": "Octopuses, squids, etc.",
        "Echinoidea": "Sea urchins",
        "Chondrostei": "Ray-finned fish",
        "Asteroidea": "Star fish",
        "Cephalaspidomorphi": "Lamprey",
        "Euchelicerata": "Spiders, scorpions, etc.",
        "Clitellata": "Earthworms",
        "Chilopoda": "Centipedes",
        "Magnoliopsida": "Magnolias",
        "Gastropoda": "Snails, slugs",
        "Diplopoda": "Millipedes",
        "Collembola": "Springtails",
        "Chlorophyceae": "Green algae",
        "Phaeophyceae": "Brown algae",
        "Bryopsida": "Mosses",
        "Pinopsida": "Conifers",
        "Polychaeta": "Bristle worms",
        "Polyplacophora": "Chiton",
        "Conjugatophyceae": "Green algae",
        "Ulvophyceae": "Green algae",
        "Charophyceae": "Stoneworts",
        "Maxillopoda": "Barnacles, copepods, etc.",
        "Ostracoda": "Seed shrimp",
        "Branchiopoda": "Various shrimp, water fleas",
        "Granuloreticulosea": "Forams",
        "Phylactolaemata": "Moss animals",
        "Polypodiopsida": "Ferns",
        "Bangiophyceae": "Red algae",
        "Gymnolaemata": "Moss animals",
        "Holothuroidea": "Sea cucumber",
        "Anthozoa": "Sea anemones, corals",
        "Lycopodiopsida": "Clubmosses, firmosses, etc.",
        "Hydrozoa": "Hydroids",
        "Florideophyceae": "Red algae",
        "Demospongiae": "Sponge",
        "Xanthophyceae": "Yellow-green algae",
        "Dorylaimea": "Roundworms",
        "Polytrichopsida": "Mosses",
        "Lecanoromycetes": "Lichen",
        "Gnetopsida": "Shrubs",
        "Holostei": "Ray-finned bony fishes",
        "Cyanophyceae": "Blue-green algae",
        "Agaricomycetes": "Smut fungi, rust fungi",
        "Sordariomycetes": "Flask-shaped fungi",
        "Trepaxonemata": "Flatworms",
        "Thaliacea": "Sea squirts",
        "Scyphozoa": "Jellyfish",
        "Cephalocarida": "Horseshow shrimp",
        "Ciliatea": "Ciliate",
        "Enopla": "Ribbon worms",
        "Actinopterygii": "Ray-finned fish",
        "Solenogastres": "Molluscs",
        "Ophiuroidea": "Brittle Stars",
    }

    
    random.seed(10)
    print("parsing bird data...")
    data = pyreadr.read_r("dietdb.rda")["dietdb"]

    species = data["Common_Name"].drop_duplicates()
    # there are some entries where the class is either an emtpy string or NaN
    # we drop those
    prey_classes = data["Prey_Class"].drop_duplicates().replace("", float("nan")).dropna()
    print(prey_classes)

    # generate questions of type "What does [species] eat the most?"
    i = 1
    for s in species:
        if (x := find_commonest_food(s)) is not None:	
            commonest_food_class, normalized_frequency = x 
            incorrect_class_answers = prey_classes[prey_classes != commonest_food_class].to_list()

            commonest_food = class_common_name[commonest_food_class]
            incorrect_answers = [class_common_name[c] for c in incorrect_class_answers]

            card = Card(i, s, incorrect_answers, commonest_food) 
            q_number, answer = make_card(card)
            print(f"{q_number}: {answer}")
            i += 1



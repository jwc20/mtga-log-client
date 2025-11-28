import uuid
from multiprocessing.managers import all_methods
from pathlib import Path
import duckdb
from dataclasses import dataclass

import pandas as pd


def find_project_root(marker=".git"):
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        if (parent / marker).exists():
            return parent
    return current.parent


project_root = find_project_root()
scryfall_allcards_json_file_path = project_root / "card_data/scryfall/allcards.json"
new_scryfall_allcards_json_file_path = project_root / "card_data/scryfall/allcards_arena.json"

@dataclass
class Card:
    pass


# [{'object': 'related_card', 'id': UUID('0001e77a-7fff-49d2-a55c-42f6fdf6db08'), 'component': 'combo_piece', 'name': "Obyra's Attendants // Desperate Parry", 'type_line': 'Creature — Faerie Wizard // Instant — Adventure', 'uri': 'https://api.scryfall.com/cards/0001e77a-7fff-49d2-a55c-42f6fdf6db08'}
# ['object', 'id', 'component', 'name', 'type_line', 'uri']
@dataclass
class CardPart:
    parent_id: uuid.UUID
    object: str
    id: uuid.UUID
    component: str
    name: str
    type_line: str
    uri: str

@dataclass
class CardFace:
    pass





def main():
    all_cards = scryfall_allcards_json_file_path.__str__()
    duckdb.read_json(all_cards)
    
    # all cards
    # column_names = duckdb.sql(f"SELECT * FROM '{all_cards}' limit 1").columns
    # print(column_names)
    # all_arena_cards = duckdb.sql(f"SELECT id, arena_id, name, color_identity, colors, booster, rarity, mana_cost, type_line, variation, games, lang, illustration_id FROM '{all_cards}' where 'arena' in games and lang = 'en' limit 10").fetchall()
    # print(all_arena_cards)

    # all_prints
    # all_prints_cards_columns = duckdb.sql(f"SELECT all_parts FROM '{all_cards}' where 'arena' in games and lang = 'en' and all_parts is not null limit 10").columns
    # print(all_prints_cards_columns)
    all_parts_cards = duckdb.sql(f"SELECT id, all_parts FROM '{all_cards}' where 'arena' in games and lang = 'en' and all_parts is not null limit 2").fetchdf()
    # print(all_parts_cards)
    # print(all_parts_cards["all_parts"][0])
    # for i in range(len(all_parts_cards["all_parts"])):
    #     df_flat_details = pd.json_normalize(all_parts_cards["all_parts"][i])
    #     print(df_flat_details)
        
    for parent_id, all_parts in zip(all_parts_cards["id"], all_parts_cards["all_parts"]):
        for i in range(len(all_parts)):
            df_flat_details = pd.json_normalize(all_parts[i])
            df_flat_details["parent_id"] = parent_id
            print(df_flat_details)


    # add parent_id to all_parts_cards
    # for i in range(len(all_parts_cards)):
    #     all_parts_cards.at[i, "parent_id"] = all_parts_cards.at[i, "id"]
    # 
    # print(all_parts_cards)


    # get keys of all_prints_cards
    # keys = all_prints_cards["all_parts"][0][0].keys()
    # print(keys)

    # df = all_prints_cards.d
    # print(df)
    
    # card_faces
    # all_card_faces_cards_columns = duckdb.sql(f"SELECT card_faces FROM '{all_cards}' where 'arena' in games and lang = 'en' and card_faces is not null limit 10").columns
    # print(all_card_faces_cards_columns)
    # all_card_faces_cards = duckdb.sql(f"SELECT card_faces FROM '{all_cards}' where 'arena' in games and lang = 'en' and card_faces is not null limit 10").fetchall()
    # print(all_card_faces_cards)
    
    
    
    
    # all_parts = duckdb.sql(f"SELECT all_parts FROM '{all_arena_cards}'").fetchall()
    # pprint(all_parts)
    
    
    # all_card_faces = duckdb.sql(f"SELECT card_faces FROM '{all_arena_cards}'")
    # 
    # print(all_parts[:5])
    # print(" ")
    # print(all_card_faces[:5])
    
    # all_arena_cards.write_json(new_scryfall_allcards_json_file_path.__str__())
    # duckdb.sql("COPY (SELECT 42) TO 'out.parquet'")
    # print("File written")



if __name__ == "__main__":
    main()

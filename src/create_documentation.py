#!env python

import csv,sys,os
from d2rmoddocumenter import d2rmoddocumenter
import urllib.parse

if len(sys.argv) < 3:
    print("Usage: python create_documentation.py <path_to_excel_files> <output_format>")
    sys.exit(1)

excel_path = sys.argv[1]
output_format = sys.argv[2]


# Initialize documenter with path from command line
documenter = d2rmoddocumenter(excel_path)
documenter.init()

def make_header(name, nice_name):
    output = ""
    #output += f"{name}\n"
    #output += f"-------\n"
    return output

def make_footer():
    output = ""
    #output += "====\n"
    return output

all_items_out = ""

os.makedirs("../docs", exist_ok=True)

def generate_individual_output_files(items):
    items_out = ""
    for name in sorted(items.keys()):
        print(f"name: {name}")
        item = items[name]
        
        # Debug prints for main item
        #print(f"\nDEBUG: Main item {name} dictionaries:")
        #print("DEBUG: Main __dict__:", item.__dict__)
        #print("DEBUG: Main properties:", item.properties if hasattr(item, 'properties') else "No properties")
        #print("DEBUG: Main base_stats:", item.base_stats if hasattr(item, 'base_stats') else "No base_stats")
        
        # Debug prints for set items
        if hasattr(item, 'set_items'):
            #print("\nDEBUG: Set items details:")
            for i, set_item in enumerate(item.set_items):
                pass
                #print(f"\nDEBUG: Set item {i+1}: {set_item.get_nice_name()}")
                #print("DEBUG: Set item __dict__:", set_item.__dict__)
                #print("DEBUG: Set item properties:", set_item.properties if hasattr(set_item, 'properties') else "No properties")
                #print("DEBUG: Set item base_stats:", set_item.base_stats if hasattr(set_item, 'base_stats') else "No base_stats")
        
        path = items[name].get_path()
        base_filename = items[name].get_base_filename()
        os.makedirs(f"../docs/{path}", exist_ok=True)
        filename = f"../docs/{path}/{base_filename}"
        
        out = items[name].get_text(show_hidden=False)

        with open(filename, "w") as f:
            nn = items[name].get_nice_name()
            file_out = out
            f.write(file_out)
            f.close()
        items_out += out
    return items_out



#set_items_out = generate_individual_output_files(documenter.get_set_item_objects())
#with open("../docs/all_set_items.txt", "w") as f:
    #f.write(set_items_out)
    #f.close()
#all_items_out += set_items_out
output_summary_pages = False

gems_out = ""
gems_out += "{| class=\"wikitable\"\n"
gems_out += "|-\n! Name !! Helmet or Armor !! Weapon !! Shield\n"
for gemtype in [ 
                {"name": "Sapphire", "color": "blue"}, 
                {"name": "Emerald", "color": "green"}, 
                {"name": "Topaz", "color": "yellow"}, 
                {"name": "Ruby", "color": "red"}, 
                {"name": "Amethyst", "color": "purple"}, 
                {"name": "Diamond", "color": "white"}, 
                {"name": "Skull", "color": "grey"} 
    ]:
    for quality in ["", "Flawless", "Perfect"]:
        if quality:
            gemname = f"{quality} {gemtype['name']}"
        else:
            gemname = gemtype['name']
        gem = documenter.get_gem_by_name(gemname)
        gems_out += gem.get_text_gem(write_table=False, color=gemtype["color"])
gems_out += "|}"
with open("../docs/Items/Gems", "w") as f:
    f.write(gems_out)
    f.close()



runes_out = ""
runes_out += "{| class=\"wikitable\"\n"
runes_out += "|-\n! Name !! Helmet or Armor !! Weapon !! Shield\n"
for num in range(1,34):
    rune_code = f"r{num:02}"
    rune = documenter.get_gem(rune_code)
    runes_out += rune.get_text_gem()
with open("../docs/Items/Runes", "w") as f:
    f.write(runes_out)
    f.close()

###################
# Uniques
uniques = documenter.get_unique_item_objects()
uniques_out = generate_individual_output_files(uniques)
uniques_article = "== Uniques ==\n\n"
#import pprint
#pprint.pp(runewords)
for name in sorted(uniques.keys()):
    link = uniques[name].get_link()
    uniques_article += f"* [[{link}|{name}]]\n\n"
with open("../docs/Items/Uniques", "w") as f:
    f.write(uniques_article)
    f.close()
if output_summary_pages:
    with open("../docs/all_unique_items.txt", "w") as f:
        f.write(uniques_out)
        f.close()
    all_items_out += uniques_out



##################
# Runewords
runewords = documenter.get_runeword_item_objects()
runewords_out = generate_individual_output_files(runewords)
runewords_article = "== Runewords ==\n\n"
#import pprint
#pprint.pp(runewords)
for name in sorted(runewords.keys()):
    link = runewords[name].get_link()
    runewords_article += f"* [[{link}|{name}]]\n\n"
with open("../docs/Items/Runewords", "w") as f:
    f.write(runewords_article)
    f.close()
if output_summary_pages:
    with open("../docs/Items/Runewords", "w") as f:
        f.write(runewords_out)
        f.close()
    all_items_out += runewords_out

sets = documenter.get_set_objects()
sets_out = generate_individual_output_files(sets)
sets_article = "== Sets ==\n\n"
#import pprint
#pprint.pp(runewords)


#################
# Gems
for name in sorted(sets.keys()):
    link = sets[name].get_link()
    sets_article += f"* [[{link}|{name}]]\n\n"
with open("../docs/Items/Sets", "w") as f:
    f.write(sets_article)
    f.close()
if output_summary_pages:
    with open("../docs/all_sets.txt", "w") as f:
        f.write(sets_out)
        f.close()

if output_summary_pages:
    with open("../docs/all_items.txt", "w") as f:
        f.write(all_items_out)
        f.close()


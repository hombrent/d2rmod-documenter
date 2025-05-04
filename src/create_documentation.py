#!env python

import csv,sys,os
import d2rmoddocumenter
import urllib.parse

documenter = d2rmoddocumenter.d2rmoddocumenter()
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
    #items = documenter.get_set_item_objects()
    items_out = ""
    for name in items.keys():
        path = items[name].get_path()
        base_filename = items[name].get_base_filename()
        os.makedirs(f"../docs/{path}", exist_ok=True)
        filename = f"../docs/{path}/{base_filename}"
        out = items[name].get_text(show_hidden=False)
        with open(filename, "w") as f:
            nn = items[name].get_nice_name()
            file_out = make_header(name, nn) + out + make_footer()
            f.write(file_out)
            f.close()
        items_out += out
    return items_out



#set_items_out = generate_individual_output_files(documenter.get_set_item_objects())
#with open("../docs/all_set_items.txt", "w") as f:
    #f.write(set_items_out)
    #f.close()
#all_items_out += set_items_out

gems_out = ""
for gemtype in [ "Sapphire", "Emerald", "Topaz", "Ruby", "Amethyst", "Diamond", "Skull" ]:
    for quality in ["", "Flawless", "Perfect"]:
        if quality:
            gemname = f"{quality} {gemtype}"
        else:
            gemname = gemtype
        gem = documenter.get_gem_by_name(gemname)
        gems_out += gem.get_text()
with open("../docs/Gem", "w") as f:
    f.write(gems_out)
    f.close()

runes_out = ""
for num in range(1,34):
    rune_code = f"r{num:02}"
    rune = documenter.get_gem(rune_code)
    runes_out += rune.get_text()
with open("../docs/Rune", "w") as f:
    f.write(runes_out)
    f.close()

unique_items_out = generate_individual_output_files(documenter.get_unique_item_objects())
with open("../docs/all_unique_items.txt", "w") as f:
    f.write(unique_items_out)
    f.close()
all_items_out += unique_items_out

runewords_out = generate_individual_output_files(documenter.get_runeword_item_objects())
with open("../docs/all_runewords.txt", "w") as f:
    f.write(runewords_out)
    f.close()
all_items_out += runewords_out

sets_out = generate_individual_output_files(documenter.get_set_objects())
with open("../docs/all_sets.txt", "w") as f:
    f.write(sets_out)
    f.close()

with open("../docs/all_items.txt", "w") as f:
    f.write(all_items_out)
    f.close()


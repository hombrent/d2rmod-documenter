#!env python

import csv,sys,os
import d2rmoddocumenter
import urllib.parse

documenter = d2rmoddocumenter.d2rmoddocumenter()
documenter.init()

def make_html_header(name, nice_name):
    output = ""
    output += f"<!DOCTYPE html><html><head><title>{name}</title></head><body>\n"
    return output

def make_html_footer():
    output = ""
    output += "</body></html>"
    return output

all_items_out = {"html": "", "txt": ""}

os.makedirs("../html", exist_ok=True)
os.makedirs("../txt", exist_ok=True)

def generate_individual_output_files(items):
    items_out = {"html": "", "txt": ""}
    items = documenter.get_set_item_objects()
    for name in items.keys():
        for output_format in ["html", "txt"]:
            base_filename = items[name].get_base_filename(output_format=output_format)
            filename = f"../{output_format}/{base_filename}"
            out = items[name].get_text(show_hidden=False, output_format=output_format)
            items_out[output_format] += out
            with open(filename, "w") as f:
                if output_format == "html":
                    nn = items[name].get_nice_name()
                    file_out = make_html_header(name, nn) + out + make_html_footer()
                else:
                    file_out = out
                f.write(file_out)
                f.close()
    return items_out


set_items_out = generate_individual_output_files(documenter.get_set_item_objects())
with open("../html/all_set_items.html", "w") as f:
    f.write(
            make_html_header("BTDiablo Set Items", "BTDiablo_Set_Items") + 
            set_items_out["html"] + 
            make_html_footer())
    f.close()
with open("../txt/all_set_items.txt", "w") as f:
    f.write(set_items_out["txt"])
    f.close()
all_items_out["html"] += set_items_out["html"]
all_items_out["txt"] += set_items_out["txt"]



unique_items_out = generate_individual_output_files(documenter.get_unique_item_objects())
with open("../html/all_unique_items.html", "w") as f:
    f.write(
            make_html_header("BTDiablo Unique Items", "BTDiablo_Unique_Items") + 
            unique_items_out["html"] + 
            make_html_footer())
    f.close()
with open("../txt/all_unique_items.txt", "w") as f:
    f.write(unique_items_out["txt"])
    f.close()
all_items_out["html"] += unique_items_out["html"]
all_items_out["txt"] += unique_items_out["txt"]


sets_out = generate_individual_output_files(documenter.get_set_objects())
with open("../html/all_sets.html", "w") as f:
    f.write(
            make_html_header("BTDiablo Unique Items", "BTDiablo_Unique_Items") + 
            sets_out["html"] + 
            make_html_footer())
    f.close()
with open("../txt/all_sets.txt", "w") as f:
    f.write(sets_out["txt"])
    f.close()









with open("../html/all_items.html", "w") as f:
    f.write(make_html_header("BTDiablo Items", "BTDiablo_Items") + all_items_out["html"] + make_html_footer())
    f.close()

with open("../txt/all_items.txt", "w") as f:
    f.write(all_items_out["txt"])
    f.close()


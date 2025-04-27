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

all_set_items_out = {"html": "", "txt": ""}
all_unique_items_out = {"html": "", "txt": ""}
all_items_out = {"html": "", "txt": ""}
all_sets_out = {"html": "", "txt": ""}

os.makedirs("../html", exist_ok=True)
os.makedirs("../txt", exist_ok=True)

items = documenter.get_set_item_objects()
for name in items.keys():
    for output_format in ["html", "txt"]:
        base_filename = items[name].get_base_filename(output_format=output_format)
        filename = f"../{output_format}/{base_filename}"
        out = items[name].get_text(show_hidden=False, output_format=output_format)
        all_set_items_out[output_format] += out
        all_items_out[output_format] += out
        with open(filename, "w") as f:
            if output_format == "html":
                file_out = make_html_header(name, items[name].get_nice_name()) + out + make_html_footer()
            else:
                file_out = out
            f.write(file_out)
            f.close()

items = documenter.get_unique_item_objects()
for name in items.keys():
    for output_format in ["html", "txt"]:
        base_filename = items[name].get_base_filename(output_format=output_format)
        filename = f"../{output_format}/{base_filename}"
        out = items[name].get_text(show_hidden=False, output_format=output_format)
        all_unique_items_out[output_format] += out
        all_items_out[output_format] += out
        with open(filename, "w") as f:
            if output_format == "html":
                file_out = make_html_header(name, items[name].get_nice_name()) + out + make_html_footer()
            else:
                file_out = out
            f.write(file_out)
            f.close()

items = documenter.get_set_objects()
for name in items.keys():
    for output_format in ["html", "txt"]:
        base_filename = items[name].get_base_filename(output_format=output_format)
        filename = f"../{output_format}/{base_filename}"
        out = items[name].get_text(show_hidden=False, output_format=output_format)
        all_sets_out[output_format] += out
        with open(filename, "w") as f:
            if output_format == "html":
                file_out = make_html_header(name, items[name].get_nice_name()) + out + make_html_footer()
            else:
                file_out = out
            f.write(file_out)
            f.close()



with open("../html/all_unique_items.html", "w") as f:
    f.write(make_html_header("BTDiablo Uniques", "BTDiablo_Uniques") + all_unique_items_out["html"] + make_html_footer())
    f.close()

with open("../html/all_set_items.html", "w") as f:
    f.write(make_html_header("BTDiablo Set Items", "BTDiablo_Set_Items") + all_set_items_out["html"] + make_html_footer())
    f.close()

with open("../html/all_items.html", "w") as f:
    f.write(make_html_header("BTDiablo Items", "BTDiablo_Items") + all_items_out["html"] + make_html_footer())
    f.close()

with open("../txt/all_unique_items.txt", "w") as f:
    f.write(all_unique_items_out["txt"])
    f.close()

with open("../txt/all_set_items.txt", "w") as f:
    f.write(all_set_items_out["txt"])
    f.close()

with open("../txt/all_items.txt", "w") as f:
    f.write(all_items_out["txt"])
    f.close()

with open("../html/all_sets.html", "w") as f:
    f.write(make_html_header("BTDiablo Sets", "Sets_Items") + all_sets_out["html"] + make_html_footer())
    f.close()

with open("../txt/all_sets.text", "w") as f:
    f.write(all_sets_out["txt"])
    f.close()

#!env python

import csv,sys
import d2rmoddocumenter
import urllib.parse

documenter = d2rmoddocumenter.d2rmoddocumenter()
documenter.init()

# make an item name nice for anchors, urls and filenames
def make_name_nice(name):
    output = name.replace("'", "")
    output = output.replace(" ", "_")
    output = urllib.parse.quote(output)
    return output

def make_html_header(name, nice_name):
    output = ""
    output += f"<!DOCTYPE html><html><head><title>{name}</title></head><body>\n"
    return output

def make_html_footer():
    output = ""
    output += "</body></html>"
    return output

all_items_html_out = ""
all_items_text_out = ""
all_set_items_html_out = ""
all_set_items_text_out = ""
all_unique_items_html_out = ""
all_unique_items_text_out = ""
all_sets_html_out = ""
all_sets_text_out = ""

items = documenter.get_set_item_objects()
for name in items.keys():
    nice_name = make_name_nice(name)
    html_filename = f"../html/{nice_name}.html"
    html_out = items[name].get_text(show_hidden=False, html=True)
    all_set_items_html_out += html_out
    all_items_html_out += html_out
    with open(html_filename, "w") as f:
        f.write(make_html_header(name, nice_name) + html_out + make_html_footer())
        f.close()

    text_filename = f"../text/{nice_name}.txt"
    text_out = ""
    text_out += items[name].get_text(show_hidden=False, html=False)
    all_set_items_text_out += text_out
    all_items_text_out += text_out
    with open(text_filename, "w") as f:
        f.write(text_out)
        f.close()

items = documenter.get_unique_item_objects()
for name in items.keys():
    nice_name = make_name_nice(name)
    html_filename = f"../html/{nice_name}.html"
    html_out = items[name].get_text(show_hidden=False, html=True)
    all_unique_items_html_out += html_out
    all_items_html_out += html_out
    with open(html_filename, "w") as f:
        f.write(make_html_header(name, nice_name) + html_out + make_html_footer())
        f.close()

    text_filename = f"../text/{nice_name}.txt"
    text_out = items[name].get_text(show_hidden=False, html=False)
    all_unique_items_text_out += text_out
    all_items_html_out += text_out
    with open(text_filename, "w") as f:
        f.write(text_out)
        f.close()


with open("../html/all_unique_items.html", "w") as f:
    f.write(make_html_header("BTDiablo Uniques", "BTDiablo_Uniques") + all_unique_items_html_out + make_html_footer())
    f.close()

with open("../html/all_set_items.html", "w") as f:
    f.write(make_html_header("BTDiablo Set Items", "BTDiablo_Set_Items") + all_set_items_html_out + make_html_footer())
    f.close()

with open("../html/all_items.html", "w") as f:
    f.write(make_html_header("BTDiablo Items", "BTDiablo_Items") + all_items_html_out + make_html_footer())
    f.close()

with open("../text/all_unique_items.text", "w") as f:
    f.write(all_unique_items_text_out)
    f.close()

with open("../text/all_set_items.text", "w") as f:
    f.write(all_set_items_text_out)
    f.close()

with open("../text/all_items.text", "w") as f:
    f.write(all_items_text_out)
    f.close()




items = documenter.get_set_objects()
for name in items.keys():
    nice_name = make_name_nice(name)
    html_filename = f"../html/{nice_name}.html"
    html_out = items[name].get_text(show_hidden=False, html=True)
    all_sets_html_out += html_out
    with open(html_filename, "w") as f:
        f.write(make_html_header(name, nice_name) + html_out + make_html_footer())
        f.close()

    text_filename = f"../text/{nice_name}.txt"
    text_out = items[name].get_text(show_hidden=False, html=False)
    all_sets_text_out += text_out
    with open(text_filename, "w") as f:
        f.write(text_out)
        f.close()

with open("../html/all_sets.html", "w") as f:
    f.write(make_html_header("BTDiablo Sets", "Sets_Items") + all_sets_html_out + make_html_footer())
    f.close()

with open("../text/all_sets.text", "w") as f:
    f.write(all_sets_text_out)
    f.close()

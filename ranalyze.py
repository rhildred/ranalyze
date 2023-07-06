#!/usr/bin/python

import os
import re
import difflib
import subprocess

prog = re.compile("^[0-9]+\-[0-9]+")


html_content = {}


def process_html_file(htmlfile, assignment, first):
    # htmlfile to edit
    # assignment is the assignment folder name


    global html_output
    global html_content


    # Read in the html file
    with open(htmlfile, 'r') as fh:
        html_content[htmlfile] = fh.read()




print("Scanning Files:")
nFinds = 0
first = True
for root, dirs, filenames in os.walk(".", topdown=True):
    dirs[:] = [d for d in dirs if d not in ["node_modules", "__MACOSX", ".vscode", "bin", "obj"]]
    for filename in filenames: 
        if ".zip" not in filename and ".mp4" not in filename and ".mkv" not in filename and ".m4a" not in filename and ".mov" not in filename and ".webp" not in filename and ".png" not in filename and ".rar" not in filename and ".docx" not in filename:
            full_filename = os.path.join(root,filename)
            nFinds += 1
            process_html_file(full_filename, filename, first)
            first = False



r = re.compile(r"(\d+-\d+)")

# Run the diff analysis to look for copied assignments
print("\nResults:\n")
items = list(html_content.items())
for a in range(0, len(items)-1):
    for b in range(a+1, len(items)):
        diff = difflib.SequenceMatcher(a=items[a][1].splitlines(1), b=items[b][1].splitlines(1))
        ratio = diff.ratio()
        # Here we check the threshold, ie 60% is 0.6
        if ratio > 0.7:
            print("Similar: {}\n{}\n{}\n".format(ratio*100, items[a][0], items[b][0]))

#!/usr/bin/python

import os
import re
import difflib
from zipfile import ZipFile
import glob


html_content = {}


def process_html_file(htmlfile, assignment, first):
    # htmlfile to edit
    # assignment is the assignment folder name


    global html_output
    global html_content


    # Read in the html file
    with open(htmlfile, 'r') as fh:
        html_content[htmlfile] = fh.read()

#unzip recursively

def unpack_zip(zipfile='', path_from_local=''):
    filepath = path_from_local+zipfile
    extract_path = ""
    if 'Download' in zipfile:
        extract_path = re.sub(' Download.*', '', filepath) + '/'
    else:
        extract_path = filepath.strip('.zip')+'/'
        extract_path = re.sub('[0-9]{6}-[0-9]{6} - ', '', extract_path)
    parent_archive = ZipFile(filepath)
    parent_archive.extractall(extract_path)
    namelist = parent_archive.namelist()
    parent_archive.close()
    for name in namelist:
        try:
            if name[-4:] == '.zip':
                unpack_zip(zipfile=name, path_from_local=extract_path)
        except:
            print('failed on', name)
            pass
    return extract_path
    
    # you can just call this with filename set to the relative path and file.
try:
    parentZip = glob.glob("*.zip")[0]
    sFolder = re.sub(' Download.*', '', parentZip)
    if os.path.isdir(sFolder):
        print(f"folder {sFolder} exists ... comparing")
    else:
        unpack_zip(parentZip)
except:
    print("No zip found. Should there be a zip file with files to compare?")
# build files
nFinds = 0
first = True
for root, dirs, filenames in os.walk(".", topdown=True):
    dirs[:] = [d for d in dirs if d not in ["node_modules", "__MACOSX", ".vscode", "bin", "obj", ".git"]]
    for filename in filenames: 
        if not re.search("(.zip|.mp4|.mkv|.m4a|.mov|.webp|.png|.rar|.docx|.pdf|.jpg|.json|.gitignore|.ds_store|.sln|.csproj|.config|assemblyinfo.cs|.vsidx|.suo|.pptx|.sqlite|.lock|license|readme.md|sitemap.xml|.xlsx)$", filename.lower()):
            full_filename = os.path.join(root,filename)
            try:
                process_html_file(full_filename, filename, first)
                nFinds += 1
                first = False
            except:
                print(f"exception processing {full_filename}")


r = re.compile(r"(\d+-\d+)")

# Run the diff analysis to look for copied assignments
print("\nResults:\n")
items = list(html_content.items())
for a in range(0, len(items)-1):
    frequencyHundred = dict()
    frequencyItem = dict()
    for b in range(a+1, len(items)):
        if items[b][0] in frequencyItem:
            frequencyItem[items[b][0]] += 1
        else:
            frequencyItem[items[b][0]] = 1

        diff = difflib.SequenceMatcher(a=items[a][1].splitlines(1), b=items[b][1].splitlines(1))
        ratio = diff.ratio()
        # Here we check the threshold, ie 60% is 0.6
        if ratio == 1:
            if items[b][0] in frequencyHundred:
                frequencyHundred[items[b][0]] += 1
            else:
                frequencyHundred[items[b][0]] = 1
        elif ratio > 0.6:
            print("Similar: {}\n{}\n{}\n".format(ratio*100, items[a][0], items[b][0]))
    for b in range(a+1, len(items)):
        if items[b][0] in frequencyHundred:
            percent100s = frequencyHundred[items[b][0]] / frequencyItem[items[b][0]]
            # for items that match 100% we only look if 1/2 the instances don't match 100%
            # I am not sure about this approach but it get's rid of boilerplate code
            if percent100s < .5:
                print("Similar: {}\n{}\n{}\n".format(100, items[a][0], items[b][0]))
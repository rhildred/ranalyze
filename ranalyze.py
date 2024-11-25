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
    extract_path = filepath.strip('.zip').replace(" ", "")
    extract_path = re.sub('Download.*', '', extract_path)
    extract_path = re.sub('\\d+-\\d+[ -]+', '', extract_path)
    extract_path += "/"
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
aZips = glob.glob("*.zip")
if len(aZips) == 0:
    print("No zip found. Should there be a zip file with files to compare?")
else:
    for parentZip in aZips:
        unpack_zip(parentZip)
# build files
nFinds = 0
first = True
for root, dirs, filenames in os.walk(".", topdown=True):
    dirs[:] = [d for d in dirs if d not in ["node_modules", "__MACOSX", ".vscode", "bin", "obj", ".git"]]
    for filename in filenames: 
        if not re.search("(.zip|.mp4|.mkv|.m4a|.mov|.webp|.png|.rar|.docx|.pdf|.jpg|.jpeg|.json|.gitignore|.ds_store|.sln|.csproj|.config|assemblyinfo.cs|.vsidx|.suo|.pptx|.sqlite|.lock|license|readme.md|sitemap.xml|.xlsx|.bin|dtbcache.v2|.gif|.eot|.woff|.otf|.woff2|.mo|.ttf)$", filename.lower()):
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
frequencyHundred = dict()
frequencyItem = dict()
for a in range(0, len(items)-1):
    for b in range(a+1, len(items)):
        if items[b][0] in frequencyItem:
            frequencyItem[items[b][0]] += 1
        else:
            frequencyItem[items[b][0]] = 1

        diff = difflib.SequenceMatcher(a=items[a][1].splitlines(1), b=items[b][1].splitlines(1))
        ratio = diff.ratio()
        # Here we check the threshold, ie 60% is 0.6
        if ratio > 0.6:
            file_a = items[a][0]
            date_match = r"(Jan|January|Feb|February|Mar|March|Apr|April|May|Jun|June|Jul|July|Aug|August|Sep|September|Oct|October|Nov|November|Dec|December)[\d\s,]*[AP]M"
            junk_match = r"[\s\-\\\/\.\,_]"
            file_a_chars = re.sub(junk_match, "", re.sub(date_match, "", file_a))
            file_b = items[b][0]
            file_b_chars = re.sub(junk_match, "", re.sub(date_match, "", file_b))
            name_similarity = difflib.SequenceMatcher(None, file_a_chars, file_b_chars).ratio()
            if name_similarity != 1:
                print("Similar: {}\n{}\n{}\n".format(ratio*100, file_a, file_b))

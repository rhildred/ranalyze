#!/usr/bin/python

import os
import re
import difflib
from zipfile import ZipFile
import glob

prog = re.compile("^[0-9]+-[0-9]+")


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
    extract_path = filepath.strip('.zip')+'/'
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
    print(f"parent zip {parentZip}")
    sFolder = parentZip.replace(".zip", "")
    if os.path.isdir(sFolder):
        print(f"folder {sFolder} exists ... comparing")
    else:
        unpack_zip(parentZip)
except:
    print("No zip found. Should there be a zip file with files to compare?")
# build files
print("Scanning Files:")
nFinds = 0
first = True
for root, dirs, filenames in os.walk(".", topdown=True):
    dirs[:] = [d for d in dirs if d not in ["node_modules", "__MACOSX", ".vscode", "bin", "obj", ".git"]]
    for filename in filenames: 
        if not re.search("(.zip|.mp4|.mkv|.m4a|.mov|.webp|.png|.rar|.docx|.pdf|.jpg|.json|.gitignore|.ds_store|.sln|.csproj|.config|assemblyinfo.cs|.vsidx|.suo|.pptx|.sqlite|.lock)$", filename.lower()):
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
    for b in range(a+1, len(items)):
        diff = difflib.SequenceMatcher(a=items[a][1].splitlines(1), b=items[b][1].splitlines(1))
        ratio = diff.ratio()
        # Here we check the threshold, ie 60% is 0.6
        if ratio > 0.6:
            print("Similar: {}\n{}\n{}\n".format(ratio*100, items[a][0], items[b][0]))

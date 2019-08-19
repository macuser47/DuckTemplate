#!/usr/bin/python3
"""
Duck parser for filling in components of duck templates
"""

import os
import sys
import re
from collections import defaultdict, namedtuple
import shutil
import json


DUCKS_URI = "./ducks" 
IGNORED_FILES = ["README.md"]

DUCK_OPEN = re.escape("{<")
DUCK_CLOSE = re.escape(">}")

#lookahead regex for any inner part of a duck string
DUCK_INNER_CHECK = f"(?! {DUCK_OPEN}) (?! {DUCK_CLOSE})"\
        .replace(" ", "")

MATCH_ALL = "(?:.|\r)"
MATCH_NOCOLON = "[^:]"

#should choose the shortest possible {< .. >} in all cases
DUCK_REGEX = \
f"""
{DUCK_OPEN}
(?: 
( (?: {DUCK_INNER_CHECK} {MATCH_NOCOLON})* ) 
:)?
( (?: {DUCK_INNER_CHECK} {MATCH_ALL})+ )?
{DUCK_CLOSE}
"""\
        .replace(" ", "")\
        .replace("\n", "")\
        .replace("\r", "\n") #It's a hack, but ¯\_(ツ)_/¯

DuckField = namedtuple("DuckField", ["id", "query"])

class DuckProcessor:
    def __init__(self, regex):
        self.fsm = re.compile(regex)

    def process_duck(self, duck_path, duck_name):
        try:
            with open(duck_path) as f:
                contents = f.read()
        except OSError:
            raise SystemExit(
                "duckparse: read failed for {}".format(duck_path)
            )

        #iterate over matches, query, and create new file
        newfile = ""
        prev_index = 0
        id_cache = {}
        for match in self.fsm.finditer(contents):
            duck_match = DuckField(*match.groups())

            #check if user query is necessary
            if (duck_match.id is not None):
                if (duck_match.id in id_cache):
                    value = id_cache[duck_match.id]
                elif duck_match.query is not None:
                    value = input("{}\t".format(duck_match.query))
                    id_cache[duck_match.id] = value
                else:
                    raise SystemExit(
                        f"duckparse: unknown id '{duck_match.id}'"
                    )
            else:
                value = input("{}\t".format(duck_match.query))

            newfile += contents[prev_index:match.start()]
            newfile += value
            prev_index = match.end()
        newfile += contents[prev_index:]

        new_path = os.path.join(".", duck_name)
        with open(new_path, "w") as f:
            f.write(newfile)

        return id_cache

def generate_ducks():
    #grab and process all ducks
    dproc = DuckProcessor(DUCK_REGEX)
    duck_dicts = {}
    for entry in os.scandir(DUCKS_URI):
        if entry.name in IGNORED_FILES:
            continue

        if entry.is_file():
            print("Duck query for {}".format(entry.name))
            duck_dicts[entry.name] = dproc.process_duck(entry.path, entry.name)

    #delete ducks folder :(
    shutil.rmtree(
        DUCKS_URI, 
        onerror=lambda f,p,e: print(f"duckparse: error deleting ducks: {e}")
    )

    #return id, value pairs for every file
    return duck_dicts 

if __name__ == "__main__":
    #query user to generate ducks, then write id, value pairs to stdout in json
    pairs = generate_ducks()
    print(json.dumps(pairs))

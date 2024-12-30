## DATA LABELING UTILITY
#  
#  Provide a file with posts grouped by user (like the ones created by group_by_user.py)
#  as a command-line argument
#
#  Manually label each user and press control-C when you're done. Labels will be written
#  to the input file. When you run the script again on the same file, all users that have
#  already been labeled will be skipped, so you don't have to redo work.
#

from os import path
import json
from enum import Enum
import sys
import signal


LABELS = {
    # formatted as `shortcut: name`
    # SHORTCUT HAS TO BE LOWERCASE!
    "r": "Russia",
    "u": "Ukraine",
    "n": "Neutral"
} # TODO: maybe add Unknown class?

## Made this into a class, in case we want to write a chatgpt integration or something.
class Labeler:
    def __init__(self, filename):
        self.filename = filename
        with open(filename, "r") as f:
            self.lines = list(map(json.loads, f.readlines()))
        self.selectLine(0)
    
    def getCurrentLine(self):
        return self.lines[self.current_line]

    def selectLine(self, index):
        self.current_line = index
        if "Label" in self.getCurrentLine():
            self.selectLine(index + 1)

    def setLabel(self, label):
        self.lines[self.current_line]["Label"] = label
        self.selectLine(self.current_line + 1)
    
    def canContinue(self):
        return len(self.lines) > self.current_line

    def writeToFile(self):
        with open(self.filename, "w") as f:
            for line in self.lines:
                json.dump(line, f)
                f.write("\n")

## Main program logic
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Give filename (such as data/cf_by_user.ndjson) as command line argument")
        sys.exit()
    print("Loading file...", end="")
    labeler = Labeler(sys.argv[1])
    print("Done.")
    startline_raw = input(f"Dataset consists of {len(labeler.lines)} users. Select starting index (default=0): ")
    labeler.selectLine(int(startline_raw or 0))
    
    ## Basically the only way to exit the loop is by pressing control-C which will
    #  exit the try block and enter the finally block. There is definitely a better
    #  way to do this but I have run out of fucks to give
    try:
        while labeler.canContinue(): 
            post_bodies = map(lambda post: post["Text"], labeler.getCurrentLine()["posts"])
            print("---\n", "\n---\n".join(post_bodies), "\n---")
            print(f"Select label from {', '.join(LABELS.values())} [{'/'.join(LABELS.keys())}]: ", end="")
            selected_option = input().lower()
            while selected_option not in LABELS:
                selected_option = input("Select a valid option [{'/'.join(LABELS.keys())}]: ").lower()
            labeler.setLabel(LABELS[selected_option])
    # except Exception as e:
    #    print(e)
    finally:
        save_or_not = input("\nSave file? [Y/n]: ")
        if len(save_or_not) > 0 and save_or_not[0].lower() == "n":
            sys.exit()
        print("Saving...", end="")
        labeler.writeToFile()
        print("Saved.")

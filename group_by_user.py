## This script groups files by author and writes them to a file
#  
#  Files are written as NDJson, so they can be partially written, line by line. It
#  probably saves some memory (but maybe it doesn't, I haven't checked). I have done
#  SOME optimisation, but lmk if it's still too slow.
#  TODO: maybe add parent text to each post?

import pandas as pd
import json
import gc
import math

def print_progress(i, total):
    if i % 1000 == 0:
        progress = math.floor(i / total * 100)
        print(f"\033[F{progress}% [{i} / {total}]")
    if i + 1 >= total:
        print(f"\033[FDone!                          ")

def group_by_author_and_write(posts: pd.DataFrame, file_descriptor):
    print("grouping posts by author\n...")
    users = dict()
    
    num_posts = len(posts)
    for i, post in posts.iterrows():
        author = post["Author"]
        if author in users:
            users[author].append(post["Post ID"])
        else:
            users[author] = [post["Post ID"]]
        print_progress(i, num_posts) 
    
    print("Writing to file\n")
    num_users = len(users)
    posts.set_index("Post ID", inplace=True)
    for i, (user, user_posts) in enumerate(users.items()):
        json.dump({
            "username": user,
            "posts": user_posts
        }, file_descriptor)
        file_descriptor.write("\n")
        print_progress(i, num_users)

if __name__ == "__main__":
    print("processing geopolitics")
    geo_posts = pd.read_csv("data/geopolitics_parent_child.csv")
    with open("data/geo_by_user.ndjson", "w") as f:
        group_by_author_and_write(geo_posts, f)

    del geo_posts
    gc.collect()
    
    print("processing combatfootage")
    cf_posts = pd.read_csv("data/combatfootage_parent_child.csv")
    with open("data/cf_by_user.ndjson", "w") as f:
        group_by_author_and_write(cf_posts, f)

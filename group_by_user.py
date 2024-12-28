## This script groups files by author and writes them to a file
#  
#  Files are written as NDJson, so they can be partially read, line by line. Might be
#  necessary seeing as how some files are huge.
#  TODO: maybe add parent text to each post?

import pandas as pd
import json
import gc

def group_by_author_and_write(posts: pd.DataFrame, file_descriptor):
    users = set()
    
    for _, post in posts.iterrows():
        users |= {post["Author"],}
    
    # doing it like this so you don't run out of memory (idk if it works tho)
    for user in users:
        user_posts = posts.query("Author == @user").to_dict(orient="records")
        json.dump({
            "username": user,
            "posts": user_posts
        }, file_descriptor)
        file_descriptor.write("\n")

if __name__ == "__main__":
    geo_posts = pd.read_csv("data/geopolitics_parent_child.csv")
    with open("data/geo_by_user.ndjson", "w") as f:
        group_by_author_and_write(geo_posts, f)

    del geo_posts
    gc.collect()

    cf_posts = pd.read_csv("data/combatfootage_parent_child.csv")
    with open("data/cf_by_user.ndjson", "w") as f:
        group_by_author_and_write(cf_posts, f)

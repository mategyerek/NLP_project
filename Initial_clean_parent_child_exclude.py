# Takes raw dataset, removes utility bots etc.
# Author,Upvotes,Parent ID,Post ID,Most Upvoted Child,Text
import json
import pandas as pd
from collections import defaultdict

# Users to be filtered out
excluded_users = ["TheWorldPost24", "AutoModerator", "SaveVideo", "Flair_Helper", "savevideobot", "redditspeedbot", "haikusbot", "sneakpeekbot", "WikiSummarizerBot", "ModeratelyHelpfulBot", "RedditMP4Bot", "RemindMeBot", "stabbot", "SomaliNotSomalianbot", "AmputatorBot", "twitterStatus_Bot", "songfinderbot", "RepostSleuthBot", "WikiMobileLinkBot", "TrendingBot", "LuckyNumber-Bot"]
# Directories - Haven't got github on my end yet, please fix if broken
GeoComs = "data/geopolitics/geopolitics_comments.ndjson"
GeoSubs = "data/geopolitics/geopolitics_submissions.ndjson"
GeoOut = "data/geopolitics_parent_child.csv"

CombatComs = "data/combatfootage/combatfootage_comments.ndjson"
CombatSubs = "data/combatfootage/combatfootage_submissions.ndjson"
CombatOut = "data/combatfootage_parent_child.csv"


def process_reddit_data(comments_file, submissions_file, output_file, excluded_users):
    def print_progress(current, total, description="Processing", interval=5):
        """Print progress at specified intervals."""
        if total == 0:  # Avoid division by zero
            return
        percentage = (current / total) * 100
        if percentage % interval < 100 / total:  # Update only at intervals
            progress = f"{description}: {current}/{total} ({percentage:.2f}%)"
            print(progress, end="\r")

    # Load submissions and comments
    submissions = []
    comments = []
    error_lines = []

    print("Parsing submissions...")
    # Parse submissions
    with open(submissions_file, "r", encoding="utf-8") as infile:
        lines = infile.readlines()
        total_lines = len(lines)
        for i, line in enumerate(lines, start=1):
            try:
                submission = json.loads(line)
                # Filter out excluded authors and deleted posts
                if submission.get("author") not in excluded_users and submission.get("selftext") not in [None, "[deleted]", "[removed]"]:
                    submissions.append(submission)
            except json.JSONDecodeError:
                error_lines.append(line)
            print_progress(i, total_lines, "Parsing Submissions")

    print("\nParsing comments...")
    # Parse comments
    with open(comments_file, "r", encoding="utf-8") as infile:
        lines = infile.readlines()
        total_lines = len(lines)
        for i, line in enumerate(lines, start=1):
            try:
                comment = json.loads(line)
                # Filter out excluded authors and deleted comments
                if comment.get("author") not in excluded_users and comment.get("body") not in [None, "[deleted]", "[removed]"]:
                    comments.append(comment)
            except json.JSONDecodeError:
                continue
            print_progress(i, total_lines, "Parsing Comments")

    print("\nProcessing data...")
    # Prepare data for DataFrame
    data = []
    post_children = defaultdict(list)  # To track children for each post
    most_upvoted = {}  # To store the most upvoted child for each parent

    # Filter and process comments
    total_comments = len(comments)
    excluded_ids = set()  # Track IDs of posts and comments by excluded users
    for i, com in enumerate(comments, start=1):
        post_id = com["id"]
        parent_id = com.get("parent_id", "").split("_")[-1]
        upvotes = com.get("score", 0)
        
        if com["author"] in excluded_users or parent_id in excluded_ids:
            excluded_ids.add(post_id)  # Mark this comment and its children as excluded
            continue

        # Track most upvoted child for each parent
        if parent_id not in most_upvoted or upvotes > most_upvoted[parent_id][1]:
            most_upvoted[parent_id] = (post_id, upvotes)
        
        post_children[parent_id].append(post_id)
        text = com["body"].replace("\n", " ").replace("\r", " ").replace("\u00a0", " ")  # Normalize spaces
        data.append({
            "Author": com["author"],
            "Upvotes": upvotes,
            "Parent ID": parent_id,
            "Post ID": post_id,
            "Most Upvoted Child": None,  # Placeholder; updated later
            "Text": text
        })
        print_progress(i, total_comments, "Processing Comments")

    # Process submissions
    for sub in submissions:
        post_id = sub["id"]
        title = sub["title"]
        selftext = sub.get("selftext", "")
        text = f"{title} -=- {selftext}" if selftext else title
        text = text.replace("\n", " ").replace("\r", " ").replace("\u00a0", " ")  # Normalize spaces

        if sub["author"] in excluded_users:
            excluded_ids.add(post_id)  # Mark this post and its children as excluded
            continue
        
        # Ensure "Most Upvoted Child" is None if there are no valid children
        most_upvoted_child = most_upvoted.get(post_id, (None, 0))[0]
        if most_upvoted_child not in post_children.get(post_id, []):
            most_upvoted_child = None

        data.append({
            "Author": sub["author"],
            "Upvotes": sub.get("score", 0),
            "Parent ID": None,
            "Post ID": post_id,
            "Most Upvoted Child": most_upvoted_child,
            "Text": text
        })

    # Update "Most Upvoted Child" for comments
    for row in data:
        if row["Parent ID"] in most_upvoted:
            child_id, _ = most_upvoted[row["Parent ID"]]
            # Ensure only valid children are assigned
            if child_id != row["Post ID"] and child_id in post_children[row["Parent ID"]]:
                row["Most Upvoted Child"] = child_id

    print("\nCreating DataFrame...")
    df = pd.DataFrame(data)

    print("Saving to CSV...")
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

    return error_lines

# Badabing Badaboom
geo_error_lines = process_reddit_data(GeoComs, GeoSubs, GeoOut, excluded_users)
combat_error_lines = process_reddit_data(CombatComs, CombatSubs, CombatOut, excluded_users)

# the next line makes me want to drink one million beers
for lines, subname in [(geo_error_lines, "geopolitics"), (combat_error_lines, "combatfootage")]:
    if len(errors) > 0:
        print(f"Error reading JSON data in {subname} file. Lines with errors:")
        for line in lines:
            print(line)

import os
import praw
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
from tqdm import tqdm

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT")
)

# Global dictionary to track progress across requests
fetch_progress = {
    "status": "idle",
    "current": 0,
    "total": 0,
    "message": ""
}

def get_reddit_comments(query, limit_posts=100, subreddit_name="all", topic_name="topic"):
    global fetch_progress
    
    fetch_progress["status"] = "fetching"
    fetch_progress["current"] = 0
    fetch_progress["total"] = limit_posts
    fetch_progress["message"] = f"Fetching posts for '{query}'"
    
    subreddit = reddit.subreddit(subreddit_name)

    comment_data = []
    post_count = 0

    print(f"Fetching {limit_posts} posts for '{query}'...")
    posts = list(subreddit.search(query, sort="relevance", limit=limit_posts))
    
    # Update total if we got fewer posts than requested
    actual_posts = len(posts)
    fetch_progress["total"] = actual_posts
    fetch_progress["message"] = "Processing comments from posts..."

    for submission in tqdm(posts, desc=f"Processing posts"):
        post_count += 1
        fetch_progress["current"] = post_count
        
        # CRITICAL FIX: limit=0 stops PRAW from making 100s of recursive network requests per post
        submission.comments.replace_more(limit=0)

        for comment in submission.comments.list():
            cleaned = comment.body.replace('\n', ' ').strip()

            if not cleaned or cleaned.lower() in ["[deleted]", "[removed]"]:
                continue

            timestamp = datetime.utcfromtimestamp(
                comment.created_utc
            ).strftime('%Y-%m-%d %H:%M:%S')

            comment_data.append({
                "post_id": submission.id,
                "post_title": submission.title,
                "text": cleaned,
                "score": comment.score,
                "timestamp": timestamp
            })

    fetch_progress["status"] = "analyzing"
    fetch_progress["message"] = "Analyzing and saving data..."
    print(f"Collected comments from {post_count} posts")

    df = pd.DataFrame(comment_data)
    
    # Ensure directory exists and construct target path
    output_dir = os.path.join("static", "analysed")
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, f"{topic_name}.csv")
    
    if not df.empty:
        df.to_csv(output_path, index=False)
        print(f"Saved results to {output_path}")
    else:
        # Create an empty CSV just to ensure the file is created, or leave it. 
        # Usually it's better to create an empty one with columns
        df = pd.DataFrame(columns=["post_id", "post_title", "text", "score", "timestamp"])
        df.to_csv(output_path, index=False)
        print(f"No comments found. Saved empty template to {output_path}")
        
    fetch_progress["status"] = "complete"
    fetch_progress["message"] = "Analysis complete!"
        
    return df

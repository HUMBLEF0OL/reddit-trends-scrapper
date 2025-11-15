import requests
import pandas as pd
import time

# scrapper details
SUBREDDIT = "technology"
TIME_FILTER = "day"
LIMIT = 50
OUTPUT_CSV=f"scraps/reddit_{SUBREDDIT}_{time.strftime('%Y-%m-%d %H-%M-%S')}.csv"

# endpoint details
ENDPOINT=f"https://www.reddit.com/r/{SUBREDDIT}/top/.json?t={TIME_FILTER}&limit={LIMIT}"

headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(ENDPOINT, headers=headers)
if response.status_code != 200:
    raise Exception(f"Request failed with status code {response.status_code}")

data = response.json()
posts = data["data"]["children"]

records = []
for post in posts:
    post_data = post["data"]
    records.append({
        "title": post_data["title"],
        "upvotes": post_data["ups"],
        "comments": post_data["num_comments"],
        "author": post_data["author"],
        "permalink": f"https://www.reddit.com{post_data['permalink']}",
        "created_utc": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(post_data["created_utc"]))
    })

df = pd.DataFrame(records)
print(df.head())
df.to_csv(OUTPUT_CSV, index=False)
print(f"Saved {len(df)} posts to {OUTPUT_CSV}")
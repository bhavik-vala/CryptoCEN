"""Post the most recent saved draft from data/posts.json to LinkedIn."""
import os
import json
import logging
from linkedin_poster import LinkedInPoster
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("valtrilabs.post_saved")

def load_latest_post(path="data/posts.json"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Posts file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not data:
        raise ValueError("No posts found in posts.json")
    return data[-1]


def main():
    post = load_latest_post()
    content = post.get("content")
    if not content:
        raise ValueError("Latest post has no content")
    poster = LinkedInPoster(test_mode=(os.getenv("TEST_MODE","true").lower() in ("1","true","yes")))
    logger.info("Posting saved draft (test_mode=%s)", poster.test_mode)
    res = poster.post(content)
    logger.info("Post result: %s", res)
    print(res)

if __name__ == '__main__':
    main()

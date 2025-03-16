import os
import requests
from requests_oauthlib import OAuth1
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Twitter API credentials
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# OAuth1 Authentication Setup
auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

def upload_media(image_file):
    """Upload media to Twitter and return media_id."""
    url = "https://upload.twitter.com/1.1/media/upload.json"
    files = {'media': image_file.getvalue()}
    response = requests.post(url, auth=auth, files=files)
    
    if response.status_code == 200:
        media_id = response.json().get('media_id_string')
        return media_id
    else:
        st.error(f"Media upload failed: {response.text}")
        return None

def post_tweet(caption, media_id):
    """Post a tweet with the provided caption and media."""
    url = "https://api.twitter.com/1.1/statuses/update.json"
    payload = {"status": caption, "media_ids": media_id}
    response = requests.post(url, auth=auth, params=payload)
    
    if response.status_code == 200:
        st.success("Tweet posted successfully!")
    else:
        st.error(f"Tweet posting failed: {response.text}")

def main():
    st.title("Twitter Post Automation")

    # Upload image
    image_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
    
    # Caption input
    caption = st.text_input("Enter Caption for the Post")
    
    # Submit button
    if st.button("Post to Twitter"):
        if image_file and caption:
            media_id = upload_media(image_file)
            if media_id:
                post_tweet(caption, media_id)
        else:
            st.warning("Please provide both an image and a caption.")

if __name__ == "__main__":
    main()

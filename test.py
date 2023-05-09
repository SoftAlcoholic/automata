import requests
from config import WORDPRESS_USER, WORDPRESS_TKN, WORDPRESS_API_KEY

def post_wordpress_article(title, content, url):
    # Set up the API endpoint for creating a post
    endpoint = f"{url}/wp-json/wp/v2/posts"

    # Set up the request headers with the user's login credentials
    headers = {"Authorization": f"Bearer {WORDPRESS_API_KEY}", "Content-Type": "application/json"}
    # Set up the request body with the post data
    data = {"title": title, "content": content}

    # Get the username and password from environment variables or a configuration file
    username = WORDPRESS_USER
    password = WORDPRESS_TKN
    if not (username and password):
        raise ValueError("WordPress username and password are required")

    # Send the POST request to create the new post
    try:
        response = requests.post(endpoint, headers=headers, auth=(username, password), json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error: {err}")
        print(f"Response content: {err.response.content}")
        print(f"Response headers: {err.response.headers}")
    except requests.exceptions.RequestException as err:
        print(f"Request error: {err}")
        print(f"Response content: {err.response.content}")
        print(f"Response headers: {err.response.headers}")

# Example usage
title = "My new post"
content = "This is the content of my new post"
url = "https://localhost/wordpress/"

post_wordpress_article(title, content, url)

import requests
from requests.exceptions import HTTPError, RequestException

def send_to_wordpress(title, content, endpoint, api_key, username):
    # Set up the request headers with the user's login credentials
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    # Set up the request body with the post data
    data = {"title": title, "content": content}

    # Use a session object to reuse the same TCP connection for multiple requests
    with requests.Session() as session:
        session.headers.update(headers)

        # Send the POST request to create the new post
        try:
            response = session.post(endpoint, json=data, auth=(username,api_key))
            response.raise_for_status()
            return response.json()
        except HTTPError as err:
            print(f"HTTP error: {err}")
            print(f"Response content: {err.response.content}")
            print(f"Response headers: {err.response.headers}")
        except RequestException as err:
            print(f"Request error: {err}")

title = "My new post"
content = "This is the content of my new post"
endpoint = "https://arrozboluga.com/w/w//wp-json/wp/v2/posts"
api_key = "RYho Tdx2 lUWr GONL tuBj bePt"
username = "@utomat@"

send_to_wordpress(title, content, endpoint, api_key, username)

import requests
from requests.structures import CaseInsensitiveDict
from PIL import Image
from config import OPENAI_API_KEY


def generate_image(prompt):
    # Set up API request parameters
    url = "https://api.openai.com/v1/images/generations"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {OPENAI_API_KEY}"
    
    # Set up prompt and model parameters
    model = "image-alpha-001"
    prompt = f"Generate an image of {prompt}"
    batch_size = 1
    
    # Pass prompt to DALL-E model for image generation
    data = {
        "model": model,
        "prompt": prompt,
        "num_images": batch_size,
        "size": '1024x1024',
        "response_format": "url"
    }

    resp = requests.post(url, headers=headers, json=data)

    # Check for errors in API response
    if resp.status_code != 200:
        print(f"Error: {resp.status_code} - {resp.text}")
        return
    
    # Extract image URL from API response
    response_text = resp.json()
    try:
        image_url = response_text['data'][0]['url']
    except KeyError:
        print(f"Error: Could not find image URL in response - {resp.text}")
        return

    # Download and display image
    image = Image.open(requests.get(image_url, stream=True).raw)
    image.show()

generate_image('Generate an image of a crisp, ripe red apple resting on a pristine white plate, with soft shadows falling across the plate and the apples surface.')

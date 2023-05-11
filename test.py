import requests
import openai
import time
from requests.structures import CaseInsensitiveDict
from PIL import Image
from config import OPENAI_API_KEY, OPENAI_ENGINE_ID


# Initialize the OpenAI API client with your API key
openai.api_key = OPENAI_API_KEY

# Define a function to generate a prompt for image generation
def generate_image_prompt(title: str) -> str:
    # Define the agent profile and prompt for the introduction
    agent_profile = "a prompt engineer, expert in dalle models, and you are working on a project to generate a photo, they are going to be used as a portrait for a wordpress post)"
    context_params = f"the title of the wordpress page is {title} (use this param as metadata u dont need to write it in the result, just use it as context, mandatory = make not to ask dalle for symbols, captions or letters)"
    task = f"Generate prompt to generate an image for the post portrait(respond only the generated prompt, be as descriptive and specific as possible)."
    prompt = f"You are {agent_profile}, {context_params}. {task}."
    try:
        # Use OpenAI's API to generate an introduction based on the prompt
        response = openai.Completion.create(
            engine=OPENAI_ENGINE_ID,
            prompt=prompt,
            max_tokens=2000,
            n=1,
            stop=None,
            temperature=0.2
        )
        print('image prompt')
        time.sleep(10)
        # Return the generated introduction as a string with leading/trailing white space removed
        return response.choices[0].text.strip()
    except Exception as e:
        # If there's an error with the OpenAI API, raise a ValueError with the error message
        raise ValueError(str(e))

def generate_image(prompt):
    # Set up API request parameters
    url = "https://api.openai.com/v1/images/generations"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {OPENAI_API_KEY}"
    
    # Set up prompt and model parameters
    model = ""
    prompt = f"Generate an photo of {prompt}"
    batch_size = 1
    
    # Pass prompt to DALL-E model for image generation
    data = {
        "model": model,
        "prompt": prompt,
        "num_images": batch_size,
        "size": "512x512",
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
        return None
    # Download and display image
    image = Image.open(requests.get(image_url, stream=True).raw)
    image.show()
    return image_url

def generate_image2(prompt):
    response = openai.Image.create(
    prompt=f"Generate an photo of {prompt}",
    n=1,
    size="512x512"
)
    print(prompt)
    return response['data'][0]['url']
title = "Consejos de Fitness para Quemar Grasa: ¡Logra tu Meta!"    
prompt_img = str(generate_image_prompt(title))


#print(str(generate_image(prompt_img)))

print(str(generate_image2(prompt_img)))

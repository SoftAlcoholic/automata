# Description: Text redaction stage
# Author: Victor Bonilla

#import the required libraries
import openai
import time
from fastapi import FastAPI
from pydantic import BaseModel
import requests
from requests.exceptions import HTTPError, RequestException
from requests.structures import CaseInsensitiveDict

#import feedparser
#import xmlrpc.client
from config import OPENAI_API_KEY, OPENAI_ENGINE_ID, WORDPRESS_URL, WORDPRESS_USER, WORDPRESS_TKN, WORDPRESS_API_KEY

# Initialize the FastAPI app
app = FastAPI()

# Define a data model for the input text
class TextInput(BaseModel):
    text: str

# Initialize the OpenAI API client with your API key
openai.api_key = OPENAI_API_KEY

# Define a function to generate a title for a Wordpress page
def generate_title(text, redaction_type, audience, industry, language):
    # Define the agent profile and context parameters for the prompt
    agent_profile = "an opinion journalist, economy expert, and writer"
    context_params = f"working on a {redaction_type} wordpress article targeting a {audience} audience in the {industry} industry, written in {language} (use this params as metadata u dont need to write it in the text, just use it as context, Answer me only the result without extra text or data use maximum 30 words)"
    task = f"Generate a title for a Wordpress page about {text}"
    prompt = f"You are {agent_profile}, {context_params}. {task}."
    try:
        # Use OpenAI's API to generate a title based on the prompt
        response = openai.Completion.create(
            engine= OPENAI_ENGINE_ID,
            prompt=prompt,
            max_tokens=40,
            n=1,
            stop=None,
            temperature=0.7,
        )
        print('title')
        time.sleep(10)
        # Return the generated title as a string with leading/trailing white space removed
        return response.choices[0].text.strip()
    except Exception as e:
        # If there's an error with the OpenAI API, raise a ValueError with the error message
        raise ValueError(str(e))


# Define a function to generate an introduction to the topic
def generate_intro(text, redaction_type, audience, industry, language, previous_prompt_result):
    # Define the agent profile and prompt for the introduction
    agent_profile = "an opinion journalist, economy expert, and writer"
    context_params = f"working on a {redaction_type} wordpress article targeting a {audience} audience in the {industry} industry, written in {language} (use this params as metadata u dont need to write it in the text, just use it as context)"
    task = f"Write an introduction for a page about {text}"
    lastPromptContext = f"The title of the Wordpress page is:{previous_prompt_result} (use this params as metadata u dont need to write it in the text, just use it as context)"
    prompt = f"You are {agent_profile}, {context_params}. {task}. {lastPromptContext}"
    try:
        # Use OpenAI's API to generate an introduction based on the prompt
        response = openai.Completion.create(
            engine=OPENAI_ENGINE_ID,
            prompt=prompt,
            max_tokens=1200,
            n=1,
            stop=None,
            temperature=0.5,
        )
        print('intro')
        time.sleep(20)
        # Return the generated introduction as a string with leading/trailing white space removed
        return response.choices[0].text.strip()
    except Exception as e:
        # If there's an error with the OpenAI API, raise a ValueError with the error message
        raise ValueError(str(e))
    
# Define a function to generate a list of key points
def generate_points(text, redaction_type, audience, industry, language, previous_prompt_result):
    # Define the agent profile and prompt for the introduction
    agent_profile = "an opinion journalist, economy expert, and writer"
    context_params = f"working on a {redaction_type} article targeting a {audience} audience in the {industry} industry, written in {language} (use this params as metadata u dont need to write it in the text, just use it as context)"
    task = f"Write a List, of key points about {text}, this was my introduction {previous_prompt_result}"
    lastPromptContext = f"The intro of the Wordpress page is:{previous_prompt_result} (use this params as metadata u dont need to write it in the text, just use it as context)"
    prompt = f"You are {agent_profile}, {context_params}. {task}. {lastPromptContext}"    
    try:
        # Use OpenAI's API to generate an introduction based on the prompt
        response = openai.Completion.create(
            engine=OPENAI_ENGINE_ID,
            prompt=prompt,
            max_tokens=550,
            n=1,
            stop=None,
            temperature=0.6,
        )
        print('points')
        time.sleep(12)
        # Return the generated introduction as a string with leading/trailing white space removed
        return response.choices[0].text.strip()
    except Exception as e:
        # If there's an error with the OpenAI API, raise a ValueError with the error message
        raise ValueError(str(e))

# Define a function to generate a summary of conclusions
def generate_conclusions(text, redaction_type, audience, industry, language, previous_prompt_result):
    # Define the agent profile and prompt for the introduction
    agent_profile = "an opinion journalist, and writer, editor, storyteller, researcher"
    context_params = f"working on a {redaction_type} article targeting a {audience} audience in the {industry} industry, written in {language} (use this params as metadata u dont need to write it in the text, just use it as context)"
    task = f"Write some conclusions about {text}"
    lastPromptContext = f"The key points of the page are:{previous_prompt_result} (use this params as metadata u dont need to write it in the text, just use it as context)"
    prompt = f"You are {agent_profile}, {context_params}. {task}. {lastPromptContext}"    
    try:
        response = openai.Completion.create(
            engine=OPENAI_ENGINE_ID,
            prompt=prompt,
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.5,
        )
        print('conclusions')
        time.sleep(15)
        # Return the generated introduction as a string with leading/trailing white space removed
        return response.choices[0].text.strip()
    except Exception as e:
        # If there's an error with the OpenAI API, raise a ValueError with the error message
        raise ValueError(str(e))
    
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


# Define a function to generate an image using DALL-E
def generate_image(prompt):
    response = openai.Image.create(
    prompt=f"Generate an photo of {prompt}",
    n=1,
    size="512x512"
)
    print(prompt)
    return response['data'][0]['url']

# Define a function to send the generated page to Wordpress
def send_to_wordpress(title, content):
    # Set up the request headers with the user's login credentials
    headers = {"Authorization": f"Bearer {WORDPRESS_API_KEY}", "Content-Type": "application/json"}

    # Set up the request body with the post data
    data = {"title": title, "content": content, "status": "publish"}

    # Use a session object to reuse the same TCP connection for multiple requests
    with requests.Session() as session:
        session.headers.update(headers)

        # Send the POST request to create the new post
        try:
            response = session.post(WORDPRESS_URL, json=data, auth=(WORDPRESS_USER,WORDPRESS_API_KEY))
            response.raise_for_status()
            return response.json()
        except HTTPError as err:
            print(f"HTTP error: {err}")
            print(f"Response content: {err.response.content}")
            print(f"Response headers: {err.response.headers}")
        except RequestException as err:
            print(f"Request error: {err}")

# Define an API endpoint that generates a Wordpress page using GPT-3
@app.post("/generate")
def generate_wordpress_page(input_data: TextInput, redaction_type: str, language: str, audience: str, industry: str):
    try:
        # Generate the content for the Wordpress page
        # Step 1: Generate the title
        title = str(generate_title(input_data, redaction_type, audience, industry, language))
        previous_prompt_result = title

        # Step 2: Generate a prompt to generate a related image
        image_prompt = str(generate_image_prompt(title))

        # Step 3: Generate an image using dalle
        image_url = str(generate_image(image_prompt))
        
        # Step 4: Generate an introduction to the topic
        intro_text = str(generate_intro(input_data, redaction_type, audience, industry, language, previous_prompt_result))
        previous_prompt_result = intro_text

        # Step 5: Generate a list of key points
        points_text = str(generate_points(input_data, redaction_type, audience, industry, language, previous_prompt_result))
        previous_prompt_result = points_text

        # Step 6: Generate a summary of conclusions
        summary_text = str(generate_conclusions(input_data, redaction_type, audience, industry, language, previous_prompt_result))
        previous_prompt_result = summary_text

        # Step 7: Generate the final Wordpress page content
        page_content = f"""
        <p>{intro_text}</p>
        <img src="{image_url}">
        <h2>Key Points:</h2>
        <ul>{points_text}</ul>
        <h2>Summary:</h2>
        <p>{summary_text}</p>
        """

        # Send the page content to the Wordpress API
        send_to_wordpress(title, page_content)
        # Return the generated page content
        return {"page_content": page_content}

    except Exception as e:
        return {"error": str(e)}

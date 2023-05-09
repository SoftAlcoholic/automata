import openai
from fastapi import FastAPI
from pydantic import BaseModel
import requests


# Initialize the FastAPI app
app = FastAPI()

# Define a data model for the input text
class TextInput(BaseModel):
    text: str

# Initialize the OpenAI API client with your API key
from config import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY

# Define a function to generate a title for a Wordpress page
def generate_title(text, redaction_type, audience, industry, language):
    # Define the agent profile and context parameters for the prompt
    agent_profile = "an opinion journalist, economy expert, and writer"
    context_params = f"working on a {redaction_type} wordpress article targeting a {audience} audience in the {industry} industry, written in {language} (use this params as metadata u dont need to write it in the text, just use it as context)"
    task = f"Generate a title for a Wordpress page about {text}"
    prompt = f"You are {agent_profile}, {context_params}. {task}."
    try:
        # Use OpenAI's API to generate a title based on the prompt
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=32,
            n=1,
            stop=None,
            temperature=0.7,
        )
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
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1032,
            n=1,
            stop=None,
            temperature=0.5,
        )
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
    task = f"Write a List three key points about {text}"
    lastPromptContext = f"The intro of the Wordpress page is:{previous_prompt_result} (use this params as metadata u dont need to write it in the text, just use it as context)"
    prompt = f"You are {agent_profile}, {context_params}. {task}. {lastPromptContext}"    
    try:
        # Use OpenAI's API to generate an introduction based on the prompt
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=258,
            n=1,
            stop=None,
            temperature=0.6,
        )
        # Return the generated introduction as a string with leading/trailing white space removed
        return response.choices[0].text.strip()
    except Exception as e:
        # If there's an error with the OpenAI API, raise a ValueError with the error message
        raise ValueError(str(e))

# Define a function to generate a summary of the key points
def generate_conclusions(text, redaction_type, audience, industry, language, previous_prompt_result):
    # Define the agent profile and prompt for the introduction
    agent_profile = "an opinion journalist, economy expert, and writer"
    context_params = f"working on a {redaction_type} article targeting a {audience} audience in the {industry} industry, written in {language} (use this params as metadata u dont need to write it in the text, just use it as context)"
    task = f"Write some conclusions about {text}"
    lastPromptContext = f"The key points of the page are:{previous_prompt_result} (use this params as metadata u dont need to write it in the text, just use it as context)"
    prompt = f"You are {agent_profile}, {context_params}. {task}. {lastPromptContext}"    
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=258,
            n=1,
            stop=None,
            temperature=0.5,
        )
        # Return the generated introduction as a string with leading/trailing white space removed
        return response.choices[0].text.strip()
    except Exception as e:
        # If there's an error with the OpenAI API, raise a ValueError with the error message
        raise ValueError(str(e))


# Define the URL of the Wordpress API endpoint
WORDPRESS_API_URL = "http://192.168.0.39/pagab/w/wp-json/wp/v2/pages"

# Define a function to send the generated Wordpress page to the Wordpress API
def send_to_wordpress(title, content):
    # Define the request body
    data = {
        "title": title,
        "content": content,
        "status": "publish"
    }

    # Define the request headers
    headers = {
        "Authorization": "Bearer YOUR_WORDPRESS_API_TOKEN",
        "Content-Type": "application/json"
    }

    # Send the HTTP POST request to the Wordpress API
    response = requests.post(WORDPRESS_API_URL, json=data, headers=headers)

    # Check the response status code
    if response.status_code == 201:
        print("Page published successfully!")
    else:
        print("Failed to publish page. Response content:")
        print(response.content)

    
# Define an API endpoint that generates a Wordpress page using GPT-3
@app.post("/generate")
def generate_wordpress_page(input_data: TextInput, redaction_type: str, language: str, audience: str, industry: str):
    try:
        # Generate the content for the Wordpress page
        # Step 1: Generate the title
        title = generate_title(input_data, redaction_type, audience, industry, language)
        previous_prompt_result = title
        
        # Step 2: Generate an introduction to the topic
        intro_text = generate_intro(input_data, redaction_type, audience, industry, language, previous_prompt_result)
        previous_prompt_result = intro_text

        # Step 3: Generate a list of key points
        points_text = generate_points(input_data, redaction_type, audience, industry, language, previous_prompt_result)
        previous_prompt_result = points_text

        # Step 4: Generate a summary of the key points
        summary_text = generate_conclusions(input_data, redaction_type, audience, industry, language, previous_prompt_result)
        previous_prompt_result = summary_text

        # Step 5: Generate the final Wordpress page content
        page_content = f"""
        <h1>{title}</h1>
        <p>{intro_text}</p>
        <h2>Key Points:</h2>
        <ul>{points_text}</ul>
        <h2>Summary:</h2>
        <p>{summary_text}</p>
        """

        # Send the page content to the Wordpress API
        send_to_wordpress(title, page_content)

        #return {"response": response.text}
        return {"page_content": page_content}

    except Exception as e:
        return {"error": str(e)}
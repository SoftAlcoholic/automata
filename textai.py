import openai
from fastapi import FastAPI
from pydantic import BaseModel

# Initialize the FastAPI app
app = FastAPI()

# Define a data model for the input text
class TextInput(BaseModel):
    text: str

# Initialize the OpenAI API client with your API key
from config import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY

import openai

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
def generate_intro(text, redaction_type, audience, industry, language, lastPromptRes):
    # Define the agent profile and prompt for the introduction
    agent_profile = "an opinion journalist, economy expert, and writer"
    context_params = f"working on a {redaction_type} wordpress article targeting a {audience} audience in the {industry} industry, written in {language} (use this params as metadata u dont need to write it in the text, just use it as context)"
    task = f"Write an introduction for a page about {text}"
    lastPromptContext = f"The title of the Wordpress page is:{lastPromptRes} (use this params as metadata u dont need to write it in the text, just use it as context)"
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
def generate_points(text, redaction_type, audience, industry, language, lastPromptRes):
    # Define the agent profile and prompt for the introduction
    agent_profile = "an opinion journalist, economy expert, and writer"
    context_params = f"working on a {redaction_type} article targeting a {audience} audience in the {industry} industry, written in {language} (use this params as metadata u dont need to write it in the text, just use it as context)"
    task = f"Write a List three key points about {text}"
    lastPromptContext = f"The intro of the Wordpress page is:{lastPromptRes} (use this params as metadata u dont need to write it in the text, just use it as context)"
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
def generate_conclusions(text, redaction_type, audience, industry, language, lastPromptRes):
    # Define the agent profile and prompt for the introduction
    agent_profile = "an opinion journalist, economy expert, and writer"
    context_params = f"working on a {redaction_type} article targeting a {audience} audience in the {industry} industry, written in {language} (use this params as metadata u dont need to write it in the text, just use it as context)"
    task = f"Write some conclusions about {text}"
    lastPromptContext = f"The key points of the page are:{lastPromptRes} (use this params as metadata u dont need to write it in the text, just use it as context)"
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
    
# Define an API endpoint that generates a Wordpress page using GPT-3
@app.post("/generate")
def generate_wordpress_page(input_data: TextInput, redaction_type: str, language: str, audience: str, industry: str):
    try:
        # Generate the content for the Wordpress page
        # Step 1: Generate the title
        title = generate_title(input_data, redaction_type, audience, industry, language)
        lastPromptRes = title
        
        # Step 2: Generate an introduction to the topic
        intro_text = generate_intro(input_data, redaction_type, audience, industry, language, lastPromptRes)
        lastPromptRes = intro_text

        # Step 3: Generate a list of key points
        points_text = generate_points(input_data, redaction_type, audience, industry, language, lastPromptRes)
        lastPromptRes = points_text

        # Step 4: Generate a summary of the key points
        summary_text = generate_conclusions(input_data, redaction_type, audience, industry, language, lastPromptRes)
        lastPromptRes = summary_text

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
        #headers = {"Authorization": f"Bearer {os.environ.get('WORDPRESS_API_KEY')}"}
        #payload = {"content": page_content}
        #response = requests.post(f"{os.environ.get('WORDPRESS_WEBSITE_URL')}/wp-json/wp/v2/pages", headers=headers, data=payload)
        
        # Return the response from the Wordpress API
        #return {"response": response.text}
        return {"page_content": page_content}
    
    except Exception as e:
        return {"error": str(e)}
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

# Define a function to generate a title
def generate_title(text, redaction_type, audience, industry, language):
    try:
        prompt = f"Generate a title for a {redaction_type} Wordpress page about {text} that targets a {audience} audience in the {industry} industry written in {language}."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=32,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        raise ValueError(str(e))

# Define a function to generate an introduction to the topic
def generate_intro(text, audience, industry, language):
    try:
        prompt = f"Write an introduction to a Wordpress page about {text} that targets a {audience} audience in the {industry} industry written in {language}."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=256,
            n=1,
            stop="Key Points:",
            temperature=0.5,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        raise ValueError(str(e))

# Define a function to generate a list of key points
def generate_points(text, audience, industry, language):
    try:
        prompt = f"List three key points that should be included in a Wordpress page about {text} that targets a {audience} audience in the {industry} industry written in {language}."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=128,
            n=3,
            stop=None,
            temperature=0.6,
        )
        points_text = "\n".join([f"- {choice.text.strip()}" for choice in response.choices])
        return points_text
    except Exception as e:
        raise ValueError(str(e))

# Define a function to generate a summary of the key points
def generate_summary(text, audience, industry, language):
    try:
        prompt = f"Write a summary of the three key points for a Wordpress page about {text} that targets a {audience} audience in the {industry} industry written in {language}."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=128,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        raise ValueError(str(e))
    
# Define an API endpoint that generates a Wordpress page using GPT-3
@app.post("/generate")
def generate_wordpress_page(input_data: TextInput, redaction_type: str, language: str, audience: str, industry: str):
    try:
        # Generate the content for the Wordpress page
        # Step 1: Generate the title
        title = generate_title(input_data, redaction_type, audience, industry, language)

        # Step 2: Generate an introduction to the topic
        intro_text = generate_intro(input_data, audience, industry, language)

        # Step 3: Generate a list of key points
        points_text = generate_points(input_data, audience, industry, language)

        # Step 4: Generate a summary of the key points
        summary_text = generate_summary(input_data, audience, industry, language)

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

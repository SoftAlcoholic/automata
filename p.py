#import the required libraries
import openai
from fastapi import FastAPI
from pydantic import BaseModel
import requests
from requests.exceptions import HTTPError, RequestException

from config import OPENAI_API_KEY, OPENAI_ENGINE_ID
from main import generate_title

# Initialize the FastAPI app
app = FastAPI()

# Define a data model for the input text
class TextInput(BaseModel):
    text: str

# Initialize the OpenAI API client with your API key
openai.api_key = OPENAI_API_KEY

def keywords():
    title=generate_title('tip tecnologia','editor de tecnologia','latam','tecnologia','español')
    prompt= f"generate english keywords according to the following title {title} separate each word by commas, maximum 10, (use these parameters as metadata you don't need to write them in the text, just use them as context, remember that these words will be used to search for images appropriate to the theme)" 
    print(title)
    try:
        response = openai.Completion.create(
            engine=OPENAI_ENGINE_ID,
            prompt=prompt,
            max_tokens=20,
            n=1,
            stop=None,
            temperature=0.7,
        )
        # 
        return response.choices[0].text.strip()
    except Exception as e:
        # If there's an error with the OpenAI API, raise a ValueError with the error message
        raise ValueError(str(e))
         


# Define a function to generate a title for a Wordpress page
def generate_url_img():
    # Define the agent profile and context parameters for the prompt
    #
    prompt = keywords()
    print (prompt)
    try:
        # 
        url = "https://api.unsplash.com/photos/random"
        #url = "urn:ietf:wg:oauth:2.0:oob"
        params = {
            "client_id": "CSOqDW6-YJTSqTC9AJuIRtYa2mldEfNP0cN5tUY2c2A",
            "query": prompt,
            "order_by": 'relevant'      
        }

        # Realiza una solicitud GET a la API de Unsplash
        response = requests.get(url, params=params)
        
        # Analiza la respuesta JSON
        data = response.json()
        #print(data)
        
        # Extrae la URL de la imagen de la respuesta
        imagen_url = data["urls"]['regular']
        
        return imagen_url
    
    except Exception as e:
        # If there's an error with the OpenAI API, raise a ValueError with the error message
        raise ValueError(str(e))
    
print (str(generate_url_img()))
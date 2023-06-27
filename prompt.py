import openai 
import os 
import re
from dotenv import load_dotenv 

""" Fetch API key """
load_dotenv()
openai.api_key = os.getenv("API_KEY")

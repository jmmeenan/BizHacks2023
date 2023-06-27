import openai 
import os 
import re
from dotenv import load_dotenv 

""" Fetch API key """
load_dotenv()
openai.api_key = os.getenv("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")

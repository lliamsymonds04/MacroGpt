from openai import OpenAI
import os
from dotenv import load_dotenv

def is_client_valid(c: OpenAI):
    try:
        c.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say this is a test"}],
            max_tokens=1
        )
    except:
        return False
    else:
        return True
    

def get_ai_client() -> OpenAI:
    load_dotenv()
    if os.environ.get("OPENAI_API_KEY"):
        c = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY")
        )
        if is_client_valid(c):
            print("OpenAI API key loaded from environment.")
            return c
        
    user_key = input("Input OpenAI API key: ")
    if user_key == "":
        return
    
    c = OpenAI(
        api_key=user_key
    )
    valid = is_client_valid(c)
    if valid:
        print("AI successfully loaded!")
        return c
    else:
        print("Invalid key, try again...")
        return get_ai_client()
    
from openai import OpenAI
import re
import os
from dotenv import load_dotenv

system_prompt = open("SystemMessage.txt", "r").read()

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
    

def prompt_ai(client: OpenAI, food: str):
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": food}],
    )


def get_protein_and_calories(msg: str):
    if msg.find("Total Protein: ") >= 0 and msg.find("Total Calories: ") >= 0:
        lines = msg.split("\n")
        result = []
        for line in lines:
            num = re.findall(r'\d+', line)[0]
            result.append(int(num))
        return result
    else:
        return
        

def get_macros_prompt(client: OpenAI, user_food: str):
    attempts = 3
    while attempts > 0:
        attempts -= 1
        result = prompt_ai(client, user_food)
        macros = get_protein_and_calories(result.choices[0].message.content)
        if macros:
            print("Total Protein: " + str(macros[0]) + "g")
            print("Total Calories: " + str(macros[1]))
            break

    if attempts == 0:
        print("Failed to get macros of what you described. Please try again.")



def main():
    client = get_ai_client()
    
    if client:
        while True:
            user_input = input("Describe the food: ")
            if user_input:
                get_macros_prompt(client, user_input)
            else:
                break


if __name__ == "__main__":
    main()
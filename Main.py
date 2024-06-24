from Client import get_ai_client

from openai import OpenAI
import re

food_macros = open("GptSystemMessages/FoodMacros.txt", "r").read()

def prompt_ai_for_macros(client: OpenAI, food: str):
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": food_macros}, {"role": "user", "content": food}],
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
        result = prompt_ai_for_macros(client, user_food)
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
            mode_input = input("Selected mode (image = 'i', text = 't'): ")
            if mode_input == "i":
                print("temp")
            elif mode_input == "t":
                while True:
                    user_input = input("Describe the food: ")
                    if user_input:
                        get_macros_prompt(client, user_input)
                    else:
                        break
            else:
                break


if __name__ == "__main__":
    main()
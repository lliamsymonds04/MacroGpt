from Client import get_ai_client
from ImageHandling import upload_image_to_imgur, prompt_ai_with_image, delete_imgur_img

from openai import OpenAI
import re

food_macros_msg = open("GptSystemMessages/FoodMacros.txt", "r").read()

def prompt_ai_for_macros(client: OpenAI, food: str):
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": food_macros_msg}, {"role": "user", "content": food}],
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

def image_helper(client: OpenAI, image_url):
    result = prompt_ai_with_image(client, image_url)
    food_description = result.choices[0].message.content
    if food_description != "Failed":
        get_macros_prompt(client, food_description)
    else:
        print("Failed to determine food in the image. Please try again")


# /Users/pjinm/OneDrive/Pictures/MacroGpt/scrambled-eggs-and-crispy-bacon.jpg
def main():
    client = get_ai_client()
    
    if client:
        while True:
            mode_input = input("Selected mode (image = 'i', text = 't'): ")
            if mode_input == "i":
                user_input = input("Image Path/url: ")
                if user_input:
                    if user_input.find("https://") >= 0: #url
                        image_helper(client, user_input)
                    else:
                        result = upload_image_to_imgur(user_input)
                        image_helper(client, result["link"])
                        delete_imgur_img(result["deletehash"])

            elif mode_input == "t":
                user_input = input("Describe the food: ")
                if user_input:
                    get_macros_prompt(client, user_input)

            else:
                break


if __name__ == "__main__":
    main()
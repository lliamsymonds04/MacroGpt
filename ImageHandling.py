import json
import requests
import os
from openai import OpenAI

food_image_msg = open("GptSystemMessages/FoodImage.txt", "r").read()


# Function to upload image to Imgur
# def upload_image_to_imgur(image_path, client_id):
#     url = "https://api.imgur.com/3/upload"
#     headers = {"Authorization": f"Client-ID {client_id}"}
#     with open(image_path, "rb") as image_file:
#         data = {"image": image_file.read()}
#     response = requests.post(url, headers=headers, files=data)
#     if response.status_code == 200:
#         return response.json()["data"]["link"]
#     else:
#         response.raise_for_status()

imgur_url = "https://api.imgur.com/3/image"
image_types = ["jpeg", "jpg", "png"]

def get_imgur_api_key():
    return os.environ.get("Imgur_Bearer")

def check_image_type(image_path: str):
    for image_type in image_types:
        if image_path.find(image_type) >= 0:
            return True
        
    return False


def upload_image_to_imgur(image_path: str):
    if not (os.path.isfile(image_path) and check_image_type(image_path)):
        print("File provided is not a valid image")
        return

    api_key = get_imgur_api_key()

    if api_key:
        split_path = image_path.split("/")
        file_name = split_path[len(split_path) - 1]

        files=[
        ('image',(file_name,open(image_path,'rb'),'image/png'))
        ]
        headers = {
        'Authorization': 'Bearer ' + api_key
        }
        response = requests.post(imgur_url, headers=headers, files=files)

        result = response.json()
        if result["success"]:
            return result["data"]
        else:
            print("failed")
    else:
        print("No api key found for Imgur. Please set the environment variable 'Imgur_Bearer'")



def prompt_ai_with_image(client: OpenAI, image_url: str):
    return client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": food_image_msg},
            {"role": "user", "content": [{
                "type": "image_url",
                "image_url": {"url": image_url},
            }]},
        ],
        max_tokens=300,
    )

def delete_imgur_img(deletehash: str):
    api_key = get_imgur_api_key()
    if api_key:
        url = f"https://api.imgur.com/3/image/{deletehash}"
        headers = {
        'Authorization': 'Bearer ' + api_key
        }
        requests.delete(url, headers=headers)
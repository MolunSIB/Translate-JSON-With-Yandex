import requests
import json

IAM_TOKEN = ''
folder_id = ''
target_language = ''
source_language = ''
file_name = ''
extension = ''
json_item_count = 0

def send_to_translate(input_text):
    body = {
        "targetLanguageCode": target_language,
        "sourceLanguageCode": source_language,
        "texts": input_text,
        "folderId": folder_id,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(IAM_TOKEN)
    }

    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
        json = body,
        headers = headers
    )
    response_json = response.json()
    text = response_json["translations"][0]["text"]
    #print(type(text))
    texten = text.encode()
    #print(type(texten))
    textde = texten.decode()
    #print(type(textde))
    return text

def read_JSON():
    global json_item_count
    data = {}
    with open(file_name+"_"+source_language+extension, encoding='utf-8') as json_file:
        data = json.load(json_file)
        json_item_count = len(data)
        #print(len(data))
    print("JSON-файл прочитан из "+file_name+"_"+source_language+extension)
    return data

def write_JSON(data):
    with open(file_name+"_"+target_language+extension,'w',encoding='utf-8') as outfile:
        end_data = json.dumps(data,ensure_ascii=False)
        json.dump(data,outfile,ensure_ascii=False,indent=4)
    print("JSON-файл записан в "+file_name+"_"+target_language+extension)

def translate_json_file(data):
    translated_data = data
    i = 0
    for key in data:
        text = data[key]
        translated_text = send_to_translate(text)
        translated_data[key] = translated_text
        i+=1
        print(f"Переведено {i}/{json_item_count}")
    return translated_data

def load_settings():
    global IAM_TOKEN
    global folder_id
    global target_language
    global source_language
    global file_name
    global extension
    
    print("Начинаю считывать настройки")
    with open("settings.json") as file:
        settings = json.load(file)
        IAM_TOKEN = settings["IAM_TOKEN"]
        folder_id = settings["folder_id"]
        target_language = settings["target_language"]
        source_language = settings["source_language"]
        file_name = settings["file_name"]
        extension = settings["extension"]
    print("Настройки записаны!")

def main():
    print("Программа запущена!")
    load_settings()
    data = read_JSON()
    translated_data = translate_json_file(data)
    write_JSON(translated_data)
    print("Программа закончила работу!")
    
    
if __name__ == "__main__":
    main()

import os
from google.cloud import translate_v2

### Initialize Environment
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'Function//Google_Vision_API.json'
# Instantiates a client
client = translate_v2.Client()

txt = " ToY Shop GENUINE HANDCRAFTED TOYS VectorStock"
target = 'vi'
lang_list = client.get_languages()
out = client.translate(txt,target_language=target,source_language='en')
print(out["translatedText"])
for i in lang_list:
    print(i)
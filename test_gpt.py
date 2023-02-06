import json
import openai
import deepl
from gtts import gTTS


def get_api_keys():
    with open("api_keys.json") as f:
        return json.load(f)

dummy = "Samuel, Ava and Mateo were having the best time ever on their pirate ship, the force of the waves rocking the ship back and forth. They had just raided a nearby town and were now headed back to their hidden cove, laden with treasure. Samuel and Mateo were tasked with guarding the treasure while Ava steered the ship. It was a dark and stormy night, but the three friends were not afraid. Suddenly, out of the darkness, a giant octopus appeared, its tentacles reaching for the ship. Mateo and Samuel grabbed their swords and began hacking at the tentacles while Ava steered the ship away. Just when it seemed like they might make it away, the octopus pulled the ship under the water with one final tentacle. Down, down, down they went, the water getting colder and darker the further they sank. Suddenly, they saw a faint light in the distance and swam towards it. They emerged into a huge cavern, illuminated by thousands of glowing jellyfish. In the center of the cavern was a giant treasure chest, guarded by a sleeping dragon. The friends were about to turn back when Mateo spotted a key hanging from the dragon's neck. He crept up quietly and grabbed the key, then ran back to the others. They quickly unlocked the chest and began scooping out the treasure. The dragon woke up with a start and began to chase them, but they were already swimming back to the surface, the treasure clutched tightly in their hands. They made it back to their ship and sailed away, laughing and cheering, their adventure finally over."


openai.api_key = get_api_keys()[0]["openai_api_key"]

prompt = "Write a bed time story about pirats for kids. Include the names Ava, Samuel and Mateo. Maximum 500 words."

response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    temperature=1,
    max_tokens=700, # calculate 1 token per word
)

text = response.choices[0].text

auth_key = get_api_keys()[1]["deepl_api_key"]
translator = deepl.Translator(auth_key)

result = translator.translate_text(f"{text}", target_lang="EN-GB")


language = 'en'

myobj = gTTS(text=f"{result}", lang=language, slow=False)

myobj.save("story_ger.mp3")

print(result)



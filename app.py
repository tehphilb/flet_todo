from flet import *
import openai
import deepl
from gtts import gTTS
import json

# dummy = open("text.txt", "r")


def get_api_keys():
    with open("api_keys.json") as f:
        return json.load(f)


def main(page):
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'

    create_story_input = Container(
        padding=padding.only(top=20, left=20, right=20,),
        content=TextField(label="Your thought",
                          autofocus=False,
                          multiline=True,
                          min_lines=1,
                          max_lines=5,
                          hint_text="What, possibly who, do you want your story to be about? Give me a few clues...",
                          hint_style=TextStyle(color="#C7C7C7", weight=FontWeight.W_100,)))

    story = Container(
        padding=padding.only(left=20,
                             right=20,
                             ),
        content=Column(
            controls=[]
        ),)

    def create_audio(result):
        language = 'en'
        myobj = gTTS(text=f"{result}", lang=language, slow=False)
        myobj.save("story_ger.mp3")

    def get_data():
        user_promt = str(create_story_input.content.value)
        openai.api_key = get_api_keys()[0]["openai_api_key"]

        prompt = f"{user_promt}, use maximum 500 words."

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            temperature=1,
            max_tokens=700,  # calculate 1 token per word
        )

        text = response.choices[0].text

        auth_key = get_api_keys()[1]["deepl_api_key"]
        translator = deepl.Translator(auth_key)

        result = translator.translate_text(f"{text}", target_lang="EN-GB")

        return result

    def btn_click(e):
        story_text = get_data()
        
        story.content.controls.append(
            Text(story_text))
        create_story_input.content.value = ""
        page.update()

    page.add(
        Container(
            width=280,
            height=600,
            bgcolor="#0f0f0f",
            border_radius=40,
            border=border.all(0.5, "white"),
            clip_behavior=ClipBehavior.ANTI_ALIAS,
            content=Column(
                auto_scroll=True,
                scroll='hidden',
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Container(height=40),
                    create_story_input,
                    Container(height=20),
                    ElevatedButton("Create story", on_click=btn_click),
                    story,
                ]
            )
        )
    )


app(target=main)

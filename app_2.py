
from flet import *
from datetime import datetime
import sqlite3

# Form class


class FormContainer(UserControl):
    def __init__(self):
        # self.func = func
        super().__init__()

    def build(self):
        return Container(
            width=280,
            height=0,
            bgcolor="#f0f0f0",
            opacity=0,
            border_radius=0,
            padding=padding.only(top=45, bottom=45),
            animate=animation.Animation(500, "decelerate"),
            animate_opacity=280,
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[TextField(
                    width=255,
                    filled=True,
                    color="black87",
                    cursor_color="black87",
                    border_color="black87",
                    border_width=0.3,
                    hint_text="Write something...",
                    hint_style=TextStyle(color="black87", weight=FontWeight.W_200),
                    text_style=TextStyle(color="black87", weight=FontWeight.W_300),
                    cursor_width=0.4,
                    multiline=True,
                    min_lines=1,
                    max_lines=2,
                ),
                IconButton(
                    content=Text("Add TODO"),
                    width=110,
                    style=ButtonStyle(
                        bgcolor="black87",
                        shape=StadiumBorder(),
                    ),
                )
                ]
            )
        )


def main(page: Page):
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'

    # funtion to show/hide form container
    def createTodo(e):
        if form.height != 200:
            
            form.height, form.opacity, form.border_radius = 200, 1, 20
            form.update()
        else:
            form.height, form.opacity, form.border_radius = 0, 0, 0
            form.update()

    # here Appbar (the white one of top of the page)
    page.appbar = AppBar(
        title=Text("TODO", color="black87", size=24),
        center_title=True,
        elevation=4,
        bgcolor="#f0f0f0",
    )

    # here main column or entiry point of main UI
    _main_column_ = Column(
        scroll='hidden',
        expand=True,
        alignment=MainAxisAlignment.CENTER,
        controls=[
            Container(padding=padding.only(left=20,
                                           right=20),
                      content=Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Text("TODO", size=24),
                    IconButton(icon=icons.ADD,
                               icon_color="#f0f0f0",
                               on_click=createTodo,)
                ],
            ),),
            Container(
                alignment=alignment.center,
                padding=padding.only(top=35, left=10, right=10),
                content=Divider(height=1, color="#f0f0f0"),
            ),
        ],
    )

    # the general UI will copy that of a mobile app
    page.add(
        # this is just a mobile feeling container
        Container(
            width=280,
            height=600,
            bgcolor="#0f0f0f",
            border_radius=40,
            border=border.all(0.5, "white"),
            padding=padding.only(top=100),
            clip_behavior=ClipBehavior.HARD_EDGE,
            content=Column(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    # main column here
                    _main_column_,
                    # form class here
                    FormContainer(),
                ]
            )
        )
    )

    page.update()

    # sets the long element index as a variable so it can be called faster
    # now it can be called from wherever in the code faster and easier
    # route is page.add.Container => Column.FormContainer => Container
    form = page.controls[0].content.controls[1].controls[0]

if __name__ == "__main__":
    app(target=main)

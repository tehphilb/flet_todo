# https: // www.youtube.com/watch?v = qRqxAUC_4oA & t = 3500s
from flet import *
from datetime import datetime
import sqlite3

# Form class


class FormContainer(UserControl):
    def __init__(self, func):
        self.func = func
        super().__init__()

    def build(self):
        return Container(
            width=280,
            height=0,
            bgcolor="#f0f0f0",
            opacity=0,
            border_radius=0,
            padding=padding.only(top=25, bottom=35),
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
                    hint_style=TextStyle(
                        color="black87", weight=FontWeight.W_200),
                    text_style=TextStyle(
                        color="black87", weight=FontWeight.W_300),
                    cursor_width=0.4,
                    multiline=True,
                    min_lines=1,
                    max_lines=2,
                ),
                    Container(height=5),                   
                    IconButton(
                        icon=icons.ADD,
                        icon_size=32,
                        icon_color="black87",
                    # content=Text("Add TODO"),
                    # width=110,
                    # style=ButtonStyle(
                    #     bgcolor="black87",
                    #     shape=StadiumBorder(),
                    # ),
                    on_click=self.func,
                )]
            )
        )

# create todo class


class CreateTodo(UserControl):
    def __init__(self, todo: str, date: str):
        self.todo = todo
        self.date = date
        super().__init__()

    def deleteEditTodo(self, name, color):
        return IconButton(
            icon=name,
            icon_size=18,
            icon_color=color,
            animate_opacity=280,
            on_click=None,
        )

    def build(self):
        return Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                Container(
                    width=260,
                    height=60,
                    border=border.all(0.3, "white"),
                    border_radius=5,
                    # on_hover=None,
                    clip_behavior=ClipBehavior.ANTI_ALIAS,
                    padding=10.0,
                    content=Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            Column(
                                spacing=1,
                                alignment=MainAxisAlignment.CENTER,
                                controls=[
                                    Text(value=self.todo, size=12),
                                    Text(value=self.date, size=8,
                                         color="white54"),
                                ]
                            ),
                            ##TODO: replace below with dropdown and 3 dot menu
                            # Icons delete and Exit
                            Row(
                                spacing=1,
                                alignment=MainAxisAlignment.SPACE_EVENLY,
                                controls=[
                                    # Calls deleteTodo function
                                    self.deleteEditTodo(icons.DELETE, "red"),
                                    self.deleteEditTodo(icons.EDIT, "green"),
                                ],
                            )
                        ]
                    )

                )])


def main(page: Page):
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'

    # datetime function
    def dateTimeFunc():
        return datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    # create tot input screen

    def createTodoScreen(e):
        dateTime = dateTimeFunc().split(" ")[0]

        # use form variable to get data from tesxtfield
        if form.content.controls[0].value:  # checks textflied value
            _main_column_.controls.append(
                # create an instance of CreateTodo class
                CreateTodo(
                    # todo takes two arguments
                    form.content.controls[0].value,
                    dateTime,
                )
            )
            _main_column_.update()

            createTodo(e)

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
            # Container(
            #     alignment=alignment.center,
            #     padding=padding.only(top=35, left=10, right=10),
            #     content=Divider(height=1, color="#f0f0f0"),
            # ),
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
            clip_behavior=ClipBehavior.ANTI_ALIAS,
            content=Column(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    # main column here
                    _main_column_,
                    # form class here
                    FormContainer(lambda e: createTodoScreen(e)),
                ]
            )
        )
    )

    page.update()

    # sets the long element index as a variable so it can be called faster
    # now it can be called from wherever in the code faster and easier
    # route is page.add.Container => Column.FormContainer => Container
    form = page.controls[0].content.controls[1].controls[0]
    print(form.content.controls[0].value)


if __name__ == "__main__":
    app(target=main)

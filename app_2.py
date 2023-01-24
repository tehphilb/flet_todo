from flet import *
from datetime import datetime
import sqlite3

# Database CRUD class


class DataBase:
    def connectToDatabase():
        try:
            db = sqlite3.connect("data.db")
            cur = db.cursor()
            cur.execute(
                "CREATE TABLE if not exists todos (id INTEGER PRIMARY KEY AUTOINCREMENT, Todo TEXT NOT NULL, Date TEXT NOT NULL)")
            return db
        except Exception as e:
            print(e)

    def readDatabase(db):
        cur = db.cursor()
        cur.execute("SELECT id, Todo, Date From todos")
        records = cur.fetchall()
        return records

    def writeDatabase(db, values):
        cur = db.cursor()
        cur.execute("INSERT INTO todos (Todo, Date) VALUES (?,?)", values)
        db.commit()

    def deleteDatabase(db, id):
        cur = db.cursor()
        # TODO: id would be better as the todo text
        cur.execute("DELETE FROM todos WHERE id=?", (id,))
        db.commit()

    def updateDatabase(db, values):
        cur = db.cursor()
        #print(values)
        cur.execute("UPDATE todos SET Todo=? WHERE id=?", values)
        db.commit()

    def getTodoId(db, value):
        cur = db.cursor()
        cur.execute("SELECT id FROM todos WHERE Todo=?", (value,))
        todo_id = cur.fetchone()
        if todo_id:
            return todo_id[0]
        else:
            return None


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
                        on_click=self.func,

                )]
            )
        )


# create todo class


class CreateTodo(UserControl):
    def __init__(self, todo: str, date: str, func1, func2):
        # create two arguments to pass in the delete function and edit function when creating an instance of it
        self.todo = todo
        self.date = date
        self.func1 = func1
        self.func2 = func2
        super().__init__()

    def deleteEditTodo(self, name, color, func):
        return IconButton(
            icon=name,
            icon_size=18,
            icon_color=color,
            animate_opacity=280,
            opacity=0,
            on_click=lambda e: func(self.getContainerInstanace()),
        )

    def getContainerInstanace(self):
        return self

    def showIcons(self, e):
        if e.data == 'true':
            # index of each icon
            (e.control.content.controls[1].controls[0].opacity,
             e.control.content.controls[1].controls[1].opacity) = (
                1, 1
            )
            e.control.content.update()
        else:
            (e.control.content.controls[1].controls[0].opacity,
             e.control.content.controls[1].controls[1].opacity) = (
                0, 0
            )
            e.control.content.update()

    def build(self):
        return Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                Container(
                    width=260,
                    height=60,
                    border=border.all(0.3, "white"),
                    border_radius=5,
                    on_hover=lambda e: self.showIcons(e),
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
                                ],
                            ),
                            # TODO: replace below with dropdown and 3 dot menu
                            # Icons delete and Exit
                            Row(
                                spacing=0,
                                alignment=MainAxisAlignment.SPACE_EVENLY,
                                controls=[
                                    # Calls deleteTodo function
                                    self.deleteEditTodo(
                                        icons.CLOSE_SHARP, "white", self.func1),
                                    self.deleteEditTodo(
                                        icons.MODE_EDIT_OUTLINED, "white", self.func2),
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
        return datetime.now().strftime("%d.%b.%Y %H:%M:%S")

    # create todo input screen
    def createTodoScreen(e):
        dateTime = dateTimeFunc()

        # opens connection to db and retun database object
        db = DataBase.connectToDatabase()
        # write to database the todo and date
        DataBase.writeDatabase(db, (form.content.controls[0].value, dateTime))
        # close connection to db
        db.close()

        # use form variable to get data from tesxtfield
        if form.content.controls[0].value:  # checks textflied value
            _main_column_.controls.append(
                # create an instance of CreateTodo class
                CreateTodo(
                    # todo takes two arguments
                    form.content.controls[0].value,
                    dateTime,
                    # now the intance takes two arguments when called...
                    deleteTodoFunction,
                    updateTodoFunction,
                )
            )
            _main_column_.update()

            # call show hide function
            createTodoForm(e)
        else:
            db.close()  # close connection to db even if no data is entered
            pass

    def deleteTodoFunction(e):
        db = DataBase.connectToDatabase()
        # get todo value
        value = e.controls[0].controls[0].content.controls[0].controls[0].value
        # get todo id
        todoId = DataBase.getTodoId(db, value)
        # delete from database
        DataBase.deleteDatabase(db, todoId)
        # close connection to db
        db.close()

        # when want to delete a todo, recall that these instances are in a list => so that means it can simply be removed from the list
        _main_column_.controls.remove(e)  # e is the instance itself
        _main_column_.update()

    def updateTodoFunction(e):
        form.height, form.opacity, form.border_radius = 200, 1, 20  # show form
        (
            form.content.controls[0].value,
            # changing the button function and icon from add to update
            form.content.controls[2].icon,
            form.content.controls[2].on_click,
        ) = (
            # this is the instant value of the todo
            e.controls[0].controls[0].content.controls[0].controls[0].value,
            # new icon for update
            icons.AUTORENEW_OUTLINED,
            lambda _: finalizeUpdate(e)
        )
        form.update()

    def finalizeUpdate(e):
        db = DataBase.connectToDatabase()
        # get todo value from the instance
        value = e.controls[0].controls[0].content.controls[0].controls[0].value
        # get new todo value from the form
        new_value = form.content.controls[0].value
        # get todo id
        todoId = DataBase.getTodoId(db, value)
        # # delete from database
        DataBase.updateDatabase(db, (new_value, todoId))
        # close connection to db
        db.close()


        # update the todo
        e.controls[0].controls[0].content.controls[0].controls[0].value = form.content.controls[0].value
        e.controls[0].controls[0].content.update()
        # show hide form
        createTodoForm(e)

    # funtion to show/hide form container

    def createTodoForm(e):
        if form.height != 200:
            form.height, form.opacity, form.border_radius = 200, 1, 20
            form.update()
        else:
            # clear textfield, change icon to add, change button function to createTodoScreen
            form.height, form.opacity, form.border_radius = 0, 0, 0
            form.content.controls[0].value = ""  # clear textfield,
            form.content.controls[2].icon = icons.ADD  # change icon to add,
            form.content.controls[2].on_click = lambda e: createTodoScreen(
                e)  # change button function to createTodoScreen

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
                               on_click=createTodoForm,)
                ],
            ),),
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

    # display the db data open connection to db
    db = DataBase.connectToDatabase()
    # get data from db and show in reverse order
    for todo in DataBase.readDatabase(db)[::-1]:
        # append the data to the main column
        _main_column_.controls.append(
            # create an instance of CreateTodo class
            CreateTodo(
                todo[1],
                todo[2],
                deleteTodoFunction,
                updateTodoFunction,
            )
        )

        _main_column_.update()


if __name__ == "__main__":
    app(target=main)

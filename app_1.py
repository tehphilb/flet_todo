from flet import *
import sqlite3
import datetime as dt

# Create a database or connct to it
conn = sqlite3.connect("data.db", check_same_thread=False)
# Create a cursor
cur = conn.cursor()
# Create a table
cur.execute("""CREATE TABLE if not exists todos(
    id integer PRIMARY KEY AUTOINCREMENT,
    todo text)""")
# Commit changes
conn.commit()


class TodoApp(UserControl):
    def __init__(self):
        super().__init__()
        # List Data
        self.allData = ListView()
        self.addData = TextField(label="Enter something...", expand=True)
        self.editData = TextField(label="Edit data")

    def now(self):
        return dt.datetime.now().strftime('%d.%m.%Y, %H:%M')

    # Call getAllTodos to refresh data
    def refreshData(self):
        self.allData.controls.clear()
        self.getAllTodos()
        self.page.update()

    # Delete todo
    def deleteTodo(self, todo, alertDialog):
        cur.execute("delete from todos where id = ? ", [todo])
        conn.commit()
        # Close alert dialog
        alertDialog.open = False
        # Call getAllTodos to refresh data
        self.refreshData()

    # Edit todo
    def editTodo(self, id, todo, alertDialog):
        cur.execute("update todos SET todo = ? where id = ?", (todo, id))
        conn.commit()
        # Close alert dialog
        alertDialog.open = False
        # Call getAllTodos to refresh data
        self.refreshData()

    # Show delete/edit alert dialog
    def editTodos(self, e):
        # Get ID from data
        idEdit = e.control.subtitle.value
        # Edit textedit to value todo from listtile
        self.editData.value = e.control.title.value
        self.update()
        # Open alert dialog
        alertDialog = AlertDialog(
            title=Text(f"Edit id {idEdit}"),
            content=self.editData,
            # Button actions
            actions=[
                # Delete todo button
                ElevatedButton("Delete TODO",
                               color="white",
                               bgcolor="red",
                               on_click=lambda e:self.deleteTodo(idEdit, alertDialog)),
                # Save button
                TextButton("Save",
                           on_click=lambda e:self.editTodo(idEdit, self.editData.value, alertDialog))
            ],
            actions_alignment="spaceBetween",
        )
        self.page.dialog = alertDialog
        alertDialog.open = True
        # Update data
        self.page.update()

    # Get all todos and render ListTile
    def getAllTodos(self):
        cur.execute("select * from todos")
        allTodos = cur.fetchall()
        for todo in allTodos:
            self.allData.controls.append(
                ListTile(
                    # Show todo
                    title=Text(todo[1]),
                    # Show ID
                    subtitle=Text(todo[0]),
                    on_click=self.editTodos
))
        self.update()

    # Lifecycle for call getAllTodos
    def did_mount(self):
        self.getAllTodos()

    # Add new todo
    def addNewData(self, e):
        cur.execute("insert into todos (todo) values (?)",
                    [self.addData.value])
        conn.commit()
        # Clear data and call again
        self.allData.controls.clear()
        self.getAllTodos()
        self.page.update()

    # Build UI
    def build(self):
        return Column(width=600, controls=[
            Row(alignment=MainAxisAlignment.CENTER,
                controls=[Text("ToDo's", size=30)]),
            Row([
                self.addData,
                FloatingActionButton(
                    icon=icons.ADD, on_click=self.addNewData)]),
            self.allData
            ])

def main(page: Page):
    page.title = "ToDo App"
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"
    page.update()

    # Create application instance
    app = TodoApp()

    # Add application's root control to the page
    page.add(app)

app(target=main)

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import calendar
from datetime import datetime
import psycopg2


class RegistrationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conn = psycopg2.connect(
            host="localhost",  # Your system IP
            database="Attendance",  # Your PostgreSQL database name
            user="postgres",  # Your PostgreSQL username
            password="sai@123",  # Your PostgreSQL password
            port=5432
        )
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # Create a table for storing employee details
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id SERIAL PRIMARY KEY,
            employee_name TEXT NOT NULL,
            employee_id TEXT NOT NULL UNIQUE
        )
        """)
        self.conn.commit()

    def register_employee(self):
        employee_name = self.ids.employee_name_input.text.strip()
        employee_id = self.ids.employee_id_input.text.strip()

        if employee_name and employee_id:
            try:
                # Insert the employee details into the database
                self.cursor.execute(
                    "INSERT INTO employees (employee_name, employee_id) VALUES (%s, %s)",
                    (employee_name, employee_id)
                )
                self.conn.commit()
                self.manager.current = "login"
            except psycopg2.IntegrityError:
                self.conn.rollback()
                self.ids.message_label.text = "Employee ID already exists!"
            except Exception as e:
                self.conn.rollback()
                self.ids.message_label.text = f"Error: {str(e)}"
        else:
            self.ids.message_label.text = "Employee Name and ID cannot be empty!"


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conn = psycopg2.connect(
            host="localhost",  # Your system IP
            database="Attendance",  # Your PostgreSQL database name
            user="postgres",  # Your PostgreSQL username
            password="sai@123",  # Your PostgreSQL password
            port=5432
        )
        self.cursor = self.conn.cursor()

    def validate_credentials(self):
        username = self.ids.username_input.text.strip()
        password = self.ids.password_input.text.strip()

        if username and password:
            # Validate the credentials against the database
            self.cursor.execute(
                "SELECT * FROM employees WHERE employee_name = %s AND employee_id = %s",
                (username, password)
            )
            result = self.cursor.fetchone()
            if result:
                self.manager.get_screen("home").logged_in_user = username
                self.manager.get_screen("home").ids.welcome_label.text = f"Welcome, {username}!"
                self.manager.current = "home"
                self.ids.username_input.text = ""
                self.ids.password_input.text = ""
            else:
                self.ids.message_label.text = "Invalid username or password!"
        else:
            self.ids.message_label.text = "Please fill in both fields!"


class HomeScreen(Screen):
    logged_in_user = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_date = None
        self.create_calendar()

    def create_calendar(self):
        now = datetime.now()
        year, month = now.year, now.month

        calendar_layout = GridLayout(cols=7, size_hint=(1, 1))

        # Add day names
        for day in ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]:
            calendar_layout.add_widget(Label(text=day, bold=True, color=(0, 0, 0, 1)))

        # Add days of the month
        cal = calendar.Calendar()
        for day in cal.itermonthdays(year, month):
            if day == 0:
                calendar_layout.add_widget(Label(text=""))  # Empty for padding
            else:
                btn = Button(text=str(day), on_press=self.select_date)
                btn.date_info = (day, month, year)  # Store date info
                calendar_layout.add_widget(btn)

        self.ids.calendar_container.add_widget(calendar_layout)

    def select_date(self, instance):
        day, month, year = instance.date_info
        self.selected_date = (day, month, year)
        popup = Popup(
            title="Selected Date",
            content=Label(text=f"Selected Date: {day}-{month}-{year}"),
            size_hint=(0.6, 0.4),
        )
        popup.open()

    def store_date_and_proceed(self):
        if not self.selected_date:
            popup = Popup(
                title="Error",
                content=Label(text="No date selected!"),
                size_hint=(0.6, 0.4),
            )
            popup.open()
            return

        if not self.logged_in_user:
            popup = Popup(
                title="Error",
                content=Label(text="No user logged in!"),
                size_hint=(0.6, 0.4),
            )
            popup.open()
            return

        day, month, year = self.selected_date
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        # Store in PostgreSQL database
        self.conn = psycopg2.connect(
            host="localhost",  # Your system IP
            database="Attendance",  # Your PostgreSQL database name
            user="postgres",  # Your PostgreSQL username
            password="sai@123",  # Your PostgreSQL password
            port=5432
        )
        self.cursor = self.conn.cursor()

        # Create the attendance table if it doesn't exist
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id SERIAL PRIMARY KEY,
            username TEXT,
            date TEXT,
            time TEXT,
            day TEXT,
            month INTEGER,
            year INTEGER
        )
        """)

        # Insert the attendance record
        self.cursor.execute("""
        INSERT INTO attendance (username, date, time, day, month, year)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (self.logged_in_user, f"{day}-{month}-{year}", current_time, day, month, year))

        self.conn.commit()
        self.conn.close()

        self.manager.current = "attendance"


class AttendanceScreen(Screen):
    def on_pre_enter(self):
        # Fetch data from PostgreSQL and display
        self.conn = psycopg2.connect(
            host="localhost",  # Your system IP
            database="Attendance",  # Your PostgreSQL database name
            user="postgres",  # Your PostgreSQL username
            password="sai@123",  # Your PostgreSQL password
            port=5432
        )
        self.cursor = self.conn.cursor()

        self.cursor.execute("SELECT * FROM attendance ORDER BY id DESC LIMIT 1")
        result = self.cursor.fetchone()
        self.conn.close()

        if result:
            username, date, time, day, month, year = result[1:]
            self.ids.attendance_label.text = (
                f"User: {username}\nDate: {date}\nTime: {time}"
            )
        else:
            self.ids.attendance_label.text = "No attendance data found!"


class AttendanceApp(ScreenManager):
    pass


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(RegistrationScreen(name="register"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(AttendanceScreen(name="attendance"))
        return sm


if __name__ == "__main__":
    MyApp().run()

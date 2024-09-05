import flet as ft
import json
import os

class ContactsPage(ft.UserControl):
    def __init__(self, go_back):
        super().__init__()
        self.go_back = go_back
        self.contacts = [ft.TextField(label=f"Contact {i+1} Name") for i in range(5)]
        self.numbers = [ft.TextField(label=f"Contact {i+1} Number", input_filter=ft.NumbersOnlyInputFilter()) for i in range(5)]
        self.icons = [ft.IconButton(icon=ft.icons.PERSON, tooltip=f"Member {i+1}") for i in range(5)]
        self.contact_data = [{"name": "", "number": 0} for _ in range(5)]
        self.load_contacts()

    def build(self):
        contacts_title = ft.Text("Close Contacts", size=20, weight="bold")
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=self.go_back)
        save_button = ft.ElevatedButton(text="Save Contacts", on_click=self.save_contacts)
        contacts_portal = ft.Column([
            ft.Row([back_button, contacts_title], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            *[ft.Row([self.icons[i], self.contacts[i], self.numbers[i]]) for i in range(5)],
            save_button
        ])
        return contacts_portal

    def load_contacts(self):
        if os.path.exists("contacts.json"):
            with open("contacts.json", "r") as f:
                loaded_data = json.load(f)
                for i, contact in enumerate(loaded_data):
                    self.contacts[i].value = contact["name"]
                    self.numbers[i].value = str(contact["number"])
                self.contact_data = loaded_data

    def save_contacts(self, e):
        for i in range(5):
            self.contact_data[i]["name"] = self.contacts[i].value
            self.contact_data[i]["number"] = int(self.numbers[i].value or 0)
        with open("contacts.json", "w") as f:
            json.dump(self.contact_data, f)
        print("Contacts saved:", self.contact_data)
        self.update()

def go_back(e):
    print("Going back")

def main(page: ft.Page):
    page.add(ContactsPage(go_back))

ft.app(target=main)
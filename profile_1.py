import flet as ft
import json
import os

class ProfilePage(ft.UserControl):
    def __init__(self, go_back):
        super().__init__()
        self.go_back = go_back
        self.profile_name = ft.TextField(label="Name", width=500)
        self.profile_age = ft.TextField(label="Age", width=500)
        self.profile_number = ft.TextField(label="Number", width=500)
        self.profile_address = ft.TextField(label="Address", width=500)
        self.profile_data = {
            "name": "",
            "age": "",
            "number": "",
            "address": ""
        }
        self.load_profile()

    def build(self):
        profile_title = ft.Text("Profile", size=20, weight="bold")
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=self.go_back)
        save_button = ft.ElevatedButton("Save", on_click=self.save_profile)
        profile_portal = ft.Column([
            ft.Row([back_button, profile_title, save_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            self.profile_name,
            self.profile_age,
            self.profile_number,
            self.profile_address
        ])
        return profile_portal

    def save_profile(self, e):
        self.profile_data["name"] = self.profile_name.value
        self.profile_data["age"] = self.profile_age.value
        self.profile_data["number"] = self.profile_number.value
        self.profile_data["address"] = self.profile_address.value
        
        with open("profile_data.json", "w") as f:
            json.dump(self.profile_data, f)
        
        print("Profile saved:", self.profile_data)

    def load_profile(self):
        if os.path.exists("profile_data.json"):
            with open("profile_data.json", "r") as f:
                self.profile_data = json.load(f)
            
            self.profile_name.value = self.profile_data.get("name", "")
            self.profile_age.value = self.profile_data.get("age", "")
            self.profile_number.value = self.profile_data.get("number", "")
            self.profile_address.value = self.profile_data.get("address", "")

def go_back(e):
    print("Going back")

def main(page: ft.Page):
    page.add(ProfilePage(go_back))

ft.app(target=main)
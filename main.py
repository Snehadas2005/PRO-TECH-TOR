import flet as ft
from profile_1 import ProfilePage 
from contacts import ContactsPage
from data import DataPage

def main(page: ft.Page):
    def show_profile_page(e):
        page.controls.clear()
        page.add(ProfilePage(go_back=show_main_page))
        page.update()

    def show_contacts_page(e):
        page.controls.clear()
        page.add(ContactsPage(go_back=show_main_page))
        page.update()

    def show_data_page(e):
        page.controls.clear()
        page.add(DataPage(go_back=show_main_page))
        page.update()

    def show_main_page(e=None):
        page.controls.clear()
        page.add(ft.Column([
            title,
            ft.Row([profile_icon, contacts_icon, data_icon], alignment=ft.MainAxisAlignment.CENTER)
        ], alignment=ft.MainAxisAlignment.CENTER))
        page.update()

    page.title = "PRO-TECT-TOR"
    title = ft.Text("PRO-TECT-TOR", size=40, weight="bold")

    profile_icon = ft.Column([
        ft.IconButton(icon=ft.icons.PERSON, on_click=show_profile_page),
        ft.Text("John Doe", size=12)  # Add name under profile icon
    ], alignment=ft.MainAxisAlignment.CENTER)

    contacts_icon = ft.Column([
        ft.IconButton(icon=ft.icons.CONTACTS, on_click=show_contacts_page),
        ft.Text("John Doe's Contacts", size=12)  # Add name under contacts icon
    ], alignment=ft.MainAxisAlignment.CENTER)

    data_icon = ft.Column([
        ft.IconButton(icon=ft.icons.STORAGE, on_click=show_data_page),
        ft.Text("John Doe's Data Storage", size=12)  # Add name under data storage icon
    ], alignment=ft.MainAxisAlignment.CENTER)

    show_main_page()

if __name__ == "__main__":
    ft.app(target=main)
import flet as ft
from components.Interfaces import App

def main(page: ft.Page):
    page.title = "Turing"
    page.scroll = "auto"
    app = App()
    page.add(app)


ft.app(main)

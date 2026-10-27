import importlib
import os
import pkgutil

import flet as ft
import apps


def main(page: ft.Page):
    page.title = "AppLab IA ⚡"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO

    contenido = ft.Container(expand=True)

    def cargar_app(nombre_modulo):
        modulo = importlib.import_module(f"apps.{nombre_modulo}")
        modulo = importlib.reload(modulo)
        contenido.content = modulo.vista()
        page.update()

    botones = []
    for info_modulo in pkgutil.iter_modules(apps.__path__):
        modulo = importlib.import_module(f"apps.{info_modulo.name}")
        botones.append(
            ft.Button(
                text=info_modulo.name,
                on_click=lambda evento, nombre=info_modulo.name: cargar_app(nombre),
            )
        )

    page.add(ft.Column([ft.Row(botones, wrap=True), contenido], expand=True))


if __name__ == "__main__":
    ft.run(
        main,
        view=ft.AppView.WEB_BROWSER,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 7860)),
    )

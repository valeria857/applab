import asyncio

import flet as ft
from ia import ia


def vista():
    palabras = ft.TextField(
        label="Tres palabras clave",
        hint_text="Ejemplo: dragón, pupusa, wifi",
        prefix_icon=ft.Icons.AUTO_AWESOME,
        border_radius=12,
        focused_border_color=ft.Colors.PURPLE_400,
    )
    genero = ft.Dropdown(
        label="🎭 Género literario",
        value="Fantasía",
        border_radius=12,
        options=[
            ft.DropdownOption(key="Fantasía"),
            ft.DropdownOption(key="Terror"),
            ft.DropdownOption(key="Ciencia ficción"),
            ft.DropdownOption(key="Comedia"),
            ft.DropdownOption(key="Misterio"),
        ],
    )
    resultado = ft.Column(spacing=12)

    async def generar_cuento(evento):
        palabras_clave = (palabras.value or "").strip()
        if not palabras_clave:
            resultado.controls = [
                ft.Text(
                    "Escribe tus tres palabras clave para comenzar.",
                    color=ft.Colors.ERROR,
                )
            ]
            evento.page.update()
            return

        resultado.controls = [
            ft.Column(
                [
                    ft.ProgressRing(),
                    ft.Text("La IA está escribiendo tu cuento..."),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            )
        ]
        evento.page.update()

        try:
            cuento = await asyncio.to_thread(
                ia,
                "Escribe un cuento de exactamente 5 líneas que incorpore "
                "las tres palabras clave y respete el género indicado. "
                "Devuelve solo el cuento, una línea por oración.",
                f"Género: {genero.value}\nPalabras clave: {palabras_clave}",
            )
            resultado.controls = [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "📜 Tu Historia Generada",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.AMBER_300,
                            ),
                            ft.Text(
                                cuento,
                                size=16,
                                color=ft.Colors.WHITE,
                                text_align=ft.TextAlign.LEFT,
                                selectable=True,
                            ),
                        ],
                        spacing=16,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                    ),
                    padding=24,
                    border_radius=16,
                    border=ft.Border.all(1, ft.Colors.AMBER_400),
                    bgcolor=ft.Colors.GREY_900,
                )
            ]
        except Exception as error:
            resultado.controls = [
                ft.Text(
                    f"No se pudo generar el cuento: {error}",
                    color=ft.Colors.ERROR,
                )
            ]

        evento.page.update()

    boton = ft.FilledButton(
        content=ft.Text("Generar Cuento mágicamente", color=ft.Colors.WHITE),
        icon=ft.Icons.AUTO_FIX_HIGH,
        on_click=generar_cuento,
        height=50,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.PURPLE_600,
            color=ft.Colors.WHITE,
            padding=20,
        ),
    )

    tarjeta = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Text(
                        "✨  HISTORIAS HECHAS A TU MEDIDA",
                        size=11,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.PURPLE_200,
                    ),
                    padding=10,
                    border_radius=20,
                    bgcolor=ft.Colors.DEEP_PURPLE_900,
                ),
                ft.Text(
                    "✨ Cuentacuentos Mágico",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.AMBER_300,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Tres palabras, un género y una aventura que solo tú "
                    "podrías imaginar.",
                    size=15,
                    color=ft.Colors.PURPLE_100,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Column([palabras, genero], spacing=16),
                ft.Row([boton], alignment=ft.MainAxisAlignment.CENTER),
                resultado,
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        ),
        width=600,
        padding=28,
        border_radius=20,
        border=ft.Border.all(1, ft.Colors.DEEP_PURPLE_ACCENT),
        shadow=ft.BoxShadow(
            blur_radius=24,
            color=ft.Colors.DEEP_PURPLE_900,
            offset=ft.Offset(0, 8),
        ),
        bgcolor=ft.Colors.GREY_900,
    )

    return ft.Column(
        [ft.Container(content=tarjeta, alignment=ft.Alignment.CENTER)],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.START,
        expand=True,
    )

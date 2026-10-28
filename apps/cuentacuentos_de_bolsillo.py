import asyncio
import inspect
import threading

import flet as ft
import pyttsx3
from ia import ia


def vista():
    palabras = ft.TextField(
        label="Tres palabras clave",
        hint_text="Ejemplo: dragón, pupusa, wifi",
        prefix_icon=ft.Icons.AUTO_AWESOME,
        border_radius=12,
        focused_border_color=ft.Colors.PURPLE_400,
    )
    protagonista = ft.TextField(
        label="Protagonista / Escenario (opcional)",
        hint_text="Ejemplo: Un gato espacial en Marte",
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
    tono = ft.Dropdown(
        label="Tono o estilo",
        value="Épico",
        border_radius=12,
        options=[
            ft.DropdownOption(key="Educativo"),
            ft.DropdownOption(key="Misterioso"),
            ft.DropdownOption(key="Humorístico"),
            ft.DropdownOption(key="Épico"),
        ],
    )
    extensiones = {
        0: ("Corto", "aproximadamente 3 líneas"),
        1: ("Mediano", "aproximadamente 6 líneas"),
        2: ("Largo", "aproximadamente 10 líneas"),
    }
    longitud = ft.Text(
        "Extensión: Mediano (aproximadamente 6 líneas)",
        color=ft.Colors.PURPLE_100,
    )
    resultado = ft.Column(spacing=12)
    ilustracion = ft.Column(spacing=12)
    reproductor = ft.Column(spacing=8)
    feedback = ft.Text("", color=ft.Colors.PURPLE_200)
    lista_historial = ft.Column(spacing=6)
    historial = []
    historia_actual = ""
    historial_abierto = False

    def actualizar_longitud(evento):
        indice = int(float(evento.control.value))
        nombre, detalle = extensiones[indice]
        longitud.value = f"Extensión: {nombre} ({detalle})"
        evento.page.update()

    selector_longitud = ft.Slider(
        min=0,
        max=2,
        divisions=2,
        value=1,
        on_change=actualizar_longitud,
    )
    estado_cuento = ft.Text("Escribiendo la historia...")
    boton_generar = ft.FilledButton(
        content=ft.Text("Generar Cuento mágicamente", color=ft.Colors.WHITE),
        icon=ft.Icons.AUTO_FIX_HIGH,
        height=50,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.PURPLE_600,
            color=ft.Colors.WHITE,
            padding=20,
        ),
    )
    boton_ilustracion = ft.OutlinedButton(
        content=ft.Text("🎨 Generar idea de ilustración"),
        icon=ft.Icons.PALETTE,
        disabled=True,
    )
    boton_copiar = ft.OutlinedButton(
        content=ft.Text("📋 Copiar cuento"),
        icon=ft.Icons.COPY,
    )
    boton_limpiar = ft.TextButton(
        content=ft.Text("🗑️ Limpiar"),
    )
    boton_escuchar = ft.TextButton(
        content=ft.Text("🔊 Escuchar cuento"),
    )
    etiqueta_historial = ft.Text("📜 Historial reciente")
    boton_historial = ft.TextButton(content=etiqueta_historial)
    panel_historial = ft.Container(
        content=lista_historial,
        padding=12,
        border_radius=12,
        bgcolor=ft.Colors.DEEP_PURPLE_900,
        visible=False,
    )

    async def animar_estado(estado, mensajes):
        indice = 0
        while True:
            estado.value = mensajes[indice % len(mensajes)]
            estado.update()
            indice += 1
            await asyncio.sleep(1.2)

    def mostrar_cuento(cuento):
        nonlocal historia_actual

        historia_actual = cuento
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
                        ft.Markdown(value=cuento),
                        ft.Row(
                            [
                                boton_copiar,
                                boton_escuchar,
                                boton_limpiar,
                                boton_ilustracion,
                            ],
                            wrap=True,
                            alignment=ft.MainAxisAlignment.END,
                        ),
                        feedback,
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
        boton_ilustracion.disabled = False
        ilustracion.controls = []
        reproductor.controls = []

    def actualizar_historial():
        lista_historial.controls = [
            ft.TextButton(
                content=ft.Text(
                    f"{indice}. {cuento.splitlines()[0][:70]}",
                    color=ft.Colors.PURPLE_100,
                ),
                on_click=lambda evento, historia=cuento: cargar_cuento(
                    evento, historia
                ),
            )
            for indice, cuento in enumerate(historial, start=1)
        ]

    def cargar_cuento(evento, cuento):
        mostrar_cuento(cuento)
        feedback.value = "Cuento cargado desde el historial."
        evento.page.update()

    def alternar_historial(evento):
        nonlocal historial_abierto

        historial_abierto = not historial_abierto
        panel_historial.visible = historial_abierto
        etiqueta_historial.value = (
            "📜 Ocultar historial" if historial_abierto else "📜 Historial reciente"
        )
        evento.page.update()

    async def generar_cuento(evento):
        nonlocal historia_actual

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

        nombre_extension, detalle_extension = extensiones[
            int(float(selector_longitud.value))
        ]
        contexto = (protagonista.value or "").strip() or "Sin contexto adicional"
        historia_actual = ""
        boton_generar.disabled = True
        boton_ilustracion.disabled = True
        ilustracion.controls = []
        reproductor.controls = []
        estado_cuento.value = "Escribiendo la historia..."
        resultado.controls = [
            ft.Row(
                [ft.ProgressRing(), estado_cuento],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=14,
            )
        ]
        evento.page.update()
        tarea_estado = asyncio.create_task(
            animar_estado(
                estado_cuento,
                [
                    "Escribiendo la historia...",
                    "Dando vida a los personajes...",
                    "Preparando una aventura inolvidable...",
                ],
            )
        )

        try:
            cuento = await asyncio.to_thread(
                ia,
                "Escribe un cuento con formato Markdown. Su extensión debe "
                f"ser {detalle_extension}. Incorpora las tres palabras clave "
                "y respeta el género, tono, protagonista y escenario indicados.",
                f"Género: {genero.value}\n"
                f"Tono: {tono.value}\n"
                f"Extensión: {nombre_extension} ({detalle_extension})\n"
                f"Palabras clave: {palabras_clave}\n"
                f"Protagonista / escenario: {contexto}",
            )
            mostrar_cuento(cuento)
            historial.insert(0, cuento)
            del historial[3:]
            actualizar_historial()
        except Exception as error:
            historia_actual = ""
            resultado.controls = [
                ft.Text(
                    f"No se pudo generar el cuento: {error}",
                    color=ft.Colors.ERROR,
                )
            ]
        finally:
            tarea_estado.cancel()
            try:
                await tarea_estado
            except asyncio.CancelledError:
                pass
            boton_generar.disabled = False
            evento.page.update()

    async def generar_ilustracion(evento):
        if not historia_actual:
            return

        boton_ilustracion.disabled = True
        estado_ilustracion = ft.Text("Imaginando la escena...")
        ilustracion.controls = [
            ft.Row(
                [ft.ProgressRing(), estado_ilustracion],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=14,
            )
        ]
        evento.page.update()
        tarea_estado = asyncio.create_task(
            animar_estado(
                estado_ilustracion,
                [
                    "Imaginando la escena...",
                    "Eligiendo los detalles visuales...",
                    "Dando color a la aventura...",
                ],
            )
        )

        try:
            idea = await asyncio.to_thread(
                ia,
                "Describe brevemente una ilustración de la escena principal "
                "del cuento, incluyendo ambiente, personajes y estilo visual. "
                "Devuelve solo la descripción.",
                historia_actual,
            )
            ilustracion.controls = [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "🎨 Idea de ilustración",
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.PURPLE_200,
                            ),
                            ft.Markdown(value=idea),
                        ],
                        spacing=8,
                    ),
                    padding=18,
                    border_radius=14,
                    bgcolor=ft.Colors.DEEP_PURPLE_900,
                )
            ]
        except Exception as error:
            ilustracion.controls = [
                ft.Text(
                    f"No se pudo generar la idea de ilustración: {error}",
                    color=ft.Colors.ERROR,
                )
            ]
        finally:
            tarea_estado.cancel()
            try:
                await tarea_estado
            except asyncio.CancelledError:
                pass
            boton_ilustracion.disabled = False
            evento.page.update()

    async def copiar_cuento(evento):
        if not historia_actual:
            return

        try:
            resultado_portapapeles = evento.page.set_clipboard(historia_actual)
            if inspect.isawaitable(resultado_portapapeles):
                await resultado_portapapeles
            feedback.value = "Cuento copiado al portapapeles."
            feedback.color = ft.Colors.GREEN_300
        except Exception as error:
            feedback.value = f"No se pudo copiar el cuento: {error}"
            feedback.color = ft.Colors.ERROR
        evento.page.update()

    def limpiar_cuento(evento):
        nonlocal historia_actual

        historia_actual = ""
        resultado.controls = []
        ilustracion.controls = []
        reproductor.controls = []
        feedback.value = ""
        boton_ilustracion.disabled = True
        evento.page.update()

    def cerrar_reproductor(evento):
        reproductor.controls = []
        evento.page.update()

    def escuchar_cuento(evento):
        if not historia_actual or boton_escuchar.disabled:
            return

        texto_del_cuento = historia_actual
        boton_escuchar.disabled = True
        estado_audio = ft.Text(
            "🔊 Reproduciendo audio localmente...",
            color=ft.Colors.PURPLE_100,
        )
        reproductor.controls = [
            ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.VOLUME_UP, color=ft.Colors.AMBER_300),
                        estado_audio,
                        ft.TextButton(
                            content=ft.Text("Cerrar reproductor"),
                            on_click=cerrar_reproductor,
                        ),
                    ],
                    spacing=10,
                    wrap=True,
                ),
                padding=14,
                border_radius=12,
                bgcolor=ft.Colors.DEEP_PURPLE_900,
            )
        ]
        evento.page.update()

        async def informar_finalizacion(error):
            boton_escuchar.disabled = False
            if reproductor.controls:
                estado_audio.value = (
                    f"No se pudo reproducir el cuento: {error}"
                    if error
                    else "Lectura finalizada."
                )
                if error:
                    estado_audio.color = ft.Colors.ERROR
            evento.page.update()

        def leer_cuento():
            error = None
            try:
                engine = pyttsx3.init()
                engine.setProperty("rate", 160)
                engine.say(texto_del_cuento)
                engine.runAndWait()
            except Exception as excepcion:
                error = str(excepcion)
            finally:
                evento.page.run_task(informar_finalizacion, error)

        threading.Thread(
            target=leer_cuento,
            name="lectura-cuento",
            daemon=True,
        ).start()

    boton_generar.on_click = generar_cuento
    boton_ilustracion.on_click = generar_ilustracion
    boton_copiar.on_click = copiar_cuento
    boton_limpiar.on_click = limpiar_cuento
    boton_escuchar.on_click = escuchar_cuento
    boton_historial.on_click = alternar_historial

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
                ft.Column(
                    [palabras, protagonista, genero, tono],
                    spacing=16,
                ),
                ft.Text(
                    "¿Qué tan larga será tu aventura?",
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                selector_longitud,
                ft.Row(
                    [
                        ft.Text("Corto", color=ft.Colors.PURPLE_200),
                        ft.Text("Mediano", color=ft.Colors.PURPLE_200),
                        ft.Text("Largo", color=ft.Colors.PURPLE_200),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                longitud,
                ft.Row(
                    [boton_generar],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                boton_historial,
                panel_historial,
                resultado,
                ilustracion,
                reproductor,
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

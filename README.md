# 📚 Cuentacuentos de Bolsillo - AppLab

Genera cuentos infantiles e historias personalizadas con inteligencia
artificial. La aplicación está construida con **Flet** y utiliza **Google
Gemini** para crear historias según las preferencias y las ideas del usuario.

## ✨ Funcionalidades

- Selección del género literario y el tono de la historia.
- Ajuste de la extensión: corta, mediana o larga.
- Personalización con palabras clave y protagonista o escenario.
- Tarjetas interactivas para leer, copiar y escuchar los cuentos.
- Historial de los tres cuentos más recientes durante la sesión.
- Generación de descripciones para ilustrar la escena principal.

## 🚀 Ejecución local

1. Instala Python 3.10 o posterior.
2. Crea y activa un entorno virtual (opcional, pero recomendado):

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Instala las dependencias:

   ```powershell
   pip install -r requirements.txt
   ```

4. Configura tu clave de Google Gemini como variable de entorno:

   ```powershell
   $env:GEMINI_API_KEY = "tu-clave-de-gemini"
   ```

5. Inicia la aplicación:

   ```powershell
   python main.py
   ```

La aplicación se abrirá localmente en `http://localhost:7860`.

# Notas importantes

Sistema simple para guardar recordatorios y notas importantes en tu día a día. Incluye una interfaz web ligera construida con Vue 3 (CDN) y almacenamiento local.

## Requisitos

- Navegador moderno para la interfaz web.
- (Opcional) Python 3.9+ si deseas usar la interfaz CLI previa.

## Interfaz web

Puedes abrir `docs/index.html` localmente o desplegar la carpeta `docs/` en cualquier hosting estático como **GitHub Pages**.

### Despliegue en GitHub Pages

1. Empuja este repositorio a GitHub.
2. Ve a **Settings → Pages**.
3. En **Build and deployment**, selecciona **Deploy from a branch**.
4. Elige la rama principal (por ejemplo `main` o `master`) y la carpeta `/docs` como fuente.
5. Guarda y espera a que GitHub genere la URL pública.

La app usa rutas relativas (`app.js` y `styles.css`) por lo que funciona correctamente en GitHub Pages.

### Ejecutar en local

```bash
cd docs
python3 -m http.server 8000
```

Luego visita `http://localhost:8000`.

### Funcionalidades

- Crear notas con título, detalle, etiquetas y fecha límite.
- Buscar por texto y filtrar por etiqueta.
- Archivar notas y verlas en una sección separada.
- Persistencia en `localStorage` del navegador.

## Uso CLI (opcional)

```bash
python3 main.py add "Pagar alquiler" "Programar transferencia antes del lunes" --tags finanzas,casa --due 2024-10-01
python3 main.py list
python3 main.py list --tag finanzas
python3 main.py list --search transferencia
python3 main.py archive 1
```

## Datos

- Interfaz web: datos en `localStorage` del navegador.
- CLI: notas en `data/notes.json` dentro del repositorio.

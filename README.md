# CI AI Analyzer 🤖

Pipeline que detecta fallos en GitHub Actions y los analiza automáticamente con inteligencia artificial, devolviendo la causa del error y posibles soluciones en segundos.

## ¿Qué problema resuelve?

Cuando un pipeline falla, el equipo pierde tiempo revisando logs largos para encontrar la causa raíz. Este proyecto automatiza ese proceso: en cuanto falla un step, una IA analiza el error y entrega un diagnóstico claro directamente en el pipeline.

## ¿Cómo funciona?

```
Push a master
    → Pipeline corre normalmente
    → Si un step falla → se activa el step de análisis
    → El script llama a OpenAI con el contexto del error
    → La IA devuelve causa y solución en español
    → El resultado aparece en los logs del pipeline
    → El pipeline se marca como fallido (comportamiento correcto)
```

## Stack

- **GitHub Actions** — orquestación del pipeline
- **Python** — script de análisis
- **OpenAI API (gpt-4o-mini)** — modelo de lenguaje para el análisis

## Setup

### 1. Clonar el repo

```bash
git clone https://github.com/havellaneda-ar/ci-ai-analyzer.git
```

### 2. Configurar secrets en GitHub

Ir a **Settings → Secrets and variables → Actions** y agregar:

| Secret | Descripción |
|--------|-------------|
| `OPENAI_API_KEY` | API key de OpenAI (platform.openai.com) |

El `GITHUB_TOKEN` es generado automáticamente por GitHub en cada run, no requiere configuración.

### 3. Hacer push a master

El workflow se activa automáticamente con cada push a `master`.

## Estructura del proyecto

```
ci-ai-analyzer/
├── .github/
│   └── workflows/
│       └── test.yml       # Definición del pipeline
├── ci-analyzer.py         # Script principal de análisis
└── README.md
```

## Ejemplo de output

Cuando un step falla, el análisis de AI aparece en los logs del step **AI Failure Analysis**:

```
📥 Bajando logs...
🤖 Analizando con AI...

--- AI Analysis ---
El error que estás viendo es un "exit code 1", lo que indica que el proceso
terminó con un error. Las causas más comunes son:

1. **Error en el script**: El comando ejecutado retornó un código de error.
2. **Permisos insuficientes**: El runner no tiene permisos para ejecutar el comando.

Soluciones:
1. Revisá el comando que falla y asegurate que retorne exit code 0 en caso de éxito.
2. Verificá los permisos del runner en Settings → Actions → General.
```

---

## Roadmap

### ✅ v1 — MVP (actual)
- Detecta fallos en el pipeline
- Analiza el error con OpenAI
- Devuelve causa y solución en los logs
- Pipeline se marca correctamente como fallido

### 🔜 v2 — Comentario automático en PR
- El análisis se postea como comentario directamente en el Pull Request
- El desarrollador ve el diagnóstico sin tener que entrar a la pestaña de Actions

### 🔜 v3 — Logs reales
- En lugar de un mensaje genérico, se descargan los logs reales del step fallido via GitHub API
- El análisis es más preciso y contextual

### 🔜 v4 — Categorización de errores
- La IA clasifica el tipo de fallo: dependency error, flaky test, config error, etc.
- Respuestas más específicas según la categoría

### 🔜 v5 — Auto PR con el fix
- Para errores simples y conocidos (versión de dependencia desactualizada, typo en config), la IA genera un PR automático con el fix propuesto

---

## Contribuciones

Este proyecto está en desarrollo activo. Si tenés ideas o encontrás bugs, abrí un issue.

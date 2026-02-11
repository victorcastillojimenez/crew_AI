# 🚀 Agencia de Colocación Inteligente

Sistema multi-agente construido con [CrewAI](https://www.crewai.com/) que analiza CVs, busca ofertas de empleo reales, investiga empresas y redacta mensajes de postulación personalizados.

## Arquitectura

El sistema usa **4 agentes especializados** en un flujo **jerárquico** supervisado por un Manager LLM:

```
career_profiler → job_market_scout → corporate_culture_researcher → application_strategist
```

| Agente | Rol | Herramientas |
|--------|-----|-------------|
| `career_profiler` | Analiza CV y sugiere roles | FileReadTool |
| `job_market_scout` | Busca ofertas reales online | SerperDevTool |
| `corporate_culture_researcher` | Investiga cultura empresarial | SerperDevTool |
| `application_strategist` | Redacta postulaciones | — |

## Requisitos

- Python 3.11+
- API Key de [Groq](https://console.groq.com/)
- API Key de [Serper](https://serper.dev/) (para búsquedas web)

## Instalación

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd crew_AI

# 2. Crear y activar entorno virtual
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus API keys
```

## Configuración

Crear un archivo `.env` en la raíz del proyecto:

```env
GROQ_API_KEY=tu_clave_groq_aqui
SERPER_API_KEY=tu_clave_serper_aqui
```

## Uso

```bash
python main.py
```

El sistema generará un archivo `reporte_postulacion.md` con los mensajes de postulación personalizados.

## Estructura del proyecto

```
crew_AI/
├── config/
│   ├── agents.yaml      # Configuración de agentes (roles, backstories)
│   └── tasks.yaml       # Definición de tareas (descripciones, outputs)
├── agencia_crew.py      # Clase principal de la crew
├── exceptions.py        # Excepciones personalizadas
├── main.py              # Punto de entrada
├── requirements.txt     # Dependencias con versiones fijadas
├── tests/               # Tests unitarios
│   └── test_agencia.py
└── .env                 # Variables de entorno (NO compartir)
```

## Tests

```bash
python -m pytest tests/ -v
```

## Licencia

Proyecto académico — uso educativo.

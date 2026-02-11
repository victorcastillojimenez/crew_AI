"""
Punto de entrada de la Agencia de Colocación Inteligente.

Carga la configuración, valida los inputs y ejecuta el flujo
completo de la crew de agentes.
"""

import logging
import os
import sys

from dotenv import load_dotenv

from agencia_crew import AgenciaColocacion
from exceptions import (
    AgencyBaseError,
    AgencyConfigError,
    CrewExecutionError,
    InputValidationError,
)

# Configuración del logger a nivel de módulo
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger: logging.Logger = logging.getLogger(__name__)

# Longitud mínima (en caracteres) para considerar válido un CV
MIN_CV_LENGTH: int = 50


def validate_inputs(inputs: dict[str, str]) -> None:
    """Valida que los datos de entrada contengan los campos requeridos.

    Args:
        inputs: Diccionario con los datos del estudiante.
            Debe contener 'nombre_estudiante' y 'cv_text'.

    Raises:
        InputValidationError: Si falta algún campo o el CV está vacío/corto.
    """
    nombre: str | None = inputs.get("nombre_estudiante")
    cv_text: str | None = inputs.get("cv_text")

    if not nombre or not nombre.strip():
        raise InputValidationError(
            "El campo 'nombre_estudiante' es obligatorio."
        )

    if not cv_text or len(cv_text.strip()) < MIN_CV_LENGTH:
        raise InputValidationError(
            f"El campo 'cv_text' debe tener al menos {MIN_CV_LENGTH} "
            f"caracteres. Se recibieron {len(cv_text.strip()) if cv_text else 0}."
        )


def run_agencia() -> None:
    """Ejecuta el flujo completo de la Agencia de Colocación.

    Carga las variables de entorno, valida los inputs de prueba
    y lanza la crew de agentes en modo jerárquico.

    Raises:
        SystemExit: Si ocurre un error irrecuperable.
    """
    load_dotenv()

    if not os.getenv("GROQ_API_KEY"):
        logger.error("No se encontró GROQ_API_KEY en el archivo .env")
        sys.exit(1)

    if not os.getenv("SERPER_API_KEY"):
        logger.warning(
            "No se encontró SERPER_API_KEY. Las búsquedas web fallarán."
        )

    logger.info("=" * 50)
    logger.info("🚀 INICIANDO AGENCIA DE COLOCACIÓN INTELIGENTE")
    logger.info("=" * 50)

    # En un entorno real, 'cv_text' vendría del lector de PDF de Streamlit
    datos_prueba: dict[str, str] = {
        "nombre_estudiante": "Usuario de Prueba",
        "cv_text": (
            "Estudiante de Ingeniería Informática apasionado por la "
            "Inteligencia Artificial. "
            "Habilidades: Python, SQL, conocimientos básicos de Machine "
            "Learning y CrewAI. "
            "Proyectos: Desarrollo de un bot de análisis de sentimientos "
            "y una web de portafolio. "
            "Idiomas: Español (Nativo), Inglés (B2)."
        ),
    }

    try:
        validate_inputs(datos_prueba)
        agencia = AgenciaColocacion()

        logger.info(
            "⏳ Los agentes están trabajando (esto puede tardar unos minutos)..."
        )
        resultado = agencia.crew().kickoff(inputs=datos_prueba)

        logger.info("=" * 50)
        logger.info("✅ PROCESO COMPLETADO CON ÉXITO")
        logger.info("=" * 50)
        logger.info("📝 REPORTE GENERADO:\n%s", resultado)
        logger.info(
            "📂 El archivo 'reporte_postulacion.md' ha sido generado."
        )

    except InputValidationError as exc:
        logger.error("Error de validación: %s", exc)
        sys.exit(1)

    except AgencyConfigError as exc:
        logger.error("Error de configuración: %s", exc)
        sys.exit(1)

    except (ConnectionError, TimeoutError) as exc:
        logger.error("Error de conexión con el servicio LLM: %s", exc)
        sys.exit(1)

    except AgencyBaseError as exc:
        logger.error("Error de la agencia: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    run_agencia()
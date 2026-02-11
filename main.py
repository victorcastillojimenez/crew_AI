import os
import sys
from dotenv import load_dotenv
from agencia_crew import AgenciaColocacion

def run_agencia():
    """
    Punto de entrada principal para ejecutar la Agencia de Colocación.
    """

    load_dotenv()
    
    if not os.getenv("GROQ_API_KEY"):
        print("❌ Error: No se encontró GROQ_API_KEY en el archivo .env")
        return
    if not os.getenv("SERPER_API_KEY"):
        print("⚠️ Advertencia: No se encontró SERPER_API_KEY. Las búsquedas fallarán.")

    print("\n" + "="*50)
    print("🚀 INICIANDO AGENCIA DE COLOCACIÓN INTELIGENTE")
    print("="*50 + "\n")

    # En un entorno real, 'cv_text' vendría del lector de PDF de tu Streamlit
    datos_prueba = {
        "nombre_estudiante": "Usuario de Prueba",
        "cv_text": """
            Estudiante de Ingeniería Informática apasionado por la Inteligencia Artificial.
            Habilidades: Python, SQL, conocimientos básicos de Machine Learning y CrewAI.
            Proyectos: Desarrollo de un bot de análisis de sentimientos y una web de portafolio.
            Idiomas: Español (Nativo), Inglés (B2).
        """
    }

    try:
        agencia = AgenciaColocacion()
        
        # 4. Ejecutar el proceso (kickoff)
        print("⏳ Los agentes están trabajando (esto puede tardar unos minutos)...")
        resultado = agencia.crew().kickoff(inputs=datos_prueba)

        # 5. Mostrar resultado final
        print("\n" + "="*50)
        print("✅ PROCESO COMPLETADO CON ÉXITO")
        print("="*50 + "\n")
        
        print("📝 REPORTE GENERADO:\n")
        print(resultado)
        
        print(f"\n📂 El archivo 'reporte_postulacion.md' ha sido generado en tu carpeta.")

    except Exception as e:
        print(f"\n❌ Se produjo un error durante la ejecución: {e}")

if __name__ == "__main__":
    # Aseguramos que el entorno virtual esté bien configurado antes de lanzar
    run_agencia()
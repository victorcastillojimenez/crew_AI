"""
Módulo principal de la Agencia de Colocación Inteligente.

Define la clase `AgenciaColocacion` que orquesta 4 agentes especializados
en un flujo jerárquico para analizar CVs, buscar empleos, investigar
empresas y redactar postulaciones personalizadas.
"""

import os
from pathlib import Path

from crewai import Agent, Crew, LLM, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool, SerperDevTool

from exceptions import AgencyConfigError

# Directorio base del proyecto (para resolver rutas relativas de forma robusta)
BASE_DIR: Path = Path(__file__).resolve().parent


@CrewBase
class AgenciaColocacion:
    """Agencia de Colocación Inteligente basada en CrewAI.

    Orquesta un flujo jerárquico de 4 agentes especializados:
        - career_profiler: Analiza el CV y propone roles.
        - job_market_scout: Busca ofertas reales en internet.
        - corporate_culture_researcher: Investiga las empresas.
        - application_strategist: Redacta mensajes de postulación.

    Args:
        No recibe argumentos; las credenciales se leen de variables de entorno.

    Raises:
        AgencyConfigError: Si falta la GROQ_API_KEY en el entorno.
    """

    agents_config: str = str(BASE_DIR / "config" / "agents.yaml")
    tasks_config: str = str(BASE_DIR / "config" / "tasks.yaml")

    def __init__(self) -> None:
        """Inicializa el LLM y las herramientas compartidas.

        Raises:
            AgencyConfigError: Si GROQ_API_KEY no está definida.
        """
        groq_api_key: str | None = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise AgencyConfigError(
                "No se encontró GROQ_API_KEY en las variables de entorno."
            )

        self.llm: LLM = LLM(
            model="llama-3.3-70b-versatile",
            temperature=0.4,
            base_url="https://api.groq.com/openai/v1",
            api_key=groq_api_key,
        )

        # SerperDevTool: búsqueda de ofertas y cultura empresarial en vivo
        self.search_tool: SerperDevTool = SerperDevTool()
        # FileReadTool: lectura de archivos locales (CVs en texto plano)
        self.file_tool: FileReadTool = FileReadTool()

    # ==========================================
    # DEFINICIÓN DE AGENTES (Decoradores @agent)
    # ==========================================

    @agent
    def career_profiler(self) -> Agent:
        """Agente estratega de carrera: analiza el CV e identifica roles potenciales."""
        return Agent(
            config=self.agents_config["career_profiler"],
            tools=[self.file_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=True,
            max_rpm=2,
            max_iter=10,
        )

    @agent
    def job_market_scout(self) -> Agent:
        """Agente cazador de empleos: busca ofertas reales con herramientas de búsqueda."""
        return Agent(
            config=self.agents_config["job_market_scout"],
            tools=[self.search_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_rpm=2,
            max_iter=10,
        )

    @agent
    def corporate_culture_researcher(self) -> Agent:
        """Agente investigador corporativo: estudia la cultura y valores de las empresas."""
        return Agent(
            config=self.agents_config["corporate_culture_researcher"],
            tools=[self.search_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_rpm=2,
            max_iter=10,
        )

    @agent
    def application_strategist(self) -> Agent:
        """Agente redactor: crea mensajes de postulación personalizados."""
        return Agent(
            config=self.agents_config["application_strategist"],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_rpm=2,
            max_iter=10,
        )

    # ==========================================
    # DEFINICIÓN DE TAREAS (Decoradores @task)
    # ==========================================

    @task
    def profile_assessment_task(self) -> Task:
        """Tarea de análisis de perfil: extrae habilidades y sugiere roles."""
        return Task(
            config=self.tasks_config["profile_assessment_task"],
            agent=self.career_profiler(),
        )

    @task
    def job_scouting_task(self) -> Task:
        """Tarea de búsqueda: localiza ofertas reales que encajen con el perfil."""
        return Task(
            config=self.tasks_config["job_scouting_task"],
            agent=self.job_market_scout(),
        )

    @task
    def company_intelligence_task(self) -> Task:
        """Tarea de inteligencia empresarial: investiga las empresas candidatas."""
        return Task(
            config=self.tasks_config["company_intelligence_task"],
            agent=self.corporate_culture_researcher(),
        )

    @task
    def custom_outreach_drafting_task(self) -> Task:
        """Tarea de redacción: genera mensajes de postulación personalizados."""
        return Task(
            config=self.tasks_config["custom_outreach_drafting_task"],
            agent=self.application_strategist(),
            output_file="reporte_postulacion.md",
        )

    # ==========================================
    # ENSAMBLAJE DE LA CREW
    # ==========================================

    @crew
    def crew(self) -> Crew:
        """Crea la Agencia con un flujo de trabajo JERÁRQUICO.

        El manager_llm actúa como director, supervisando la calidad
        de cada fase y coordinando la comunicación entre agentes.

        Returns:
            Crew: Instancia configurada y lista para ejecutarse.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_llm=self.llm,
            # Deshabilitado para evitar el error 401 de embeddings
            memory=False,
            verbose=True,
        )
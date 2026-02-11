import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, FileReadTool

@CrewBase
class AgenciaColocacion():
    """
    Agencia de Colocación Inteligente: 
    Analiza CVs, busca empleos reales, investiga empresas y redacta postulaciones.
    """
    
    # Rutas a los archivos (YAML)
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self) -> None:

        #LLM 
        self.llm = LLM(
            model="llama-3.3-70b-versatile",
            temperature=0.4,
            base_url="https://api.groq.com/openai/v1",
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        # SerperDevTool: Para búsqueda de ofertas y cultura empresarial en vivo
        self.search_tool = SerperDevTool()
        # FileReadTool: Para leer el contenido del CV localmente
        self.file_tool = FileReadTool()

    # ==========================================
    # DEFINICIÓN DE AGENTES (Decoradores @agent)
    # ==========================================

    @agent
    def career_profiler(self) -> Agent:
        return Agent(
            config=self.agents_config['career_profiler'],
            llm=self.llm,
            verbose=True,
            allow_delegation=True, # Permitimos delegar para mejor calidad
            max_rpm=2,            # Lento pero sin errores 429
            max_iter=10,
        )

    @agent
    def job_market_scout(self) -> Agent:
        return Agent(
            config=self.agents_config['job_market_scout'],
            tools=[self.search_tool], # SerperDevTool 
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_rpm=2,
            max_iter=10,
        )

    @agent
    def corporate_culture_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['corporate_culture_researcher'],
            tools=[self.search_tool], # SerperDevTool
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_rpm=2,
            max_iter=10
        )

    @agent
    def application_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['application_strategist'],
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
        return Task(
            config=self.tasks_config['profile_assessment_task'],
            agent=self.career_profiler(),
        )

    @task
    def job_scouting_task(self) -> Task:
        return Task(
            config=self.tasks_config['job_scouting_task'],
            agent=self.job_market_scout(),
        )

    @task
    def company_intelligence_task(self) -> Task:
        return Task(
            config=self.tasks_config['company_intelligence_task'],
            agent=self.corporate_culture_researcher(),
        )

    @task
    def custom_outreach_drafting_task(self) -> Task:
        return Task(
            config=self.tasks_config['custom_outreach_drafting_task'],
            agent=self.application_strategist(),
            output_file='reporte_postulacion.md', # Genera el entregable final automáticamente
        )

    # ==========================================
    # ENSAMBLAJE DE LA CREW (Punto extra: Jerarquía)
    # ==========================================

    @crew
    def crew(self) -> Crew:
        """
        Crea la Agencia con un flujo de trabajo JERÁRQUICO.
        Esto añade un 'Manager LLM' que supervisa la calidad de cada fase.
        """
        return Crew(
            agents=self.agents,  # Recogidos automáticamente por los decoradores
            tasks=self.tasks,    # Recogidos automáticamente por los decoradores
            process=Process.hierarchical, # REQUISITO PARA EL PUNTO EXTRA (+1) [cite: 17, 18]
            manager_llm=self.llm,         # El LLM que actuará como director
            memory=False,  # <--- FALSE PARA EVITAR EL ERROR 401 DE EMBEDDINGS
            verbose=True,
            step_callback=None,
        )
import flet as ft
from startup_equipes_agentesIA_pv import Agent, Task, Crew
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CrewAIView(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.agents = []
        self.tasks = []
        self.setup_view()
        
    def setup_view(self):
        # Campos para Agente
        self.agent_role = ft.TextField(label="Role do Agente", width=300)
        self.agent_goal = ft.TextField(label="Objetivo do Agente", width=300)
        self.agent_backstory = ft.TextField(
            label="História do Agente",
            width=300,
            multiline=True,
            min_lines=3
        )
        
        # Campos para Tarefa
        self.task_description = ft.TextField(
            label="Descrição da Tarefa",
            width=300,
            multiline=True,
            min_lines=2
        )
        self.task_expected = ft.TextField(
            label="Saída Esperada",
            width=300,
            multiline=True,
            min_lines=2
        )
        self.task_attempts = ft.TextField(
            label="Número de Tentativas",
            width=300,
            value="2"
        )
        
        # Campo para o tema
        self.theme_field = ft.TextField(
            label="Tema para Pesquisa",
            width=300,
            multiline=True,
            min_lines=2
        )
        
        # Dropdown para selecionar agente para tarefa
        self.agent_dropdown = ft.Dropdown(
            label="Selecione o Agente",
            width=300,
            options=[]
        )
        
        # Listas de Agentes e Tarefas
        self.agents_list = ft.ListView(
            expand=1,
            spacing=10,
            padding=20,
            height=200
        )
        
        self.tasks_list = ft.ListView(
            expand=1,
            spacing=10,
            padding=20,
            height=200
        )
        
        # Botões de ação
        self.add_agent_btn = ft.ElevatedButton(
            "Adicionar Agente",
            icon=ft.icons.PERSON_ADD,
            on_click=self.add_agent
        )
        
        self.add_task_btn = ft.ElevatedButton(
            "Adicionar Tarefa",
            icon=ft.icons.ADD_TASK,
            on_click=self.add_task
        )
        
        self.execute_btn = ft.ElevatedButton(
            "Executar Tarefas",
            icon=ft.icons.PLAY_ARROW,
            on_click=self.execute_tasks
        )
        
        # Container para o resultado
        self.result_text = ft.Text()
        
    def build(self):
        return ft.Container(
            content=ft.Column([
                ft.Text("Gerenciador de Agentes IA", size=30, weight=ft.FontWeight.BOLD),
                
                ft.Text("Adicionar Agente", size=20, weight=ft.FontWeight.W_500),
                self.agent_role,
                self.agent_goal,
                self.agent_backstory,
                self.add_agent_btn,
                
                ft.Divider(),
                ft.Text("Agentes Criados:", size=16),
                self.agents_list,
                
                ft.Text("Adicionar Tarefa", size=20, weight=ft.FontWeight.W_500),
                self.task_description,
                self.task_expected,
                self.task_attempts,
                self.agent_dropdown,
                self.add_task_btn,
                
                ft.Divider(),
                ft.Text("Tarefas Criadas:", size=16),
                self.tasks_list,
                
                ft.Text("Tema da Pesquisa", size=20, weight=ft.FontWeight.W_500),
                self.theme_field,
                
                self.execute_btn,
                
                ft.Divider(),
                self.result_text
            ], 
            scroll=ft.ScrollMode.AUTO),
            padding=40
        )
    
    def add_agent(self, e):
        try:
            agent = Agent(
                role=self.agent_role.value,
                goal=self.agent_goal.value,
                backstory=self.agent_backstory.value
            )
            
            self.agents.append(agent)
            self.agents_list.controls.append(
                ft.Text(f"Agente: {agent.role} - {agent.goal}")
            )
            
            # Atualiza dropdown
            self.agent_dropdown.options.append(
                ft.dropdown.Option(
                    text=agent.role,
                    key=len(self.agents) - 1
                )
            )
            
            # Limpa campos
            self.agent_role.value = ""
            self.agent_goal.value = ""
            self.agent_backstory.value = ""
            
            self.update()
            self.page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Agente adicionado com sucesso!"))
            )
            
        except Exception as ex:
            self.page.show_snack_bar(
                ft.SnackBar(content=ft.Text(f"Erro ao adicionar agente: {str(ex)}"))
            )
    
    def add_task(self, e):
        try:
            if not self.agent_dropdown.value:
                raise ValueError("Selecione um agente para a tarefa")
                
            agent_idx = int(self.agent_dropdown.value)
            agent = self.agents[agent_idx]
            
            task = Task(
                description=self.task_description.value,
                agent=agent,
                expected_output=self.task_expected.value,
                attempts=int(self.task_attempts.value)
            )
            
            self.tasks.append(task)
            self.tasks_list.controls.append(
                ft.Text(f"Tarefa para {agent.role}: {task.description[:50]}...")
            )
            
            # Limpa campos
            self.task_description.value = ""
            self.task_expected.value = ""
            self.task_attempts.value = "2"
            self.agent_dropdown.value = None
            
            self.update()
            self.page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Tarefa adicionada com sucesso!"))
            )
            
        except Exception as ex:
            self.page.show_snack_bar(
                ft.SnackBar(content=ft.Text(f"Erro ao adicionar tarefa: {str(ex)}"))
            )
    
    def execute_tasks(self, e):
        try:
            if not self.agents or not self.tasks:
                raise ValueError("Adicione pelo menos um agente e uma tarefa")
                
            if not self.theme_field.value:
                raise ValueError("Digite um tema para a pesquisa")
            
            # Cria a equipe
            crew = Crew(
                agents=self.agents,
                tasks=self.tasks
            )
            
            # Define entradas
            inputs = {"tema": self.theme_field.value}
            
            # Executa tarefas
            self.result_text.value = "Executando tarefas..."
            self.update()
            
            results = crew.kickoff(inputs=inputs)
            
            # Gera markdown
            if len(results) > 1:
                self.result_text.value = "Gerando arquivo markdown..."
                self.update()
                
                # Gera o arquivo
                markdown_content = results[1]  # Pega o resultado da segunda tarefa
                filename = "resultado.md"
                
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(markdown_content)
                
                # Prepara download
                self.page.show_snack_bar(
                    ft.SnackBar(
                        content=ft.Text("Arquivo markdown gerado com sucesso!")
                    )
                )
                
                # Cria botão de download
                download_btn = ft.ElevatedButton(
                    "Baixar Arquivo Markdown",
                    icon=ft.icons.DOWNLOAD,
                    on_click=lambda _: self.download_file(filename)
                )
                
                self.result_text.value = "Tarefas concluídas com sucesso!"
                self.page.add(download_btn)
                
            self.update()
            
        except Exception as ex:
            self.page.show_snack_bar(
                ft.SnackBar(content=ft.Text(f"Erro ao executar tarefas: {str(ex)}"))
            )
    
    def download_file(self, filename):
        try:
            # Lê o conteúdo do arquivo
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Cria um arquivo temporário para download
            self.page.client_storage.set("markdown_content", content)
            self.page.launch_url(f"/download/{filename}")
            
        except Exception as ex:
            self.page.show_snack_bar(
                ft.SnackBar(content=ft.Text(f"Erro ao baixar arquivo: {str(ex)}"))
            )

def main(page: ft.Page):
    # Configurações da página
    page.title = "CrewAI Manager"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 800
    page.window.height = 1000
    
    # Adiciona a view
    crew_view = CrewAIView(page)
    page.add(crew_view)

if __name__ == "__main__":
    ft.app(target=main)

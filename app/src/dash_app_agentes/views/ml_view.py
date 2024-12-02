import flet as ft
from agents.ml_agents import KNNAgent, DecisionTreeAgent
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class MLView(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.knn_agent = KNNAgent()
        self.dt_agent = DecisionTreeAgent()
        self.current_agent = self.knn_agent
        self.setup_view()

    def setup_view(self):
        # Componentes da UI
        self.file_picker = ft.FilePicker(
            on_result=self.handle_file_picked
        )
        self.page.overlay.append(self.file_picker)
        
        self.upload_button = ft.ElevatedButton(
            "Carregar arquivo Excel",
            icon=ft.icons.UPLOAD_FILE,
            on_click=lambda _: self.file_picker.pick_files(
                allowed_extensions=["xlsx", "xls"]
            )
        )
        
        self.data_table = ft.DataTable(
            columns=[],
            rows=[],
            border=ft.border.all(2, "grey"),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(3, "grey"),
            horizontal_lines=ft.border.BorderSide(1, "grey"),
        )
        
        self.x_dropdown = ft.Dropdown(
            label="Variável X",
            width=200,
            on_change=self.handle_variable_change
        )
        
        self.y_dropdown = ft.Dropdown(
            label="Variável Y",
            width=200,
            on_change=self.handle_variable_change
        )
        
        self.agent_toggle = ft.SegmentedButton(
            selected={"knn"},
            segments=[
                ft.Segment(
                    value="knn",
                    label="KNN",
                    icon=ft.icons.RADAR
                ),
                ft.Segment(
                    value="dt",
                    label="Árvore de Decisão",
                    icon=ft.icons.ACCOUNT_TREE
                ),
            ],
            on_change=self.toggle_agent
        )
        
        self.train_button = ft.ElevatedButton(
            "Treinar Modelo",
            icon=ft.icons.PLAY_ARROW_ROUNDED,
            on_click=self.train_model,
            disabled=True
        )
        
        self.results_container = ft.Container(
            content=ft.Markdown("### Resultados do modelo aparecerão aqui..."),
            bgcolor=ft.colors.SURFACE_VARIANT,
            padding=20,
            border_radius=10,
            width=600
        )

    def build(self):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    self.upload_button,
                    self.agent_toggle
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    self.x_dropdown,
                    self.y_dropdown,
                    self.train_button
                ]),
                ft.Container(
                    content=self.data_table,
                    height=200,
                    scroll=ft.ScrollMode.ALWAYS
                ),
                self.results_container
            ], spacing=20),
            padding=20
        )

    def handle_file_picked(self, e: ft.FilePickerResultEvent):
        """Manipula o arquivo selecionado"""
        if e.files:
            file_path = e.files[0].path
            logger.info(f"File picked: {file_path}")
            
            try:
                # Carrega dados e atualiza dropdowns
                columns = self.current_agent.load_data(file_path)
                self.x_dropdown.options = [ft.dropdown.Option(col) for col in columns]
                self.y_dropdown.options = [ft.dropdown.Option(col) for col in columns]
                
                # Atualiza tabela
                self.update_data_table()
                self.page.update()
                
            except Exception as ex:
                logger.error(f"Error loading file: {str(ex)}")
                self.page.show_snack_bar(
                    ft.SnackBar(content=ft.Text(f"Erro ao carregar arquivo: {str(ex)}"))
                )

    def update_data_table(self):
        """Atualiza a tabela de dados"""
        if self.current_agent.data is not None:
            preview = self.current_agent.get_table_preview()
            
            # Atualiza colunas
            self.data_table.columns = [
                ft.DataColumn(ft.Text(col))
                for col in preview.columns
            ]
            
            # Atualiza linhas
            self.data_table.rows = [
                ft.DataRow(
                    cells=[ft.DataCell(ft.Text(str(cell))) for cell in row]
                )
                for row in preview.values
            ]

    def handle_variable_change(self, e):
        """Manipula mudança nas variáveis X e Y"""
        if self.x_dropdown.value and self.y_dropdown.value:
            self.train_button.disabled = False
            self.page.update()

    def toggle_agent(self, e):
        """Alterna entre agentes KNN e Árvore de Decisão"""
        selected = e.control.selected.pop()
        self.current_agent = self.knn_agent if selected == "knn" else self.dt_agent
        logger.info(f"Switched to {self.current_agent.role}")
        
        # Mantém os dados se já carregados
        if self.x_dropdown.value and self.y_dropdown.value:
            self.current_agent.set_variables(
                self.x_dropdown.value,
                self.y_dropdown.value
            )

    def train_model(self, e):
        """Treina o modelo selecionado"""
        try:
            self.current_agent.set_variables(
                self.x_dropdown.value,
                self.y_dropdown.value
            )
            results = self.current_agent.train_model()
            self.results_container.content = ft.Markdown(results)
            self.page.update()
            
        except Exception as ex:
            logger.error(f"Error training model: {str(ex)}")
            self.page.show_snack_bar(
                ft.SnackBar(content=ft.Text(f"Erro ao treinar modelo: {str(ex)}"))
            )

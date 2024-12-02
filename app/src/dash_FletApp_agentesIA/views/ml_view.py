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
        # File picker para upload
        self.file_picker = ft.FilePicker(
            on_result=self.handle_file_picked
        )
        self.page.overlay.append(self.file_picker)
        
        # Botão de upload
        self.upload_button = ft.ElevatedButton(
            "Carregar arquivo Excel",
            icon=ft.icons.UPLOAD_FILE,
            on_click=lambda _: self.file_picker.pick_files(
                allowed_extensions=["xlsx", "xls"]
            )
        )
        
        # Tabela de dados
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Carregue um arquivo para ver os dados"))
            ],
            rows=[],
            border=ft.border.all(2, "grey"),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(3, "grey"),
            horizontal_lines=ft.border.BorderSide(1, "grey"),
        )
        
        # Dropdowns
        self.x_dropdown = ft.Dropdown(
            label="Variável X",
            width=200,
            on_change=self.handle_variable_change,
            disabled=True
        )
        
        self.y_dropdown = ft.Dropdown(
            label="Variável Y",
            width=200,
            on_change=self.handle_variable_change,
            disabled=True
        )
        
        # Seleção de agente
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
        
        # Botão treinar
        self.train_button = ft.ElevatedButton(
            "Treinar Modelo",
            icon=ft.icons.PLAY_ARROW_ROUNDED,
            on_click=self.train_model,
            disabled=True
        )
        
        # Container resultados
        self.results_container = ft.Container(
            content=ft.Markdown("### Resultados aparecerão aqui após treinar o modelo..."),
            bgcolor=ft.colors.SURFACE_VARIANT,
            padding=20,
            border_radius=10,
            width=600
        )
        
        # Container da tabela com scroll
        self.table_container = ft.Container(
            content=self.data_table,
            height=200,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=10,
            padding=10
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
                self.table_container,
                self.results_container
            ], 
            spacing=20,
            scroll=ft.ScrollMode.AUTO),
            padding=20
        )

    def handle_file_picked(self, e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            logger.info(f"File picked: {file_path}")
            
            try:
                # Carrega dados e atualiza dropdowns
                columns = self.current_agent.load_data(file_path)
                self.x_dropdown.options = [ft.dropdown.Option(col) for col in columns]
                self.y_dropdown.options = [ft.dropdown.Option(col) for col in columns]
                
                # Habilita os dropdowns
                self.x_dropdown.disabled = False
                self.y_dropdown.disabled = False
                
                # Atualiza tabela
                self.update_data_table()
                self.page.update()
                
                # Mostra mensagem de sucesso
                self.page.show_snack_bar(
                    ft.SnackBar(content=ft.Text("Arquivo carregado com sucesso!"))
                )
                
            except Exception as ex:
                logger.error(f"Error loading file: {str(ex)}")
                self.page.show_snack_bar(
                    ft.SnackBar(content=ft.Text(f"Erro ao carregar arquivo: {str(ex)}"))
                )

    def update_data_table(self):
        if self.current_agent.data is not None:
            preview = self.current_agent.get_table_preview()
            
            self.data_table.columns = [
                ft.DataColumn(ft.Text(col))
                for col in preview.columns
            ]
            
            self.data_table.rows = [
                ft.DataRow(
                    cells=[ft.DataCell(ft.Text(str(cell))) for cell in row]
                )
                for row in preview.values
            ]

    def handle_variable_change(self, e):
        if self.x_dropdown.value and self.y_dropdown.value:
            self.train_button.disabled = False
            self.page.update()

    def toggle_agent(self, e):
        selected = e.control.selected.pop()
        self.current_agent = self.knn_agent if selected == "knn" else self.dt_agent
        logger.info(f"Switched to {self.current_agent.role}")
        
        # Mantém os dados se já carregados
        if self.x_dropdown.value and self.y_dropdown.value:
            self.current_agent.set_variables(
                self.x_dropdown.value,
                self.y_dropdown.value
            )
            
        # Atualiza mensagem
        self.page.show_snack_bar(
            ft.SnackBar(content=ft.Text(f"Agente alterado para: {self.current_agent.role}"))
        )

    def train_model(self, e):
        try:
            logger.info("Training model...")
            self.current_agent.set_variables(
                self.x_dropdown.value,
                self.y_dropdown.value
            )
            results = self.current_agent.train_model()
            self.results_container.content = ft.Markdown(results)
            self.page.update()
            logger.info("Model trained successfully!")
            
            # Mostra mensagem de sucesso
            self.page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Modelo treinado com sucesso!"))
            )
            
        except Exception as ex:
            logger.error(f"Error training model: {str(ex)}")
            self.page.show_snack_bar(
                ft.SnackBar(content=ft.Text(f"Erro ao treinar modelo: {str(ex)}"))
            )

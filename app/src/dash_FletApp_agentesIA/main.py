import flet as ft
from views.regression_view import RegressionView
from views.ml_view import MLView
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(page: ft.Page):
    # Configurações da página
    page.title = "Dashboard de Agentes IA 2024"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.spacing = 0
    
    # Configuração da janela
    page.window.width = 1200
    page.window.height = 800
    page.window.title = "Dashboard de Agentes IA"
    
    # Views
    regression_view = RegressionView(page)
    ml_view = MLView(page)
    
    # Container principal para as views
    content = ft.Container(
        content=regression_view,
        expand=True,
        padding=20
    )
    
    def route_change(e):
        selected = e.control.selected_index
        content.content = regression_view if selected == 0 else ml_view
        page.update()
    
    # Barra de navegação
    navigation = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        leading=ft.Text("Agentes", size=20),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.SHOW_CHART,
                selected_icon=ft.icons.SHOW_CHART,
                label="Regressão",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.PSYCHOLOGY,
                selected_icon=ft.icons.PSYCHOLOGY,
                label="ML Agents",
            ),
        ],
        on_change=route_change,
    )
    
    # Layout principal
    page.add(
        ft.Row(
            [
                navigation,
                ft.VerticalDivider(width=1),
                content,
            ],
            expand=True,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)

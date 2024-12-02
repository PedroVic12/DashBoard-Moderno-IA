import flet as ft
from views.regression_view import RegressionView
from views.ml_view import MLView

class DashboardApp:
    def __init__(self):
        self.current_view = None
        
    def initialize(self, page: ft.Page):
        self.page = page
        self.page.title = "AI Agents Dashboard"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 0
        self.setup_layout()
        
    def setup_layout(self):
        self.navigation_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            leading=ft.FloatingActionButton(icon=ft.icons.CREATE, text="AI Agents"),
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.SHOW_CHART,
                    selected_icon=ft.icons.SHOW_CHART,
                    label="Regressão",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SCIENCE,
                    selected_icon=ft.icons.SCIENCE,
                    label="ML Agents",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SETTINGS,
                    selected_icon=ft.icons.SETTINGS,
                    label="Settings",
                ),
            ],
            on_change=self.navigation_change,
        )
        
        self.page.add(
            ft.Row(
                [
                    self.navigation_rail,
                    ft.VerticalDivider(width=1),
                    ft.Column([self.get_view(0)], expand=True),
                ],
                expand=True,
            )
        )
    
    def get_view(self, index: int) -> ft.View:
        if index == 0:
            return RegressionView(self.page)
        elif index == 1:
            return MLView(self.page)
        elif index == 2:
            return ft.Text("Settings View")
            
    def navigation_change(self, e):
        self.page.clean()
        self.page.add(
            ft.Row(
                [
                    self.navigation_rail,
                    ft.VerticalDivider(width=1),
                    ft.Column([self.get_view(e.control.selected_index)], expand=True),
                ],
                expand=True,
            )
        )

def main(page: ft.Page):
    app = DashboardApp()
    app.initialize(page)

if __name__ == "__main__":
    ft.app(target=main)

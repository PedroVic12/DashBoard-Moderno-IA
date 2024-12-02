import flet as ft
from views.regression_view import RegressionView
import os

class DashboardApp:
    def __init__(self):
        self.current_view = None
        
    def initialize(self, page: ft.Page):
        self.page = page
        self.page.title = "AI Agents Dashboard 2024"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 0
        self.setup_layout()
        
    def setup_layout(self):
        # Side Navigation
        self.nav_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            leading=ft.Icon(ft.icons.DASHBOARD_ROUNDED),
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.HOME_OUTLINED,
                    selected_icon=ft.icons.HOME_ROUNDED,
                    label="Home",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SETTINGS_OUTLINED,
                    selected_icon=ft.icons.SETTINGS_ROUNDED,
                    label="Settings",
                ),
            ],
            on_change=self.nav_change,
        )
        
        # Main content area
        self.content_area = ft.Container(
            content=self.build_home_view(),
            expand=True,
            padding=20,
        )
        
        # Main layout
        self.page.add(
            ft.Row(
                [
                    self.nav_rail,
                    ft.VerticalDivider(width=1),
                    self.content_area,
                ],
                expand=True,
            )
        )
    
    def build_home_view(self):
        return ft.Column(
            controls=[
                ft.Text("AI Agents", size=32, weight=ft.FontWeight.BOLD),
                ft.ResponsiveRow(
                    controls=[
                        # Regression Agent Card
                        ft.Container(
                            col={"sm": 12, "md": 6, "lg": 4},
                            content=ft.Card(
                                content=ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            ft.ListTile(
                                                leading=ft.Icon(ft.icons.ANALYTICS_ROUNDED, size=40),
                                                title=ft.Text("Regression Agent", size=20),
                                                subtitle=ft.Text("Linear regression analysis and prediction"),
                                            ),
                                            ft.Row(
                                                [
                                                    ft.TextButton("Open", on_click=self.open_regression_view),
                                                    ft.TextButton("Export"),
                                                ],
                                                alignment=ft.MainAxisAlignment.END,
                                            ),
                                        ],
                                    ),
                                    padding=10,
                                ),
                            ),
                            padding=10,
                        ),
                        # Add more agent cards here
                    ],
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        )
    
    def build_settings_view(self):
        return ft.Column(
            controls=[
                ft.Text("Settings", size=32, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.TextField(label="API Key", password=True),
                            ft.Dropdown(
                                label="Theme",
                                options=[
                                    ft.dropdown.Option("Light"),
                                    ft.dropdown.Option("Dark"),
                                ],
                            ),
                            ft.ElevatedButton("Save Settings"),
                        ],
                    ),
                    padding=20,
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    border_radius=10,
                ),
            ],
        )
    
    def nav_change(self, e):
        if e.control.selected_index == 0:  # Home
            self.content_area.content = self.build_home_view()
        elif e.control.selected_index == 1:  # Settings
            self.content_area.content = self.build_settings_view()
        self.page.update()
    
    def open_regression_view(self, e):
        if not self.current_view:
            self.current_view = RegressionView()
        self.content_area.content = self.current_view.build()
        self.page.update()

def main():
    app = DashboardApp()
    ft.app(target=app.initialize)

if __name__ == "__main__":
    main()

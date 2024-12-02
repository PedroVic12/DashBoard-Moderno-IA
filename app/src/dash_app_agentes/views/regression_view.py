import flet as ft
import pandas as pd
from agents.regression_agent import RegressionAgent

class RegressionView:
    def __init__(self):
        self.agent = RegressionAgent()
        self.data_table = None
        self.x_dropdown = None
        self.y_dropdown = None
        self.result_text = None
        
    def build(self):
        return ft.Column(
            controls=[
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.icons.ARROW_BACK,
                            on_click=self.go_back
                        ),
                        ft.Text("Regression Agent", size=32, weight=ft.FontWeight.BOLD),
                    ]
                ),
                self.build_data_input(),
                self.build_model_controls(),
                self.build_results(),
            ],
            scroll=ft.ScrollMode.AUTO,
        )
    
    def build_data_input(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Data Input", size=20, weight=ft.FontWeight.BOLD),
                    ft.ElevatedButton(
                        "Upload Data",
                        icon=ft.icons.UPLOAD_FILE,
                        on_click=self.pick_files
                    ),
                    ft.DataTable(
                        columns=[],
                        rows=[],
                        ref=self.data_table,
                    ) if self.data_table else ft.Text("No data loaded"),
                ]
            ),
            padding=20,
            bgcolor=ft.colors.SURFACE_VARIANT,
            border_radius=10,
            margin=ft.margin.only(top=20),
        )
    
    def build_model_controls(self):
        self.x_dropdown = ft.Dropdown(
            label="Select X variable",
            width=200,
            disabled=True
        )
        
        self.y_dropdown = ft.Dropdown(
            label="Select Y variable",
            width=200,
            disabled=True
        )
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Model Configuration", size=20, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        controls=[
                            self.x_dropdown,
                            self.y_dropdown,
                            ft.ElevatedButton(
                                "Train Model",
                                on_click=self.train_model,
                                disabled=True,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                ]
            ),
            padding=20,
            bgcolor=ft.colors.SURFACE_VARIANT,
            border_radius=10,
            margin=ft.margin.only(top=20),
        )
    
    def build_results(self):
        self.result_text = ft.Markdown(
            "",
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
        )
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Results", size=20, weight=ft.FontWeight.BOLD),
                    self.result_text,
                ]
            ),
            padding=20,
            bgcolor=ft.colors.SURFACE_VARIANT,
            border_radius=10,
            margin=ft.margin.only(top=20),
        )
    
    async def pick_files(self, e):
        file_picker = ft.FilePicker(
            on_result=self.handle_file_picked
        )
        e.page.overlay.append(file_picker)
        e.page.update()
        await file_picker.pick_files(
            allowed_extensions=["csv", "xlsx", "xls"],
            allow_multiple=False
        )
    
    def handle_file_picked(self, e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            columns = self.agent.load_data(file_path)
            
            # Update dropdowns
            self.x_dropdown.options = [ft.dropdown.Option(col) for col in columns]
            self.y_dropdown.options = [ft.dropdown.Option(col) for col in columns]
            self.x_dropdown.disabled = False
            self.y_dropdown.disabled = False
            
            # Update data table
            if self.agent.data is not None:
                self.update_data_table()
            
            e.page.update()
    
    def update_data_table(self):
        df = self.agent.data
        if len(df) > 10:
            df = df.head(10)  # Show only first 10 rows
            
        columns = [ft.DataColumn(ft.Text(col)) for col in df.columns]
        rows = []
        for _, row in df.iterrows():
            cells = [ft.DataCell(ft.Text(str(val))) for val in row]
            rows.append(ft.DataRow(cells=cells))
            
        self.data_table = ft.DataTable(
            columns=columns,
            rows=rows,
        )
    
    def train_model(self, e):
        if self.x_dropdown.value and self.y_dropdown.value:
            self.agent.set_variables(self.x_dropdown.value, self.y_dropdown.value)
            self.agent.train_model()
            
            # Update results
            equation = self.agent.get_equation()
            r2 = self.agent.r2
            
            result_md = f"""
### Model Results

**Regression Equation:**
```
{equation}
```

**R² Score:** {r2:.4f}

---
**Sample Predictions:**
```
X = 10 → Y = {self.agent.predict(10):.2f}
X = 20 → Y = {self.agent.predict(20):.2f}
X = 30 → Y = {self.agent.predict(30):.2f}
```
"""
            self.result_text.value = result_md
            e.page.update()
    
    def go_back(self, e):
        # This will be handled by the main app
        pass

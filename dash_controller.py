# controllers.py
class DashboardController:
    def __init__(self, data_model):
        self.data_model = data_model
        self.file_upload_component = FileUploadComponent("upload-data")
        self.data_table_component = DataTableComponent("data-table")
        self.chart_types = ["Bar Chart", "Line Chart", "Scatter Chart"]

    def update_table(self, contents, filename):
        if contents is not None:
            if self.data_model.load_data(contents, filename):
                return self.data_table_component.render(self.data_model.df)
            else:
                return html.Div("Erro ao carregar o arquivo. Verifique o formato.")
        else:
            return html.Div(
                "Nenhum arquivo selecionado. Arraste e solte ou selecione um arquivo CSV ou Excel."
            )

    def create_card(self, title, content):
        return CardComponent(title, content).render()

    def create_chart(self, selected_chart):
        if self.data_model.df.empty:
            return {}
        fig = None
        if selected_chart == "Bar Chart":
            fig = px.bar(
                self.data_model.df,
                x=self.data_model.df.columns[0],
                y=self.data_model.df.columns[1],
                color=self.data_model.df.columns[2],
            )
        elif selected_chart == "Line Chart":
            fig = px.line(
                self.data_model.df,
                x=self.data_model.df.columns[0],
                y=self.data_model.df.columns[1],
                color=self.data_model.df.columns[2],
            )
        elif selected_chart == "Scatter Chart":
            fig = px.scatter(
                self.data_model.df,
                x=self.data_model.df.columns[0],
                y=self.data_model.df.columns[1],
                color=self.data_model.df.columns[2],
            )

        fig.update_layout(
            title=f"{selected_chart} of AI Systems by Domain",
            xaxis_title="Year",
            yaxis_title="Annual Number of AI Systems",
            legend_title="Entity",
        )
        return fig

    def generate_insights(self, selected_chart):
        return f"This {selected_chart} shows the trends in the number of AI systems across different domains over time. You can see that..."

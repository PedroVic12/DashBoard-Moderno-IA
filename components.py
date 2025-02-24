import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Funções do Menu Lateral
def menu_lateral():
    """Cria o menu lateral para carregar dados e selecionar opções."""
    st.sidebar.markdown("---")
    st.sidebar.title("Carregar Dados")
    st.sidebar.markdown("---")
    
    uploaded_file = st.sidebar.file_uploader("Envie um arquivo Excel", type=["xlsx", "xls"])
    df = None
    
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file, sheet_name=None)  # Carrega todas as tabelas
            st.sidebar.success("Arquivo carregado com sucesso!")
        except Exception as e:
            st.sidebar.error(f"Erro ao carregar arquivo: {e}")
    else:
        st.sidebar.info("Envie um arquivo Excel para começar.")
    
    return df

def select_table(df):
    """Seleciona uma tabela do arquivo Excel carregado."""
    if df:
        table_name = st.sidebar.selectbox("Selecione a tabela", list(df.keys()))
        return df[table_name]
    return None

def select_axes(df):
    """Seleciona as colunas para os eixos X e Y."""
    x_col = st.sidebar.selectbox("Selecione a coluna para o eixo X", df.columns)
    y_col = st.sidebar.selectbox("Selecione a coluna para o eixo Y", df.columns)
    return x_col, y_col

def select_analysis_column(df):
    """Seleciona uma coluna para análise estatística."""
    st.sidebar.title("Análise do arquivo Excel")
    st.sidebar.markdown("---")
    return st.sidebar.selectbox("Selecione uma coluna para análise estatística", df.columns)

# Funções para input de arquivos
def input_img():
    """Função para carregar imagens."""
    st.sidebar.markdown("---")
    st.sidebar.title("Carregar Imagem")
    img_file = st.sidebar.file_uploader("Envie uma imagem", type=["jpg", "jpeg", "png"])
    return img_file

def input_pdf():
    """Função para carregar arquivos PDF."""
    st.sidebar.markdown("---")
    st.sidebar.title("Carregar PDF")
    pdf_file = st.sidebar.file_uploader("Envie um arquivo PDF", type=["pdf"])
    return pdf_file

# Função para formulário
def formulario():
    """Cria um formulário simples de entrada."""
    st.sidebar.markdown("---")
    st.sidebar.title("Formulário")
    
    with st.sidebar.form("form_dados"):
        nome = st.text_input("Nome")
        email = st.text_input("Email")
        idade = st.number_input("Idade", min_value=0, max_value=120)
        submit = st.form_submit_button("Enviar")
        
        if submit:
            return {"nome": nome, "email": email, "idade": idade}
    return None

# Funções de Header
def header():
    """Configura o cabeçalho do dashboard."""
    col1, col2, col3 = st.columns([1, 8, 1])
    
    with col1:
        menu_button = st.button("≡")
        if menu_button:
            st.session_state.show_menu = not st.session_state.get('show_menu', False)
    
    with col2:
        st.title("Dashboard Interativo")
    
    with col3:
        chat_button = st.button("🔔")
        if chat_button:
            st.session_state.show_chat = not st.session_state.get('show_chat', False)
    
    return st.session_state.get('show_menu', False), st.session_state.get('show_chat', False)

# Funções para Cards
def cards(df, stat_col):
    """Exibe estatísticas da coluna selecionada em formato de cards."""
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        # Só prossegue se a coluna for numérica
        if pd.api.types.is_numeric_dtype(df[stat_col]):
            col1.metric("Mínimo", f"{df[stat_col].min():.2f}", delta=None)
            col2.metric("Máximo", f"{df[stat_col].max():.2f}", delta=None)
            col3.metric("Média", f"{df[stat_col].mean():.2f}", delta=None)
            col4.metric("Desvio Padrão", f"{df[stat_col].std():.2f}", delta=None)
        else:
            st.info(f"A coluna '{stat_col}' não é numérica. Selecione uma coluna numérica para visualizar estatísticas.")
    except Exception as e:
        st.error(f"Erro ao calcular estatísticas: {e}")

# Funções para Footer
def footer():
    """Exibe o rodapé do dashboard."""
    st.markdown("""
        <footer style="margin-top: 50px; text-align: center; color: gray;">
        <p>Powered by <a href="https://streamlit.io/">Streamlit</a> and <a href="https://plotly.com/python/">Plotly</a></p>
        </footer>
    """, unsafe_allow_html=True)

# Classe ChatBot
class ChatBot:
    """Classe para gerenciar o chatbot lateral."""
    
    def __init__(self):
        if 'messages' not in st.session_state:
            st.session_state.messages = []

    def display_chat(self):
        """Exibe o chat e processa as mensagens."""
        st.sidebar.title("Chatbot")
        
        # Exibir mensagens anteriores
        for message in st.session_state.messages:
            with st.sidebar.chat_message(message["role"]):
                st.sidebar.write(message["content"])

        # Campo de entrada para nova mensagem
        if prompt := st.sidebar.chat_input("Digite sua mensagem..."):
            # Adicionar mensagem do usuário
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Simular resposta do bot (ping-pong)
            response = "pong" if prompt.lower() == "ping" else "Como posso ajudar?"
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

# Funções para criação de gráficos
class Graficos:
    """Classe para criar diferentes tipos de gráficos."""
    
    @staticmethod
    def scatter_plot(df, x_col, y_col):
        """Cria um gráfico de dispersão."""
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df[x_col], y=df[y_col],
            mode='lines+markers', name=f'{y_col} vs {x_col}'
        ))
        fig.update_layout(
            title=f'Gráfico de {y_col} vs {x_col}',
            xaxis_title=x_col,
            yaxis_title=y_col,
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        return fig

    @staticmethod
    def bar_plot(df, x_col, y_col):
        """Cria um gráfico de barras."""
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df[x_col], y=df[y_col], name=f'{y_col} vs {x_col}'
        ))
        fig.update_layout(
            title=f'Gráfico de Barras: {y_col} vs {x_col}',
            xaxis_title=x_col,
            yaxis_title=y_col,
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        return fig

    @staticmethod
    def pie_chart(df, x_col, y_col):
        """Cria um gráfico de pizza."""
        fig = go.Figure(data=[go.Pie(
            labels=df[x_col], values=df[y_col]
        )])
        fig.update_layout(
            title=f'Gráfico de Pizza: {y_col} por {x_col}',
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        return fig
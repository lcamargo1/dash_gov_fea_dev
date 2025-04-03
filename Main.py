import streamlit as st
import pandas as pd
import streamlit.components.v1 as stc
import plotly.express as px
import plotly.graph_objects as go
import time
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import plotly.subplots as sp
import plotly.graph_objects as go
from streamlit_elements import elements, mui, html
import numpy as np

st.set_page_config(
    page_title="Governança Fea.dev",
    layout="wide",  # Já está usando o layout wide, o que é bom
    initial_sidebar_state="collapsed"  # Mudar para collapsed para dar mais espaço à área principal
)

#theme_plotly = None

df = pd.read_excel("base.xlsx",sheet_name="Planilha1")

df.columns = df.columns.str.lower()

df["atividade_em_aberto"] = df["atividade_em_aberto"].astype(str)  


#st.sidebar.header("Filtro de Nome:")
nome = st.sidebar.multiselect(
    "filtro de teste:",
    options=df["assignee_username"].unique(),
    default=None
)
df_selection = df.query(
    "assignee_username == @nome"
)

st.image("logo.png",width=200)

st.markdown("""
<div>
<h3 style='margin-top: -70px;'> Deck de indicadores</h3>
<p style='margin-top: -15px;'> Objetivo: Acompanhar de forma centralizada o grau de engajamento dos membros sobre as atividades administrativas e dos projetos.</p>
</div>
""",unsafe_allow_html=True)

df_selection2 = df_selection.pivot_table(index="assignee_username",columns="tipo_atividade",values="id_tarefa",aggfunc="count",fill_value=0)
df_selection2.columns = df_selection2.columns.str.lower()

total_columns = []
if 'administrativo' in df_selection2.columns:
    total_columns.append(df_selection2["administrativo"])
else:
    df_selection2["administrativo"] = 0
    total_columns.append(df_selection2["administrativo"])
    
if 'projeto' in df_selection2.columns:
    total_columns.append(df_selection2["projeto"])
else:
    df_selection2["projeto"] = 0
    total_columns.append(df_selection2["projeto"])

# Sum all columns that should contribute to total
df_selection2["total"] = sum(total_columns)

st.markdown("""
<div style='line-height: 1.0;margin-top: 20px;'>
<h5>Quantidade de atividades por membro ativo</h5>
<p style='margin-top: -10px;'>Considerar 'Administrativo' todas as atividades que não estão presentes no click-up dos cases ou dos projetos em edital</p>
</div>
""", unsafe_allow_html=True)


df_selection2 = df_selection2.rename(columns={"administrativo":"Administrativo","projeto":"Projeto","total":"Total de Atividades"})
df_selection2.index.names = ['Nome']

st.dataframe(df_selection2, use_container_width=True)


st.markdown("""
<div style='line-height: 1.0;'>
<p>Quantidade máxima de dias em aberto (por atividade)</p>
<p style='margin-top: -10px;'>'0' Significa que a atividade está concluída.</p> 
<p style='margin-top: -10px;'>'1' Significa que a tarefa ainda está em andamento.</p>
</div>
""",unsafe_allow_html=True)


df_selection3 = df_selection.pivot_table(index="nome",columns="atividade_em_aberto",values="dias_em_aberto",aggfunc="max",fill_value=0)
df_selection3.columns = df_selection3.columns.str.lower()

#df_selection3 = df_selection3.sort_values(by="dias_em_aberto",ascending=False)

#df_selection3 = df_selection3.sort_values(by="dias_em_aberto",ascending=False)

df_selection3 = df_selection3.rename(columns={"dias_em_aberto":"Dias em Aberto"})

df_selection3.index.names = ['Tarefa']

st.dataframe(df_selection3, use_container_width=True)

from plotly.subplots import make_subplots

fig_top = make_subplots(
    rows=1, 
    cols=2, 
    subplot_titles=("Atividades por membro", "Dias em aberto por tarefa")
)

fig_top.add_trace(go.Bar(x=df["assignee_username"], y=df["atividade_em_aberto"], name="Total de Atividades"), row=1, col=1)
fig_top.add_trace(go.Bar(x=df["assignee_username"], y=df["atividade_em_aberto"], name="Dias em Aberto"), row=1, col=2)
fig_top.update_layout(height=400, showlegend=True)

# Gráfico inferior
fig_bottom = make_subplots(
    rows=1, 
    cols=2, 
    subplot_titles=("Gráfico 3", "Gráfico 4")  # Altere os títulos conforme necessário
)

fig_bottom.add_trace(go.Bar(x=df["assignee_username"], y=df["atividade_em_aberto"], name="Total de Atividades"), row=1, col=1)
fig_bottom.add_trace(go.Bar(x=df["assignee_username"], y=df["atividade_em_aberto"], name="Dias em Aberto"), row=1, col=2)
fig_bottom.update_layout(height=400, showlegend=True)


# Gráfico inferior
fig_bottom2 = make_subplots(
    rows=1, 
    cols=3, 
    subplot_titles=("Gráfico 5", "Gráfico 6")  # Altere os títulos conforme necessário
)

fig_bottom.add_trace(go.Bar(x=df["assignee_username"], y=df["atividade_em_aberto"], name="Total de Atividades"), row=1, col=1)
fig_bottom.add_trace(go.Bar(x=df["assignee_username"], y=df["atividade_em_aberto"], name="Dias em Aberto"), row=1, col=2)
fig_bottom.update_layout(height=400, showlegend=True)



# Exibir os gráficos um após o outro
st.plotly_chart(fig_top, use_container_width=True)
st.plotly_chart(fig_bottom, use_container_width=True)
st.plotly_chart(fig_bottom2, use_container_width=True)


df_teste = pd.read_excel("reuniões_semanais.xlsx",sheet_name="Sheet1")


df_selection


#df_selection.groupby(by=["assignee_username"]).count()[["tipo_atividade"]]
#teste = px.bar()





#filtro = df[df["assignee_username"] == "Lucas dos Santos Camargo"]

#filtro

#teste = filtro.pivot_table(index="assignee_username",columns="tipo_atividade",values="id_tarefa",aggfunc="count")

#teste.columns = teste.columns.str.lower()

#teste = teste.reset_index(drop=True)

#teste.columns

#teste["total"] = teste["administrativo"] + teste["projeto"]

#teste.columns







#st.dataframe(df,use_container_width=True)

#st.sidebar.header("Filtro: ")
#membro_dev = st.sidebar.multiselect(
##    "teste",
 #   options=df["assignee_username"].unique(),
 #   default=None
#)

#df_selection = df.query(
#    "assignee_username == @membro_dev"
#)


#teste = df.pivot_table(index="assignee_username",columns="tipo_atividade",values="id_tarefa",#aggfunc="count",margins=True)

#teste = teste.reset_index()

#teste.columns = teste.columns.str.lower()
#teste.columns


#base = teste[["assignee_username","administrativo","projeto","all"]]

#base = base.reset_index(drop=True)

#eixo_x = sum(base["administrativo"])
#eixo_y = sum(base["projeto"])

#fig = go.Figure()
#fig.add_trace(go.Bar(x=["administrativo"],y=sum(base["administrativo"])))
#fig.add_trace(go.Bar(x=["projeto"],y=(base["projeto"])))
#fig.show()

#print(base)s



# 

#    with st.expander("My database"):

#        shwdata = st.multiselect('Filter :',df_selection.columns,default=[])
#        st.dataframe(df_selection[shwdata],use_container_width=True)


#homepage()
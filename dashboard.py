import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados (substitua 'dataset.csv' pelo nome correto do arquivo)
@st.cache_data
def load_data():
    df = pd.read_excel("data.xlsx", sheet_name="Data")
    return df

df = load_data()

# ---- Sidebar para Filtros ----
st.sidebar.header("Filtros")
selected_year = st.sidebar.slider("Selecione o Ano de Fundação", int(df["founded"].min()), int(df["founded"].max()), step=1)
selected_city = st.sidebar.multiselect("Selecione a Cidade", df["location"].unique())

# ---- Pergunta 1: Indústria mais investida por ano ----
st.header("📈 Indústria mais investida por ano")
invested_industry = df.groupby(["founded", "industry"])["team_size"].sum().reset_index()
fig1 = px.line(invested_industry, x="founded", y="team_size", color="industry", title="Indústria mais investida ao longo dos anos")
st.plotly_chart(fig1)

# ---- Pergunta 2: Top 10 cidades com mais empresas ----
st.header("🌍 Top 10 cidades com mais startups fundadas")
top_cities = df["location"].value_counts().head(10).reset_index()
top_cities.columns = ["location", "count"]
fig2 = px.bar(top_cities, x="location", y="count", title="Top 10 Cidades com Mais Startups", color="location")
st.plotly_chart(fig2)

# ---- Pergunta 3: Indústrias mais bem-sucedidas (Public / Acquired) ----
st.header("🏆 Indústrias mais bem-sucedidas")
successful_industries = df[df["status"].isin(["Public", "Acquired"])].groupby("industry")["name"].count().reset_index()
successful_industries.columns = ["industry", "count"]
successful_industries = successful_industries.sort_values(by="count", ascending=False).head(10)
fig3 = px.bar(successful_industries, x="industry", y="count", title="Top Indústrias Bem-Sucedidas", color="industry")
st.plotly_chart(fig3)

# Média de time das empresas bem-sucedidas
avg_team_size = df[df["status"].isin(["Public", "Acquired"])]["team_size"].mean()
st.write(f"📊 Média de tamanho de equipe das empresas bem-sucedidas: **{avg_team_size:.2f}** funcionários.")

# ---- Pergunta 4: Indústrias menos bem-sucedidas (Archived) ----
st.header("📉 Indústrias menos bem-sucedidas")
failed_industries = df[df["status"] == "Archived"].groupby("industry")["name"].count().reset_index()
failed_industries.columns = ["industry", "count"]
failed_industries = failed_industries.sort_values(by="count", ascending=False).head(10)
fig4 = px.bar(failed_industries, x="industry", y="count", title="Indústrias com Mais Falências", color="industry")
st.plotly_chart(fig4)

# ---- Pergunta 5: Melhor indústria para investir ----
st.header("💰 Melhor indústria para investir")
investment_industry = successful_industries.iloc[0]["industry"]
st.write(f"🔹 A melhor indústria para investir é: **{investment_industry}**")
st.write("Justificativa: Esta indústria tem o maior número de empresas bem-sucedidas.")

# ---- Pergunta 6: Melhor empresa para investir ----
st.header("🚀 Melhor empresa para investir")
best_company = df[df["status"] == "Active"].sort_values(by=["team_size", "jobs"], ascending=False).iloc[0]
st.write(f"🏅 A melhor empresa para investir é: **{best_company['name']}**")
st.write(f"🌍 Localização: {best_company['location']}")
st.write(f"📊 Tamanho da equipe: {best_company['team_size']}")
st.write(f"🔗 [Site oficial]({best_company['website']})")
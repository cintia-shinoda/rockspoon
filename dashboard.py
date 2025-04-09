import streamlit as st
import pandas as pd
import plotly.express as px

# Data Loading
@st.cache_data
def load_data():
    df = pd.read_excel("data.xlsx", sheet_name="Data")
    return df

df = load_data()

# ---- Sidebar to filters ----
st.sidebar.header("Filters")
selected_year = st.sidebar.slider("Select the year of foundation", int(df["founded"].min()), int(df["founded"].max()), step=1)
selected_city = st.sidebar.multiselect("Select the city", df["location"].unique())

# ---- 1: Mosto invested industry by year ----
st.header("The most invested industry by year")
invested_industry = df.groupby(["founded", "industry"])["team_size"].sum().reset_index()
fig1 = px.line(invested_industry, x="founded", y="team_size", color="industry", title="Invested Industry by Year")
st.plotly_chart(fig1)

# ---- 2: Top 10 cities in number of companies ----
st.header("🌍 Top 10 cities")
top_cities = df["location"].value_counts().head(10).reset_index()
top_cities.columns = ["location", "count"]
fig2 = px.bar(top_cities, x="location", y="count", title="Top 10 Cities", color="location")
st.plotly_chart(fig2)

# ---- 3: Successful Companies (Public / Acquired) ----
st.header("Successful Companies (Public / Acquired)")
successful_industries = df[df["status"].isin(["Public", "Acquired"])].groupby("industry")["name"].count().reset_index()
successful_industries.columns = ["industry", "count"]
successful_industries = successful_industries.sort_values(by="count", ascending=False).head(10)
fig3 = px.bar(successful_industries, x="industry", y="count", title="Top Successful Industries", color="industry")
st.plotly_chart(fig3)

# ---- 4: Average team size of successful companies ----
avg_team_size = df[df["status"].isin(["Public", "Acquired"])]["team_size"].mean()
st.write(f"Average team size of successful companies : **{avg_team_size:.2f}** funcionários.")

# ---- 5: Unsuccessful industries (Inactive) ----
st.header("Unsuccessful Industries (Inactive)")
failed_industries = df[df["status"] == "Inactive"].groupby("industry")["name"].count().reset_index()
failed_industries.columns = ["industry", "count"]
failed_industries = failed_industries.sort_values(by="count", ascending=False).head(10)
fig4 = px.bar(failed_industries, x="industry", y="count", title="Failed industries", color="industry")
st.plotly_chart(fig4)

# ---- 6: Best industry to invvest ----
st.header("Best industry to invest")
investment_industry = successful_industries.iloc[0]["industry"]
st.write(f"The best industry to invest is: **{investment_industry}**")
st.write("It's the industry with the most successful companies")

# ---- 7: Best company to invest ----
st.header("Best company to invest")
best_company = df[df["status"] == "Active"].sort_values(by=["team_size", "jobs"], ascending=False).iloc[0]
st.write(f"Best company to invest: **{best_company['name']}**")
st.write(f"Localization: {best_company['location']}")
st.write(f"Team size: {best_company['team_size']}")
st.write(f"Official website]({best_company['website']})")
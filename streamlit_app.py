import streamlit as st
import pandas as pd
import altair as alt

import matplotlib      
matplotlib.use('Agg')  

import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="COVID Data Viz", layout="wide")
st.title("COVID-19: Deaths & Vaccination — Interactive Dashboard")

# Load data from OWID URL or user upload
@st.cache_data
def load_data(uploaded_file=None):
    usecols = ['date', 'location', 'new_deaths_smoothed', 'people_vaccinated_per_hundred']
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, usecols=usecols)
    else:
        url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
        df = pd.read_csv(url, usecols=usecols)

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

# Sidebar upload option (optional)
uploaded = st.sidebar.file_uploader("Upload your own OWID COVID-19 CSV", type=['csv'])
df = load_data(uploaded)

# Validate dataset
expected = ['date', 'location', 'new_deaths_smoothed', 'people_vaccinated_per_hundred']
missing = [c for c in expected if c not in df.columns]
if missing:
    st.error(f"Dataset is missing columns: {missing}")
    st.stop()

# Sidebar filters
all_countries = sorted(df['location'].dropna().unique())
default = ["United States", "India", "Brazil", "United Kingdom"]
selected_countries = st.sidebar.multiselect("Select countries", all_countries, default)

min_date = df['date'].min().date()
max_date = df['date'].max().date()
date_range = st.sidebar.date_input("Date range", [min_date, max_date], min_value=min_date, max_value=max_date)

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
else:
    start = end = pd.to_datetime(date_range)

# Filter data
mask = df['location'].isin(selected_countries) & (df['date'] >= start) & (df['date'] <= end)
data = df.loc[mask, expected].dropna(how='all')

if data.empty:
    st.warning("No rows match your filters.")
    st.stop()

# Show table
st.subheader("Filtered data (first 200 rows)")
st.dataframe(data.head(200), use_container_width=True)

# Altair Charts
st.subheader("New deaths (smoothed) over time")
chart_deaths = (
    alt.Chart(data)
    .mark_line()
    .encode(
        x=alt.X('date:T', title='Date'),
        y=alt.Y('new_deaths_smoothed:Q', title='New deaths (smoothed)'),
        color='location:N',
        tooltip=['date:T', 'location:N', 'new_deaths_smoothed:Q']
    )
    .interactive()
)
st.altair_chart(chart_deaths, use_container_width=True)

st.subheader("People vaccinated per hundred")
chart_vax = (
    alt.Chart(data)
    .mark_line()
    .encode(
        x='date:T',
        y=alt.Y('people_vaccinated_per_hundred:Q', title='People vaccinated per 100'),
        color='location:N',
        tooltip=['date:T', 'location:N', 'people_vaccinated_per_hundred:Q']
    )
    .interactive()
)
st.altair_chart(chart_vax, use_container_width=True)

st.subheader("Deaths vs Vaccinations (scatter)")
scatter = (
    alt.Chart(data)
    .mark_circle(size=60)
    .encode(
        x=alt.X('people_vaccinated_per_hundred:Q', title='People vaccinated per 100'),
        y=alt.Y('new_deaths_smoothed:Q', title='New deaths (smoothed)'),
        color='location:N',
        tooltip=['date:T', 'location:N', 'new_deaths_smoothed:Q', 'people_vaccinated_per_hundred:Q']
    )
    .interactive()
)
st.altair_chart(scatter, use_container_width=True)

st.subheader("Cumulative deaths by country")
cumulative = data.groupby("location")['new_deaths_smoothed'].sum().reset_index()
bar_chart = (
    alt.Chart(cumulative)
    .mark_bar()
    .encode(
        x=alt.X('new_deaths_smoothed:Q', title='Total deaths (smoothed sum)'),
        y=alt.Y('location:N', sort='-x'),
        color='location:N',
        tooltip=['location:N', 'new_deaths_smoothed:Q']
    )
)
st.altair_chart(bar_chart, use_container_width=True)

st.subheader("Heatmap: Vaccination vs Deaths")
heatmap = (
    alt.Chart(data)
    .mark_rect()
    .encode(
        x=alt.X('date:T', title='Date'),
        y=alt.Y('location:N', title='Country'),
        color=alt.Color('new_deaths_smoothed:Q', scale=alt.Scale(scheme='reds'), title='Deaths'),
        tooltip=['date:T', 'location:N', 'new_deaths_smoothed:Q', 'people_vaccinated_per_hundred:Q']
    )
)
st.altair_chart(heatmap, use_container_width=True)

# Optional: Seaborn/Matplotlib plots
# Optional: Seaborn/Matplotlib plots
if st.sidebar.checkbox("Show Seaborn/Matplotlib plots"):
    st.subheader("Seaborn/Matplotlib Versions")

    # Chart 1
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=data, x='date', y='new_deaths_smoothed', hue='location', ax=ax)
    ax.set_title("COVID-19 Deaths Over Time")
    ax.set_xlabel("")
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    st.pyplot(fig)
    plt.close(fig) # Correct

    # Chart 2
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=data, x='date', y='people_vaccinated_per_hundred', hue='location', ax=ax2)
    ax2.set_title("Vaccination Progress Over Time")
    ax2.set_xlabel("")
    ax2.legend(loc='upper left', bbox_to_anchor=(1, 1))
    st.pyplot(fig2)
    plt.close(fig2) # Correct

    # Chart 3
    fig3, ax3 = plt.subplots(figsize=(6, 6))
    sns.scatterplot(data=data, x='people_vaccinated_per_hundred', y='new_deaths_smoothed', hue='location', ax=ax3)
    ax3.set_title("Deaths vs Vaccinations (scatter)")
    st.pyplot(fig3)
    plt.close(fig3) # Add this line

    # Chart 4
    fig4, ax4 = plt.subplots(figsize=(6, 4))
    sns.barplot(data=cumulative, x='new_deaths_smoothed', y='location', ax=ax4)
    ax4.set_title("Cumulative deaths by country")
    st.pyplot(fig4)
    plt.close(fig4) # Add this line

    # Chart 5
    pivot_data = data.pivot_table(index='location', columns='date', values='new_deaths_smoothed')
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot_data, cmap="Reds", cbar_kws={'label': 'Deaths'}, ax=ax5)
    ax5.set_title("Heatmap: Deaths across countries and dates")
    st.pyplot(fig5)
    plt.close(fig5) # Add this line
    
# CSV Download
csv = data.to_csv(index=False)
st.download_button("Download filtered CSV", csv, file_name="filtered_covid_data.csv", mime="text/csv")




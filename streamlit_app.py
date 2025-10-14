import streamlit as st
import pandas as pd
import altair as alt
import matplotlib
matplotlib.use('Agg') # Set non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import st_folium
import requests

# --- Page Configuration ---
st.set_page_config(page_title="COVID Data Viz", layout="wide")
st.title("COVID-19: Deaths & Vaccination — Interactive Dashboard")

# --- Data Loading ---
@st.cache_data
def load_data(uploaded_file=None):
    """Loads COVID data from OWID URL or a user-uploaded file."""
    usecols = ['date', 'location', 'new_deaths_smoothed', 'people_vaccinated_per_hundred']
    try:
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file, usecols=usecols)
        else:
            url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
            df = pd.read_csv(url, usecols=usecols)
        
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# --- Sidebar and Filters ---
st.sidebar.header("Dashboard Filters")
uploaded = st.sidebar.file_uploader("Upload your own OWID COVID-19 CSV", type=['csv'])
df = load_data(uploaded)

if not df.empty:
    # Validate dataset
    expected = ['date', 'location', 'new_deaths_smoothed', 'people_vaccinated_per_hundred']
    if not all(c in df.columns for c in expected):
        st.error(f"Dataset is missing one or more required columns: {expected}")
        st.stop()

    all_countries = sorted(df['location'].dropna().unique())
    default = ["United States", "India", "Brazil", "United Kingdom"]
    selected_countries = st.sidebar.multiselect("Select countries", all_countries, default=default)

    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    date_range = st.sidebar.date_input("Date range", [min_date, max_date], min_value=min_date, max_value=max_date)

    # --- Data Filtering ---
    if len(date_range) == 2:
        start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        mask = df['location'].isin(selected_countries) & (df['date'] >= start) & (df['date'] <= end)
        data = df.loc[mask].copy() # Use .copy() to avoid SettingWithCopyWarning
    else:
        st.warning("Please select a valid date range.")
        st.stop()

    if data.empty:
        st.warning("No data available for the selected filters.")
        st.stop()
    
    # --- Main Page Display ---
    st.subheader("Filtered data (first 200 rows)")
    st.dataframe(data.head(200), use_container_width=True)

    # --- Altair Charts ---
    st.header("Altair Visualizations")
    
    st.subheader("New deaths (smoothed) over time")
    chart_deaths = alt.Chart(data).mark_line().encode(
        x=alt.X('date:T', title='Date'),
        y=alt.Y('new_deaths_smoothed:Q', title='New deaths (smoothed)'),
        color='location:N',
        tooltip=['date:T', 'location:N', 'new_deaths_smoothed:Q']
    ).interactive()
    st.altair_chart(chart_deaths, use_container_width=True)

    st.subheader("People vaccinated per hundred")
    chart_vax = alt.Chart(data).mark_line().encode(
        x='date:T',
        y=alt.Y('people_vaccinated_per_hundred:Q', title='People vaccinated per 100'),
        color='location:N',
        tooltip=['date:T', 'location:N', 'people_vaccinated_per_hundred:Q']
    ).interactive()
    st.altair_chart(chart_vax, use_container_width=True)

    st.subheader("Deaths vs Vaccinations (scatter)")
    scatter = alt.Chart(data).mark_circle(size=60).encode(
        x=alt.X('people_vaccinated_per_hundred:Q', title='People vaccinated per 100'),
        y=alt.Y('new_deaths_smoothed:Q', title='New deaths (smoothed)'),
        color='location:N',
        tooltip=['date:T', 'location:N', 'new_deaths_smoothed:Q', 'people_vaccinated_per_hundred:Q']
    ).interactive()
    st.altair_chart(scatter, use_container_width=True)

    # --- Folium Map ---
    if st.sidebar.checkbox("Show Folium Map"):
        st.header("Geographic Data Map")
        map_type = st.sidebar.radio("Select map type", ("Deaths Intensity", "Vaccination Progress"))

        st.subheader(f"Global COVID-19 Map — {map_type}")

        # Prepare aggregated data
        if map_type == "Deaths Intensity":
            map_data = data.groupby("location")["new_deaths_smoothed"].mean().reset_index()
            map_data = map_data.rename(columns={"new_deaths_smoothed": "metric"})
            legend_label = "Average New Deaths (Smoothed)"
            color_scheme = "YlOrRd"
        else:
            map_data = data.groupby("location")["people_vaccinated_per_hundred"].max().reset_index()
            map_data = map_data.rename(columns={"people_vaccinated_per_hundred": "metric"})
            legend_label = "Max People Vaccinated per 100"
            color_scheme = "YlGnBu"
        
        # *** FIX: Map OWID country names to GeoJSON country names ***
        country_name_mapping = {
            "United States": "United States of America",
            "United Kingdom": "United Kingdom",
            "Democratic Republic of Congo": "Democratic Republic of the Congo",
            "Congo": "Republic of the Congo",
            "Czechia": "Czech Republic",
            "Timor": "Timor-Leste",
            "Cote d'Ivoire": "Ivory Coast"
        }
        map_data['location'] = map_data['location'].replace(country_name_mapping)

        # Load world GeoJSON
        geo_url = "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/world-countries.json"
        try:
            geo_json = requests.get(geo_url).json()
            
            m = folium.Map(location=[20, 0], zoom_start=2, tiles="cartodb positron")

            folium.Choropleth(
                geo_data=geo_json,
                data=map_data,
                columns=["location", "metric"],
                key_on="feature.properties.name",
                fill_color=color_scheme,
                fill_opacity=0.7,
                line_opacity=0.2,
                nan_fill_color="lightgray",
                legend_name=legend_label
            ).add_to(m)

            st_folium(m, width=900, height=500)
        except Exception as e:
            st.error(f"Could not load or process map data: {e}")

    # --- Optional Seaborn/Matplotlib Plots ---
    if st.sidebar.checkbox("Show Seaborn/Matplotlib plots"):
        st.header("Seaborn/Matplotlib Visualizations")

        # Prepare cumulative data for bar chart
        cumulative = data.groupby("location")['new_deaths_smoothed'].sum().reset_index()

        # Chart 1: Deaths Over Time
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.lineplot(data=data, x='date', y='new_deaths_smoothed', hue='location', ax=ax)
        ax.set_title("COVID-19 Deaths Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("New Deaths (Smoothed)")
        ax.legend(title='Country')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        plt.close(fig)

        # Chart 2: Vaccinations Over Time
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        sns.lineplot(data=data, x='date', y='people_vaccinated_per_hundred', hue='location', ax=ax2)
        ax2.set_title("Vaccination Progress Over Time")
        ax2.set_xlabel("Date")
        ax2.set_ylabel("People Vaccinated per 100")
        ax2.legend(title='Country')
        plt.xticks(rotation=45)
        st.pyplot(fig2)
        plt.close(fig2)
        
    # --- CSV Download ---
    @st.cache_data
    def convert_df_to_csv(df_to_convert):
        return df_to_convert.to_csv(index=False).encode('utf-8')

    csv = convert_df_to_csv(data)
    st.download_button(
        "Download filtered data as CSV",
        csv,
        file_name="filtered_covid_data.csv",
        mime="text/csv",
    )
else:
    st.info("Awaiting data load...")

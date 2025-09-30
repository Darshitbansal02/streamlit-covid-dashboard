# COVID-19 Deaths & Vaccinations — A Data Story

## 1. Introduction

The COVID-19 pandemic has been one of the most significant global health crises in recent history, affecting millions of people and placing enormous pressure on healthcare systems worldwide. Beyond the human toll, the pandemic also generated massive amounts of data, making it an important case study for data visualization and storytelling.

In this project, I use the **Our World in Data (OWID) COVID-19 dataset** to explore two key aspects of the pandemic:

* Daily deaths due to COVID-19
* Progress of vaccination campaigns

The goal is to demonstrate how data visualization can be used not only for analysis but also for **effective storytelling**. I use **Matplotlib** and **Seaborn** for creating static plots, and also built an interactive application with **Streamlit** to allow users to explore the data themselves.

---

## 2. Methodology

### Tools Used

* **Python** (Pandas for data manipulation)
* **Matplotlib and Seaborn** for visualizations
* **Altair** for interactive charts
* **Streamlit** for building a deployable web app

### Dataset

* Source: [Our World in Data (OWID) COVID-19](https://ourworldindata.org/covid-deaths)
* Columns used:

  * `date`
  * `location` (country)
  * `new_deaths_smoothed` (7-day smoothed deaths)
  * `people_vaccinated_per_hundred` (percentage of population vaccinated)

---

## 3. Visualisations

### 3.1 COVID-19 Deaths Over Time

Using **Seaborn line plots**, I visualized smoothed daily deaths across multiple countries. This revealed clear peaks during different waves of the pandemic. For example, the United States and India experienced significant spikes during early 2021 and mid-2021 respectively.

*Key Insight:*
The timing and intensity of waves varied widely by country, showing that the pandemic did not follow a uniform global trajectory.

### 3.2 Vaccination Progress

Another visualization focused on the percentage of people vaccinated per hundred. Countries such as the United States and the United Kingdom achieved rapid early vaccination, while others like India ramped up later in 2021.

*Key Insight:*
Vaccination rollout speed was highly uneven, reflecting differences in supply, infrastructure, and policy.

### 3.3 Interactive Storytelling

The **Streamlit app** allows users to:

* Filter by countries and date ranges
* Compare trends interactively using Altair charts
* Download filtered data for further analysis

This interactivity transforms static insights into a **personalized data exploration tool**.

---

## 4. Misleading Visualization & Redesign

### Misleading Chart

In one version of the vaccination chart, I truncated the y-axis to start at **50 instead of 0**. This exaggerated the differences between countries and made the gaps appear larger than they really were.

**Why it’s misleading:**

* By not showing the full axis, the chart visually amplifies small differences.
* It may lead viewers to believe one country’s vaccination campaign was far more effective than another’s.

### Corrected Chart

In the redesigned version, the y-axis starts at **0 and ends at 100** (percent scale). This provides proper context and ensures the visualization accurately reflects the real differences.

**Lesson learned:**
A small design choice, such as axis scaling, can completely change the perception of the data. Ethical visualization requires avoiding manipulations that distort reality.

---

## 5. Storytelling with the Dataset

The combination of deaths and vaccination data allows us to tell a compelling story:

* **Early Pandemic (2020):** Most countries struggled with rising deaths and had no vaccine protection.
* **Early 2021:** Vaccination campaigns began, with high-income countries leading the rollout. Deaths began to stabilize where vaccination rates increased quickly.
* **Mid–Late 2021:** Countries like India and Brazil caught up in vaccination efforts, leading to visible declines in deaths after massive second waves.
* **Overall:** Vaccination progress is strongly correlated with a reduction in COVID-19 deaths, although the relationship is influenced by other factors such as new variants and healthcare capacity.

This narrative demonstrates how **visualization is not just about charts, but about uncovering and communicating stories hidden in the data.**

---

## 6. Conclusion

Through this project, I learned:

* **Visualization choices matter.** A poorly designed chart can mislead, while a thoughtful redesign can clarify.
* **Interactivity enhances storytelling.** Streamlit and Altair provide tools for users to engage with the data directly.
* **Data storytelling combines analysis and narrative.** Numbers alone are not enough — effective communication requires context, design, and narrative flow.

The final deliverable is both a **set of static plots** created using Matplotlib and Seaborn and a **deployable interactive Streamlit app** for exploring COVID-19 deaths and vaccinations. This approach highlights the power of visualization not just for analysis but for public understanding and communication during global crises.

---

## 7. References

* Our World in Data (COVID-19 Dataset): [https://ourworldindata.org/covid-deaths](https://ourworldindata.org/covid-deaths)
* Streamlit Documentation: [https://docs.streamlit.io](https://docs.streamlit.io)
* Seaborn Documentation: [https://seaborn.pydata.org](https://seaborn.pydata.org)
* Altair Documentation: [https://altair-viz.github.io](https://altair-viz.github.io)

---

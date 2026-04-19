# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.19.10",
#     "pandas>=2.3.3",
#     "plotly>=6.5.1",
#     "pyarrow>=22.0.0",
#     "pyzmq>=27.1.0",
# ]
# ///

import marimo

__generated_with = "0.23.1"
app = marimo.App()


@app.cell
async def _():
    import marimo as mo
    import pandas as pd

    try:
        import plotly.express as px
    except ImportError:
        import micropip
        await micropip.install("plotly")
        import plotly.express as px

    return mo, pd, px


@app.cell
def _():
    return


@app.cell
def _(mo):
    title = mo.md("""
    # 🎓 Personal Portfolio Webpage

    A professional portfolio built with **marimo**, combining personal profile,
    project highlights, and an interactive finance dashboard.
    """)
    return (title,)


@app.cell
def _(pd):
    csv_url = "https://gist.githubusercontent.com/DrAYim/80393243abdbb4bfe3b45fef58e8d3c8/raw/ed5cfd9f210bf80cb59a5f420bf8f2b88a9c2dcd/sp500_ZScore_AvgCostofDebt.csv"

    try:
        df_final = pd.read_csv(csv_url)
        data_message = "Loaded live portfolio data from the online CSV."
    except Exception:
        # Fallback dataset so the app still works
        df_final = pd.DataFrame({
            "Name": ["Apple", "Microsoft", "JPMorgan", "Tesla", "Goldman Sachs", "Amazon"],
            "Ticker": ["AAPL", "MSFT", "JPM", "TSLA", "GS", "AMZN"],
            "Sector_Key": [
                "Technology",
                "Technology",
                "Financial Services",
                "Consumer Cyclical",
                "Financial Services",
                "Consumer Cyclical",
            ],
            "AvgCost_of_Debt": [0.021, 0.018, 0.034, 0.029, 0.041, 0.024],
            "Z_Score_lag": [4.5, 5.1, 2.4, 3.0, 1.9, 3.8],
            "Market_Cap": [2800000000000, 3100000000000, 550000000000, 750000000000, 130000000000, 1900000000000],
        })
        data_message = "Online CSV could not be loaded, so a built-in sample dataset is being used."

    df_final = df_final.dropna(subset=["AvgCost_of_Debt", "Z_Score_lag", "Sector_Key"])
    df_final = df_final[df_final["AvgCost_of_Debt"] < 5].copy()
    df_final["Debt_Cost_Percent"] = df_final["AvgCost_of_Debt"] * 100
    df_final["Market_Cap_B"] = df_final["Market_Cap"] / 1e9
    return data_message, df_final


@app.cell
def _(data_message, mo):
    data_status = mo.md(f"""
    ## Data Status

    {data_message}
    """)
    return (data_status,)


@app.cell
def _(df_final, mo):
    all_sectors = sorted(df_final["Sector_Key"].unique().tolist())

    sector_dropdown = mo.ui.multiselect(
        options=all_sectors,
        value=all_sectors,
        label="Filter by Sector",
    )

    max_cap = max(10, int(df_final["Market_Cap_B"].max()))

    cap_slider = mo.ui.slider(
        start=0,
        stop=max_cap,
        step=max(1, max_cap // 20),
        value=0,
        label="Minimum Market Cap ($ Billions)",
    )
    return cap_slider, sector_dropdown


@app.cell
def _(cap_slider, df_final, sector_dropdown):
    filtered_portfolio = df_final[
        (df_final["Sector_Key"].isin(sector_dropdown.value))
        & (df_final["Market_Cap_B"] >= cap_slider.value)
    ]

    count = len(filtered_portfolio)
    avg_cost = filtered_portfolio["Debt_Cost_Percent"].mean() if count > 0 else 0
    avg_z = filtered_portfolio["Z_Score_lag"].mean() if count > 0 else 0
    return avg_cost, avg_z, count, filtered_portfolio


@app.cell
def _(count, filtered_portfolio, px):
    fig_portfolio = px.scatter(
        filtered_portfolio,
        x="Z_Score_lag",
        y="Debt_Cost_Percent",
        color="Sector_Key",
        size="Market_Cap_B",
        hover_name="Name",
        hover_data=["Ticker", "Market_Cap_B"],
        title=f"Cost of Debt vs. Altman Z-Score ({count} observations)",
        labels={
            "Z_Score_lag": "Altman Z-Score (lagged)",
            "Debt_Cost_Percent": "Average Cost of Debt (%)",
            "Market_Cap_B": "Market Cap ($ Billions)",
        },
        template="plotly_white",
        width=950,
        height=620,
    )

    fig_portfolio.add_vline(
        x=1.81,
        line_dash="dash",
        line_color="red",
        annotation_text="Distress Threshold (1.81)",
    )

    fig_portfolio.add_vline(
        x=2.99,
        line_dash="dash",
        line_color="green",
        annotation_text="Safe Threshold (2.99)",
    )

    fig_portfolio.update_layout(title=dict(x=0, xanchor="left"))
    return (fig_portfolio,)


@app.cell
def _(mo):
    hero = mo.md("""
    # 👋 Ash Islam

    **BSc Accounting and Finance**

    Welcome to my professional portfolio webpage. This site brings together my academic interests, technical skills, and data-driven finance projects built using **Python, pandas, Plotly, and marimo**.

    ### Interests
    - Investment Banking
    - Finance
    - Data Analytics
    - Financial Visualisation
    - Gym & Fitness
    - Chess
    - Gaming
    """)
    return (hero,)


@app.cell
def _(mo):
    about_me = mo.md("""
    ## 👤 About Me

    I am an Accounting and Finance student with a strong interest in how data and technology can support financial analysis and decision-making. Through this portfolio, I showcase work that combines coding, data preparation, and interactive visualisation.

    I am especially interested in careers related to:
    - Investment banking
    - Financial analysis
    - Data-driven decision support

    This webpage reflects both technical learning and practical financial applications.
    """)
    return (about_me,)


@app.cell
def _(mo):
    projects = mo.md("""
    ## 📁 My Projects

    ### 1. Credit Risk Dashboard
    Built an interactive dashboard to analyse the relationship between a company’s **lagged Altman Z-Score** and its **average cost of debt**.

    ### 2. Data Preparation Pipeline
    Prepared panel data by handling missing values, creating lagged variables, engineering new metrics, and transforming raw financial data into a form suitable for analysis.

    ### 3. Interactive Visualisation
    Used Plotly to create finance-focused visualisations that allow users to explore relationships across companies and sectors through hovering, filtering, and dynamic chart interaction.
    """)
    return (projects,)


@app.cell
def _(mo):
    skills = mo.md("""
    ## 🛠 Skills

    ### Technical
    - Python
    - pandas
    - Plotly
    - marimo

    ### Data Skills
    - Data cleaning
    - Feature engineering
    - Lagged variable construction
    - Exploratory data analysis
    - Interactive dashboard design

    ### Finance Skills
    - Credit risk interpretation
    - Altman Z-Score analysis
    - Cost of debt analysis
    - Financial data storytelling
    """)
    return (skills,)


@app.cell
def _(mo):
    contact = mo.md("""
    ## 📬 Contact

    - **Email:** ash.islam@bayes.city.ac.uk
    """)
    return (contact,)


@app.cell
def _(avg_cost, avg_z, count, mo):
    highlights = mo.md(f"""
    ## 📊 Portfolio Highlights

    | Metric | Value |
    | :--- | :---: |
    | Companies Currently Displayed | **{count}** |
    | Avg. Cost of Debt | **{avg_cost:.2f}%** |
    | Avg. Lagged Z-Score | **{avg_z:.2f}** |

    These summary metrics update automatically based on the dashboard filters.
    """)
    return (highlights,)


@app.cell
def _(cap_slider, count, fig_portfolio, mo, sector_dropdown):
    dashboard_tab = mo.vstack([
        mo.md(f"""
    ## 📈 Interactive Finance Dashboard

    Use the controls below to explore how credit risk and borrowing costs vary across sectors and firms.

    **Current observations selected:** {count}
    """),
        sector_dropdown,
        cap_slider,
        mo.as_html(fig_portfolio),
    ])
    return (dashboard_tab,)


@app.cell
def _(
    about_me,
    contact,
    dashboard_tab,
    hero,
    highlights,
    mo,
    projects,
    skills,
):
    tabs = mo.ui.tabs({
        "Home": hero,
        "About Me": about_me,
        "Projects": projects,
        "Skills": skills,
        "Dashboard": dashboard_tab,
        "Highlights": highlights,
        "Contact": contact,
    })
    return (tabs,)


@app.cell
def _(data_status, mo, tabs, title):
    page = mo.vstack([
        title,
        data_status,
        tabs,
    ])
    return (page,)


@app.cell
def _(page):
    page
    return


if __name__ == "__main__":
    app.run()

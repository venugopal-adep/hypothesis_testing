import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy import stats

st.set_page_config(layout="wide", page_title="Mobile Internet Usage Analysis")

# Custom CSS for improved visual appeal and tooltips
st.markdown("""
<style>
    .main {
        padding: 2rem 3rem;
    }
    h1, h2, h3 {
        color: #1E90FF;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #F0F8FF;
        border-radius: 4px;
        color: #1E90FF;
        font-size: 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E90FF;
        color: white;
    }
    .stRadio [data-testid="stMarkdownContainer"] > p {
        font-size: 16px;
    }
    .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted black;
    }
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 300px;
        background-color: #555;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -150px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

# Function to create tooltips
def tooltip(text, code):
    return f"""
    <div class="tooltip">{text}
      <span class="tooltiptext">{code}</span>
    </div>
    """

st.title("Mobile Internet Usage Analysis")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Context", "📈 Analysis & Visualization", "🧮 Solved Examples", "🧠 Quiz"])

with tab1:
    st.header("Context")
    st.markdown("""
    ExperienceMyServices reported that a typical American spends an average of 144 minutes (2.4 hours) per day accessing the Internet via a mobile device with a standard deviation of 110 minutes.

    To test the validity of this statement, you collected 30 samples from friends and family. The results for the time spent per day accessing the Internet via a mobile device (in minutes) are stored in "InternetMobileTime.csv".

    ## Key Question:
    Is there enough statistical evidence to conclude that the population mean time spent per day accessing the Internet via mobile device is different from the hypothesized mean? Use the p-value approach and a level of significance of 0.05.

    **Note:** We can assume that the samples are randomly selected, independent, and come from a normally distributed population.
    """)

with tab2:
    st.header("Analysis & Visualization")
    
    # Load data
    @st.cache_data
    def load_data():
        return pd.read_csv('InternetMobileTime.csv')

    data = load_data()

    st.subheader("Data Preview")
    st.write(data.head())
    st.markdown(tooltip(f"Data shape: {data.shape}", "data.shape"), unsafe_allow_html=True)

    st.subheader("Hypothesis Testing")

    col1, col2 = st.columns([2, 1])

    with col1:
        hypothesized_mean = st.slider("Hypothesized mean (minutes)", min_value=60, max_value=240, value=144, step=1)

    with col2:
        alpha = st.number_input("Significance Level (α)", value=0.05, step=0.01, format="%.2f")

    # Calculations
    sample_mean = data["Minutes"].mean()
    sample_std = data["Minutes"].std()
    n = len(data)
    sigma = 110

    # Z-test
    z_stat = (sample_mean - hypothesized_mean) / (sigma / np.sqrt(n))
    p_value_z = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    # T-test
    t_stat, p_value_t = stats.ttest_1samp(data["Minutes"], popmean=hypothesized_mean)

    # Visualization
    confidence_level = 1 - alpha
    df = n - 1
    t_value = stats.t.ppf((1 + confidence_level) / 2, df)
    margin_of_error = t_value * (sample_std / np.sqrt(n))
    ci_lower = sample_mean - margin_of_error
    ci_upper = sample_mean + margin_of_error

    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=data["Minutes"],
        name="Sample Data",
        nbinsx=10,
        marker_color='lightblue'
    ))

    fig.add_vline(x=hypothesized_mean, line_dash="dash", line_color="green", 
                  annotation_text=f"Hypothesized Mean: {hypothesized_mean}",
                  annotation_position="top left")

    fig.add_vline(x=sample_mean, line_dash="dash", line_color="red", 
                  annotation_text=f"Sample Mean: {sample_mean:.2f}",
                  annotation_position="top right")

    fig.add_vrect(
        x0=ci_lower, x1=ci_upper,
        fillcolor="yellow", opacity=0.3, line_width=0,
        annotation_text=f"{confidence_level:.0%} CI: ({ci_lower:.2f}, {ci_upper:.2f})",
        annotation_position="bottom right"
    )

    fig.update_layout(
        title="Distribution of Internet Usage Time",
        xaxis_title="Minutes",
        yaxis_title="Frequency",
        showlegend=True,
        hovermode="x"
    )

    x_min = max(0, min(data["Minutes"].min(), hypothesized_mean, ci_lower) - 50)
    x_max = max(data["Minutes"].max(), hypothesized_mean, ci_upper) + 50
    fig.update_xaxes(range=[x_min, x_max])

    # Add custom hover text
    fig.update_traces(
        hovertemplate="<br>".join([
            "Minutes: %{x}",
            "Frequency: %{y}",
            "p-value %{customdata}",
            "%{text}"
        ])
    )

    # Create hover text based on x-coordinate
    hover_text = []
    custom_data = []
    for x in data["Minutes"]:
        if ci_lower <= x <= ci_upper:
            hover_text.append("Failed to reject H₀")
            custom_data.append("> alpha")
        else:
            hover_text.append("Reject H₀")
            custom_data.append("< alpha")

    fig.data[0].text = hover_text
    fig.data[0].customdata = custom_data

    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Z-test Results")
        st.markdown(tooltip(f"Z-statistic: {z_stat:.4f}", "z_stat = (sample_mean - hypothesized_mean) / (sigma / np.sqrt(n))"), unsafe_allow_html=True)
        st.markdown(tooltip(f"p-value: {p_value_z:.4f}", "p_value_z = 2 * (1 - stats.norm.cdf(abs(z_stat)))"), unsafe_allow_html=True)

    with col2:
        st.subheader("T-test Results")
        st.markdown(tooltip(f"T-statistic: {t_stat:.4f}", "t_stat, p_value_t = stats.ttest_1samp(data['Minutes'], popmean=hypothesized_mean)"), unsafe_allow_html=True)
        st.markdown(tooltip(f"p-value: {p_value_t:.4f}", "t_stat, p_value_t = stats.ttest_1samp(data['Minutes'], popmean=hypothesized_mean)"), unsafe_allow_html=True)

    decision_z = "Reject" if p_value_z < alpha else "Fail to reject"
    decision_t = "Reject" if p_value_t < alpha else "Fail to reject"

    st.subheader("Decision")
    st.markdown(tooltip(f"Z-test decision: {decision_z} the null hypothesis", 
                        "decision_z = 'Reject' if p_value_z < alpha else 'Fail to reject'"), 
                unsafe_allow_html=True)
    st.markdown(tooltip(f"T-test decision: {decision_t} the null hypothesis", 
                        "decision_t = 'Reject' if p_value_t < alpha else 'Fail to reject'"), 
                unsafe_allow_html=True)

    st.markdown(f"""
    ### Conclusion

    Based on the analysis:

    1. The Z-test (assuming known population standard deviation) yielded a p-value of {p_value_z:.4f}.
    2. The T-test (not assuming known population standard deviation) yielded a p-value of {p_value_t:.4f}.

    At a significance level of {alpha:.2f}, we {decision_t.lower()} the null hypothesis. 

    This means that there is {"" if decision_t == "Reject" else "not"} enough statistical evidence to conclude that the population mean time spent per day accessing the Internet via mobile device is different from {hypothesized_mean} minutes.
    """)

with tab3:
    st.header("Solved Numerical Examples")

    st.markdown("""
    ### Example 1: Calculating Z-statistic

    Given:
    - Sample mean (x̄) = 155 minutes
    - Hypothesized population mean (μ₀) = 144 minutes
    - Population standard deviation (σ) = 110 minutes
    - Sample size (n) = 30

    Calculate the Z-statistic:

    Z = (x̄ - μ₀) / (σ / √n)
    Z = (155 - 144) / (110 / √30)
    Z = 11 / 20.08
    Z ≈ 0.5478

    ### Example 2: Calculating p-value for two-tailed test

    Given:
    - Z-statistic = 0.5478

    Calculate the p-value:

    p-value = 2 * P(Z > |0.5478|)
    p-value = 2 * (1 - Φ(0.5478))
    p-value ≈ 0.5838

    Where Φ is the cumulative distribution function of the standard normal distribution.

    ### Example 3: Confidence Interval Calculation

    Given:
    - Sample mean (x̄) = 155 minutes
    - Sample standard deviation (s) = 105 minutes
    - Sample size (n) = 30
    - Confidence level = 95% (α = 0.05)

    Calculate the 95% confidence interval:

    1. Find t-value: t₀.₀₂₅,₂₉ ≈ 2.045 (using t-distribution table with df = 29)
    2. Calculate margin of error: ME = t * (s / √n) = 2.045 * (105 / √30) ≈ 39.23
    3. Confidence Interval: x̄ ± ME = 155 ± 39.23 = (115.77, 194.23)

    Therefore, we can be 95% confident that the true population mean falls between 115.77 and 194.23 minutes.
    """)

with tab4:
    st.header("Quiz")

    def check_answer(question, correct_answer, user_answer, explanation):
        if user_answer == correct_answer:
            st.success("Correct!")
            st.markdown(f"Explanation: {explanation}")
        else:
            st.error("Incorrect. Try again!")

    st.markdown("Test your understanding with these questions:")

    # Question 1
    st.subheader("Question 1")
    st.markdown("What is the null hypothesis in this study?")
    q1_options = ["μ = 144", "μ ≠ 144", "x̄ = 144", "x̄ ≠ 144"]
    q1_answer = st.radio("Select your answer:", q1_options, key="q1")
    if st.button("Submit Q1"):
        check_answer("Q1", q1_options[0], q1_answer,
                     "The null hypothesis states that the population mean (μ) is equal to the hypothesized value of 144 minutes.")

    # Question 2
    st.subheader("Question 2")
    st.markdown("What does a small p-value indicate?")
    q2_options = ["Strong evidence against H₀", "Strong evidence for H₀", "No evidence", "Inconclusive"]
    q2_answer = st.radio("Select your answer:", q2_options, key="q2")
    if st.button("Submit Q2"):
        check_answer("Q2", q2_options[0], q2_answer,
                     "A small p-value suggests that the observed data is unlikely under the null hypothesis, providing strong evidence against it.")

    # Question 3
    st.subheader("Question 3")
    st.markdown("What does the confidence interval represent?")
    q3_options = ["Range for μ", "Range for x̄", "Population SD", "Sample size"]
    q3_answer = st.radio("Select your answer:", q3_options, key="q3")
    if st.button("Submit Q3"):
        check_answer("Q3", q3_options[0], q3_answer,
                     "The confidence interval provides a range of plausible values for the population mean (μ) with a certain level of confidence.")

# Sidebar
st.sidebar.markdown("""
## Navigation
- [📊 Context](#context)
- [📈 Analysis & Visualization](#analysis-visualization)
- [🧮 Solved Examples](#solved-numerical-examples)
- [🧠 Quiz](#quiz)
""")

st.sidebar.info("This app performs hypothesis testing on mobile internet usage data.")

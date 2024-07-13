import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import norm, t, binom

st.set_page_config(layout="wide", page_title="Medicon Dose Analysis")

# CSS for tooltips and improved visual appeal
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

# Function to load data
@st.cache_data
def load_data():
    return pd.read_csv('doses.csv')

# Main title
st.title("Medicon Dose Testing Analysis")

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Context", "📈 Probability Distribution", "⏱️ Time of Effect Analysis", "🧮 Numerical Examples", "🧠 Quiz"])

with tab1:
    st.header("Context")
    st.write("""
    ## Context
    
    Medicon, a pharmaceutical company, has manufactured the sixth batch (40,000 units) of COVID-19 vaccine doses. 
    This vaccine was clinically tested last quarter and around 200,000 doses have already been given to people in five batches.

    Now, the sixth batch of doses needs to be tested for their **time of effect** and **quality assurance**.

    You are working with the quality assurance team of Medicon to understand the quality of the sixth batch.
    """)

with tab2:
    st.header("Probability Distribution of Unsatisfactory Doses")

    col1, col2 = st.columns(2)
    with col1:
        n = st.slider("Number of doses", 10, 1000, 100)
    with col2:
        p = st.slider("Probability of unsatisfactory dose", 0.01, 0.20, 0.09, 0.01)
    
    k = np.arange(0, n+1)
    binomial = binom.pmf(k=k, n=n, p=p)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=k, y=binomial, name='Binomial Distribution'))
    fig.update_layout(
        title=f'Binomial Distribution: n={n}, p={p:.2f}',
        xaxis_title='Number of Unsatisfactory Doses',
        yaxis_title='Probability',
        showlegend=False
    )

    col1, col2 = st.columns(2)
    with col1:
        shade_type = st.radio("Select shading type:", ["Exactly", "At most", "At least"])
    with col2:
        shade_value = st.slider(f"Number of doses to shade ({shade_type})", 0, n, 3)

    if shade_type == "Exactly":
        fig.add_trace(go.Bar(x=[shade_value], y=[binomial[shade_value]], marker_color='red', name='Shaded'))
        prob = binom.pmf(k=shade_value, n=n, p=p)
        st.markdown(tooltip(f"Probability of exactly {shade_value} unsatisfactory doses: {prob:.6f}", "prob = binom.pmf(k=shade_value, n=n, p=p)"), unsafe_allow_html=True)
    elif shade_type == "At most":
        fig.add_trace(go.Bar(x=k[:shade_value+1], y=binomial[:shade_value+1], marker_color='red', name='Shaded'))
        prob = binom.cdf(k=shade_value, n=n, p=p)
        st.markdown(tooltip(f"Probability of at most {shade_value} unsatisfactory doses: {prob:.6f}", "prob = binom.cdf(k=shade_value, n=n, p=p)"), unsafe_allow_html=True)
    else:  # "At least"
        fig.add_trace(go.Bar(x=k[shade_value:], y=binomial[shade_value:], marker_color='red', name='Shaded'))
        prob = 1 - binom.cdf(k=shade_value-1, n=n, p=p)
        st.markdown(tooltip(f"Probability of at least {shade_value} unsatisfactory doses: {prob:.6f}", "prob = 1 - binom.cdf(k=shade_value-1, n=n, p=p)"), unsafe_allow_html=True)

    st.plotly_chart(fig)

with tab3:
    st.header("Analysis of Time of Effect")

    drug = load_data()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Sample Data")
        st.write(drug.head())
    with col2:
        st.subheader("Summary Statistics")
        st.write(drug.describe())

    mu = drug['time_of_effect'].mean()
    sigma = drug['time_of_effect'].std()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(tooltip(f"Estimated mean: {mu:.2f}", "mu = drug['time_of_effect'].mean()"), unsafe_allow_html=True)
    with col2:
        st.markdown(tooltip(f"Estimated standard deviation: {sigma:.2f}", "sigma = drug['time_of_effect'].std()"), unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Histogram(x=drug['time_of_effect'], nbinsx=30, name='Time of Effect'))
    fig.add_trace(go.Scatter(x=drug['time_of_effect'], y=norm.pdf(drug['time_of_effect'], mu, sigma),
                             mode='lines', name='Normal Distribution'))
    fig.update_layout(title='Distribution of Time of Effect',
                      xaxis_title='Time (hours)',
                      yaxis_title='Frequency')
    st.plotly_chart(fig)

    col1, col2 = st.columns(2)
    with col1:
        threshold = st.slider("Time threshold (hours)", float(drug['time_of_effect'].min()), float(drug['time_of_effect'].max()), 11.5)
        prob = norm.cdf(threshold, mu, sigma)
        st.markdown(tooltip(f"Probability that time of effect is less than {threshold} hours: {prob:.4f}", "prob = norm.cdf(threshold, mu, sigma)"), unsafe_allow_html=True)
    with col2:
        percentile = st.slider("Percentile", 1, 99, 90)
        perc_value = norm.ppf(percentile/100, mu, sigma)
        st.markdown(tooltip(f"The {percentile}th percentile of time of effect: {perc_value:.2f} hours", "perc_value = norm.ppf(percentile/100, mu, sigma)"), unsafe_allow_html=True)

    st.subheader("Confidence Interval Estimation")
    confidence_level = st.slider("Confidence Level", 0.80, 0.99, 0.95, 0.01)
    n = len(drug)
    ci = t.interval(confidence_level, df=n-1, loc=mu, scale=sigma/np.sqrt(n))
    st.markdown(tooltip(f"{confidence_level*100:.0f}% Confidence Interval for mean time of effect: ({ci[0]:.2f}, {ci[1]:.2f})", "ci = t.interval(confidence_level, df=n-1, loc=mu, scale=sigma/np.sqrt(n))"), unsafe_allow_html=True)

with tab4:
    st.header("Numerical Examples")

    st.markdown("""
    ### Example 1: Calculating Probability of Unsatisfactory Doses

    Given:
    - Number of doses (n) = 100
    - Probability of unsatisfactory dose (p) = 0.09
    - We want exactly 3 unsatisfactory doses

    Calculate the probability:

    P(X = 3) = C(100,3) * 0.09³ * 0.91⁹⁷
    P(X = 3) ≈ 0.1235

    ### Example 2: Calculating Time of Effect Percentile

    Given:
    - Mean time of effect (μ) = 10.5 hours
    - Standard deviation (σ) = 2.1 hours
    - We want the 90th percentile

    Calculate the 90th percentile:

    X₉₀ = μ + Z₉₀ * σ
    X₉₀ = 10.5 + 1.28 * 2.1
    X₉₀ ≈ 13.19 hours

    ### Example 3: Confidence Interval Calculation

    Given:
    - Sample mean (x̄) = 10.5 hours
    - Sample standard deviation (s) = 2.1 hours
    - Sample size (n) = 100
    - Confidence level = 95% (α = 0.05)

    Calculate the 95% confidence interval:

    1. Find t-value: t₀.₀₂₅,₉₉ ≈ 1.984 (using t-distribution table with df = 99)
    2. Calculate margin of error: ME = t * (s / √n) = 1.984 * (2.1 / √100) ≈ 0.417
    3. Confidence Interval: x̄ ± ME = 10.5 ± 0.417 = (10.083, 10.917)

    Therefore, we can be 95% confident that the true population mean time of effect falls between 10.083 and 10.917 hours.
    """)

with tab5:
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
    st.markdown("What distribution is used to model the number of unsatisfactory doses?")
    q1_options = ["Binomial", "Normal", "Poisson", "Exponential"]
    q1_answer = st.radio("Select your answer:", q1_options, key="q1")
    if st.button("Submit Q1"):
        check_answer("Q1", q1_options[0], q1_answer,
                     "The Binomial distribution is used to model the number of successes (unsatisfactory doses) in a fixed number of independent trials.")

    # Question 2 (New)
    st.subheader("Question 2")
    st.markdown("What does 'time of effect' refer to in this analysis?")
    q2_options = ["Time for the vaccine to take effect", "Manufacturing time", "Expiration time", "Storage time"]
    q2_answer = st.radio("Select your answer:", q2_options, key="q2")
    if st.button("Submit Q2"):
        check_answer("Q2", q2_options[0], q2_answer,
                     "The 'time of effect' refers to the time it takes for the vaccine to become effective after administration.")

    # Question 3 (New)
    st.subheader("Question 3")
    st.markdown("Which measure of central tendency is used to estimate the average time of effect?")
    q3_options = ["Mean", "Median", "Mode", "Range"]
    q3_answer = st.radio("Select your answer:", q3_options, key="q3")
    if st.button("Submit Q3"):
        check_answer("Q3", q3_options[0], q3_answer,
                     "The mean (average) is used to estimate the central tendency of the time of effect for the vaccine doses.")




# Sidebar
st.sidebar.markdown("""
## Navigation
- [📊 Context](#context)
- [📈 Probability Distribution](#probability-distribution-of-unsatisfactory-doses)
- [⏱️ Time of Effect Analysis](#analysis-of-time-of-effect)
- [🧮 Numerical Examples](#numerical-examples)
- [🧠 Quiz](#quiz)
""")

st.sidebar.info("This app analyzes the quality and time of effect for Medicon's COVID-19 vaccine doses.")
st.sidebar.markdown("---")
st.sidebar.markdown("Created by [Your Name]")
st.sidebar.markdown("Data Source: Medicon Pharmaceutical Company")
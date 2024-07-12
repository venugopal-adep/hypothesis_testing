import streamlit as st
import plotly.graph_objects as go
import numpy as np
from scipy import stats

st.set_page_config(page_title="Hypothesis Testing Interactive Guide", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
.stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size: 24px;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab-list"] button {
    padding: 10px 20px;
    background-color: #f0f2f6;
    border-radius: 5px 5px 0 0;
}
.stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
    background-color: #4e8cff;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("Interactive Guide to Hypothesis Testing")

tab1, tab2, tab3, tab4 = st.tabs(["Key Terms", "Interactive Demo", "Solved Numerical", "Quiz"])

with tab1:
    st.header("Key Terms in Hypothesis Testing")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("P-Value")
        st.write("""
        • Probability of observing equal or more extreme results than the computed test statistic, under the null hypothesis.
        • The smaller the p-value, the stronger the evidence against the null hypothesis.
        """)
        
        st.subheader("Level of Significance")
        st.write("""
        • The significance level (denoted by α), is the probability of rejecting the null hypothesis when it is true.
        • It is a measure of the strength of the evidence that must be present in the sample data to reject the null hypothesis.
        """)
    
    with col2:
        st.subheader("Acceptance or Rejection Region")
        st.write("""
        • The total area under the distribution curve of the test statistic is partitioned into acceptance and rejection region.
        • Reject the null hypothesis when the test statistic lies in the rejection region, else we fail to reject it.
        """)
        
        st.subheader("Types of Error")
        st.write("""
        • There are two types of errors - Type I and Type II.
        • Type I Error: Rejecting a true null hypothesis (false positive)
        • Type II Error: Failing to reject a false null hypothesis (false negative)
        """)

with tab2:
    st.header("Interactive P-value Demonstration")

    col1, col2 = st.columns([1, 2])

    with col1:
        # User inputs
        mean = st.slider("Sample Mean", 0.0, 10.0, 5.0, 0.1)
        std_dev = st.slider("Standard Deviation", 0.1, 5.0, 1.0, 0.1)
        sample_size = st.slider("Sample Size", 10, 1000, 100)
        alpha = st.selectbox("Significance Level (α)", [0.01, 0.05, 0.1])

        # Calculate test statistic and p-value
        null_mean = 5.0
        t_stat = (mean - null_mean) / (std_dev / np.sqrt(sample_size))
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=sample_size-1))

        st.write(f"Test Statistic: {t_stat:.4f}")
        st.write(f"P-value: {p_value:.4f}")
        
        if p_value < alpha:
            st.success("Reject the null hypothesis")
        else:
            st.info("Fail to reject the null hypothesis")

    with col2:
        # Create the plot
        x = np.linspace(-4, 4, 1000)
        y = stats.t.pdf(x, df=sample_size-1)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='t-distribution'))
        
        # Shade rejection regions
        critical_value = stats.t.ppf(1 - alpha/2, df=sample_size-1)
        fig.add_trace(go.Scatter(x=np.concatenate([x[x <= -critical_value], [-critical_value]]),
                                 y=np.concatenate([y[x <= -critical_value], [0]]),
                                 fill='tozeroy', fillcolor='rgba(255,0,0,0.3)', line=dict(color='rgba(255,0,0,0.3)'),
                                 name='Rejection Region'))
        fig.add_trace(go.Scatter(x=np.concatenate([[critical_value], x[x >= critical_value]]),
                                 y=np.concatenate([[0], y[x >= critical_value]]),
                                 fill='tozeroy', fillcolor='rgba(255,0,0,0.3)', line=dict(color='rgba(255,0,0,0.3)'),
                                 name='Rejection Region'))

        # Add vertical line for test statistic
        fig.add_vline(x=t_stat, line_dash="dash", line_color="green", annotation_text="Test Statistic", annotation_position="top right")

        fig.update_layout(
            title='T-Distribution with Rejection Regions',
            xaxis_title='T-value',
            yaxis_title='Probability Density',
            height=400,  # Reduce the height of the plot
            margin=dict(l=0, r=0, t=30, b=0)  # Reduce margins
        )

        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Solved Numerical Example")
    st.write("""
    Problem: A company claims that their new energy drink increases reaction time by 20 milliseconds on average. 
    A study is conducted with 36 participants, resulting in a mean increase of 18 milliseconds and a standard deviation of 6 milliseconds. 
    Test this claim at a 5% significance level.
    
    Step 1: State the hypotheses
    - Null Hypothesis (H₀): μ = 20 ms (The true mean increase is 20 ms)
    - Alternative Hypothesis (H₁): μ ≠ 20 ms (The true mean increase is not 20 ms)
    
    Step 2: Calculate the test statistic
    t = (x̄ - μ₀) / (s / √n)
    where x̄ = 18, μ₀ = 20, s = 6, n = 36
    
    t = (18 - 20) / (6 / √36) = -2 / 1 = -2
    
    Step 3: Determine the critical value
    For a two-tailed test with α = 0.05 and df = 35, the critical value is ±2.030 (from t-distribution table)
    
    Step 4: Compare test statistic to critical value
    |-2| < 2.030, so we fail to reject the null hypothesis
    
    Step 5: Calculate p-value
    p-value = 2 * P(T ≤ -2) = 2 * 0.0262 = 0.0524
    
    Conclusion: Since p-value (0.0524) > α (0.05), we fail to reject the null hypothesis. 
    There is not enough evidence to conclude that the true mean increase in reaction time is different from 20 ms.
    """)

with tab4:
    st.header("Quiz")
    
    q1 = st.radio(
        "1. What does a small p-value indicate?",
        ("Strong evidence against the null hypothesis", "Strong evidence for the null hypothesis", "No evidence either way")
    )
    if q1 == "Strong evidence against the null hypothesis":
        st.success("Correct! A small p-value suggests that the observed data is unlikely under the null hypothesis, providing evidence against it.")
    elif q1:
        st.error("Incorrect. A small p-value actually indicates strong evidence against the null hypothesis.")
    
    q2 = st.radio(
        "2. What is the significance level (α) commonly used in hypothesis testing?",
        ("0.01", "0.05", "0.1", "0.5")
    )
    if q2 == "0.05":
        st.success("Correct! 0.05 or 5% is the most commonly used significance level in many fields.")
    elif q2:
        st.error("Incorrect. While other levels are sometimes used, 0.05 is the most common significance level.")
    
    q3 = st.radio(
        "3. What happens if the test statistic falls in the rejection region?",
        ("We fail to reject the null hypothesis", "We reject the null hypothesis", "We accept the alternative hypothesis")
    )
    if q3 == "We reject the null hypothesis":
        st.success("Correct! When the test statistic falls in the rejection region, we reject the null hypothesis.")
    elif q3:
        st.error("Incorrect. If the test statistic is in the rejection region, we reject the null hypothesis.")

    if st.button("Show Detailed Explanations"):
        st.write("""
        1. P-value: Think of the p-value as the probability of seeing your results (or more extreme) if the null hypothesis were true. 
           A small p-value means this probability is low, suggesting your results are unlikely under the null hypothesis. 
           For example, if you flip a coin 100 times and get 80 heads, the p-value would be very small because this outcome is very unlikely for a fair coin.

        2. Significance Level: The significance level is like setting a threshold for decision-making. 
           0.05 or 5% is commonly used because it balances the risk of false positives and false negatives. 
           It's like saying, "I'll only reject the null hypothesis if there's less than a 5% chance of seeing these results by random chance."

        3. Rejection Region: Imagine a dartboard where the bullseye represents the null hypothesis. 
           The rejection region is like the area outside the dartboard. If your dart (test statistic) lands outside the board (in the rejection region), 
           you conclude that you're not aiming at the center (reject the null hypothesis). 
           For example, in a z-test with α = 0.05, if your z-score is greater than 1.96 or less than -1.96, it falls in the rejection region.
        """)
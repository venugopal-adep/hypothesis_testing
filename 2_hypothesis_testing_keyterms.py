import streamlit as st
import numpy as np
from scipy import stats
import plotly.graph_objects as go

st.set_page_config(page_title="Hypothesis Testing Simplified", layout="wide")

st.title("🎓 Hypothesis Testing - Key Terms")
st.write("**Developed by : Venugopal Adep**")

tab1, tab2, tab3, tab4 = st.tabs(["📚 Key Terms", "🎮 Interactive Demo", "🧑‍⚖️ Real-World Example", "🧠 Quiz"])

with tab1:
    st.header("Key Terms in Hypothesis Testing - Explained Simply")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Null Hypothesis (H₀)")
        st.markdown("""
        <div style="background-color: #e6f3ff; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
        The initial assumption we're testing.
        
        🎲 Example: "This coin is fair" (50% chance of heads)
        
        It's what we assume to be true unless we find strong evidence otherwise.
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("Alternative Hypothesis (H₁)")
        st.markdown("""
        <div style="background-color: #e6f3ff; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
        What we're considering as an alternative to the null hypothesis.
        
        🎲 Example: "This coin is not fair" (chance of heads is not 50%)
        
        It's what we'll conclude if we reject the null hypothesis.
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("P-Value")
        st.markdown("""
        <div style="background-color: #e6f3ff; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
        The probability of getting our observed results (or more extreme) if the null hypothesis is true.
        
        🎲 Example: You flip a coin 100 times and get 60 heads. The p-value tells you how likely it is to get 60 or more heads with a fair coin.
        
        A small p-value (usually < 0.05) suggests strong evidence against the null hypothesis (i.e., the coin might not be fair).
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Significance Level (α)")
        st.markdown("""
        <div style="background-color: #e6f3ff; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
        The threshold for considering a result significant, usually set at 0.05 (5%).
        
        🎲 Example: If α = 0.05, you're saying: "I'll only believe the coin is unfair if there's less than a 5% chance of seeing these results with a fair coin."
        
        If p-value < α, we reject the null hypothesis (conclude the coin might be unfair).
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("Type I Error")
        st.markdown("""
        <div style="background-color: #e6f3ff; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
        Rejecting the null hypothesis when it's actually true (false positive).
        
        🎲 Example: Concluding the coin is unfair when it's actually fair.
        
        The probability of making this error is equal to the significance level (α).
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("Type II Error")
        st.markdown("""
        <div style="background-color: #e6f3ff; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
        Failing to reject the null hypothesis when it's actually false (false negative).
        
        🎲 Example: Concluding the coin is fair when it's actually unfair.
        
        The probability of avoiding this error is called the power of the test.
        </div>
        """, unsafe_allow_html=True)

    st.subheader("Why do we say 'Fail to Reject H₀' instead of 'Accept H₀'?")
    st.markdown("""
    <div style="background-color: #e6f3ff; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
    We use "fail to reject" because we're never 100% certain that the null hypothesis is true. 
    We're just saying we don't have enough evidence to reject it.

    🎲 Example: If we don't find strong evidence that a coin is unfair, we don't say it's definitely fair. 
    We just say we don't have enough evidence to conclude it's unfair. The coin could still be slightly biased, 
    but our test might not be powerful enough to detect it.
    </div>
    """, unsafe_allow_html=True)


with tab2:
    st.header("Interactive Coin Flip Demo")

    st.markdown("""
    <div style="background-color: #e6f3ff; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
    This interactive plot shows how changing your sample data affects the test results. 
    Play with the sliders to see how the results change!
    
    We're testing if a coin is fair (50% chance of heads) based on a series of flips.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        # User inputs
        num_flips = st.slider("Number of coin flips", 10, 1000, 100)
        num_heads = st.slider("Number of heads observed", 0, num_flips, num_flips // 2)
        alpha = st.selectbox("Significance Level (α)", [0.01, 0.05, 0.1])

        # Calculate p-value
        p_value = min(
            1 - stats.binom.cdf(num_heads - 1, num_flips, 0.5),
            stats.binom.cdf(num_heads, num_flips, 0.5)
        ) * 2  # Two-tailed test

        st.write(f"P-value: {p_value:.4f}")
        
        if p_value < alpha:
            st.error("Reject the null hypothesis")
        else:
            st.success("Fail to reject the null hypothesis")

    with col2:
        # Create the plot
        x = np.arange(0, num_flips + 1)
        y = stats.binom.pmf(x, num_flips, 0.5)

        fig = go.Figure()
        fig.add_trace(go.Bar(x=x, y=y, name='Probability'))

        # Add vertical line for observed number of heads
        fig.add_vline(x=num_heads, line_dash="dash", line_color="green", annotation_text="Observed Heads", annotation_position="top right")

        # Calculate critical values
        lower_critical = stats.binom.ppf(alpha/2, num_flips, 0.5)
        upper_critical = stats.binom.ppf(1-alpha/2, num_flips, 0.5)

        # Shade rejection regions
        fig.add_vrect(x0=0, x1=lower_critical, fillcolor="red", opacity=0.2, layer="below", line_width=0)
        fig.add_vrect(x1=num_flips, x0=upper_critical, fillcolor="red", opacity=0.2, layer="below", line_width=0)

        # Annotations
        fig.add_annotation(x=num_flips/4, y=max(y), text="Rejection Region", showarrow=False, yshift=10)
        fig.add_annotation(x=3*num_flips/4, y=max(y), text="Rejection Region", showarrow=False, yshift=10)
        fig.add_annotation(x=num_flips/2, y=max(y)/2, text="Acceptance Region", showarrow=False, yshift=10)
        fig.add_annotation(x=num_flips/2, y=max(y), text=f"Significance Level (α) = {alpha}", showarrow=False, yshift=30)
        fig.add_annotation(x=lower_critical, y=0, text="Coin is not fair", showarrow=False, yshift=-20)
        fig.add_annotation(x=upper_critical, y=0, text="Coin is not fair", showarrow=False, yshift=-20)
        fig.add_annotation(x=num_flips/2, y=0, text="Coin is fair", showarrow=False, yshift=-20)

        fig.update_layout(
            title='Binomial Distribution for Coin Flips',
            xaxis_title='Number of Heads',
            yaxis_title='Probability',
            height=500,
            margin=dict(l=0, r=0, t=30, b=0)
        )

        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Real-World Example: The Case of the Speeding Judge")

    st.markdown("""
    <div style="background-color: #e6f3ff; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
    Let's look at a real-world scenario to see how hypothesis testing works in practice.

    🚗 Scenario: A judge is accused of speeding. The speed limit is 65 mph, and the judge claims he wasn't speeding. 
    The police department has been tracking speeds on this road and knows that the average speed is normally distributed 
    with a standard deviation of 3 mph. They took 25 speed measurements of the judge's car.

    Null Hypothesis (H₀): The judge was not speeding (average speed ≤ 65 mph)
    Alternative Hypothesis (H₁): The judge was speeding (average speed > 65 mph)

    Let's say the 25 measurements had a mean of 66.2 mph. Is this enough evidence to conclude the judge was speeding?
    We'll use a significance level of 0.05 (5%).
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background-color: #e6f3ff; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
    Step 1: Calculate the test statistic (t-value)
    t = (x̄ - μ₀) / (s / √n)
    Where x̄ = 66.2, μ₀ = 65, s = 3, n = 25
    
    t = (66.2 - 65) / (3 / √25) = 2
    
    Step 2: Find the critical t-value
    For a one-tailed test with α = 0.05 and df = 24, the critical value is 1.711
    
    Step 3: Compare and conclude
    Since 2 > 1.711, we reject the null hypothesis.
    
    In simple terms: The evidence suggests the judge was indeed speeding! 
    The chance of seeing an average speed this high if the judge wasn't speeding is less than 5%.
    </div>
    """, unsafe_allow_html=True)

with tab4:
    st.header("Quick Quiz")
    
    st.markdown("""
    <div style="background-color: #f0f2f6; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
    <h3>1. What does a small p-value indicate?</h3>
    </div>
    """, unsafe_allow_html=True)
    q1 = st.radio("Select your answer:", 
        ("Strong evidence against the null hypothesis", "Strong evidence for the null hypothesis", "No evidence either way"),
        key="q1")
    if st.button("Check Answer", key="b1"):
        if q1 == "Strong evidence against the null hypothesis":
            st.success("Correct! A small p-value suggests that what we observed would be rare if the null hypothesis were true.")
        else:
            st.error("Not quite. Think about what a small probability means in terms of how likely your observation is under the null hypothesis.")
    
    st.markdown("""
    <div style="background-color: #f0f2f6; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
    <h3>2. What is the significance level (α) commonly used in hypothesis testing?</h3>
    </div>
    """, unsafe_allow_html=True)
    q2 = st.radio("Select your answer:", ("0.01", "0.05", "0.1", "0.5"), key="q2")
    if st.button("Check Answer", key="b2"):
        if q2 == "0.05":
            st.success("Correct! 0.05 or 5% is the most commonly used significance level in many fields.")
        else:
            st.error("Not quite. While other levels are sometimes used, there's one that's most common in practice.")
    
    st.markdown("""
    <div style="background-color: #f0f2f6; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
    <h3>3. What happens if the test statistic falls in the rejection region?</h3>
    </div>
    """, unsafe_allow_html=True)
    q3 = st.radio("Select your answer:", 
        ("We fail to reject the null hypothesis", "We reject the null hypothesis", "We accept the alternative hypothesis"),
        key="q3")
    if st.button("Check Answer", key="b3"):
        if q3 == "We reject the null hypothesis":
            st.success("Correct! When the test statistic falls in the rejection region, we reject the null hypothesis.")
        else:
            st.error("Not quite. Think about what it means when our evidence (test statistic) falls in an area we've designated for 'strong evidence against the null hypothesis'.")

st.markdown("---")

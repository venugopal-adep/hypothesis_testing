import streamlit as st
import plotly.graph_objects as go
import numpy as np
from scipy import stats

# Set page config
st.set_page_config(layout="wide", page_title="Type I and II Errors Explorer", page_icon="🎲")

# Custom CSS
st.markdown("""
<style>
    .main {max-width: 1200px; margin: 0 auto;}
    .stApp {padding-top: 1rem;}
    .st-emotion-cache-10trblm {text-align: center;}
    .info-box {background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 15px;}
    .quiz-container {background-color: #e1e5eb; padding: 15px; border-radius: 10px; margin-top: 15px;}
    .stTabs {background-color: #f9f9f9; padding: 10px; border-radius: 10px;}
    .plot-container {display: flex; justify-content: space-between;}
    .plot {width: 70%;}
    .sliders {width: 25%; padding-left: 20px;}
</style>
""", unsafe_allow_html=True)

# Title and introduction
st.title("🎲 Type I and II Errors Explorer")
st.markdown("Dive into the world of hypothesis testing errors with this interactive tool!")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["📚 Concept", "📊 Visualization", "🧮 Numericals", "🧠 Quiz"])

with tab1:
    st.header("Understanding Type I and II Errors")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Type I Error (False Positive) 🚨
        - Rejecting a true null hypothesis
        - Probability = α (significance level)
        - "Crying wolf" when there's no wolf
        """)
        
    with col2:
        st.markdown("""
        ### Type II Error (False Negative) 😴
        - Failing to reject a false null hypothesis
        - Probability = β
        - Missing the wolf when it's actually there
        """)
    
    st.markdown("""
    <div class="info-box">
    <h3>🔑 Key Concepts</h3>
    <ul>
        <li>α: The risk of false alarms</li>
        <li>β: The risk of missed detections</li>
        <li>Power (1 - β): The ability to spot real effects</li>
        <li>Tradeoff: Decreasing α often increases β</li>
        <li>Larger samples help reduce both error types</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)


with tab2:
    st.header("Interactive Visualization")
    
    col1, col2 = st.columns([0.7, 0.3])
    
    with col2:
        st.subheader("Adjust Parameters")
        mu0 = st.slider("Null Hypothesis Mean (μ₀)", 0.0, 5.0, 2.5, 0.1)
        mu1 = st.slider("Alternative Mean (μ₁)", 0.0, 5.0, 3.5, 0.1)
        sigma = st.slider("Standard Deviation (σ)", 0.1, 2.0, 1.0, 0.1)
        alpha = st.slider("Significance Level (α)", 0.01, 0.10, 0.05, 0.01)
    
    # Calculate critical value and probabilities
    z_crit = stats.norm.ppf(1 - alpha)
    x_crit = mu0 + z_crit * sigma
    
    x = np.linspace(0, 5, 1000)
    y0 = stats.norm.pdf(x, mu0, sigma)
    y1 = stats.norm.pdf(x, mu1, sigma)
    
    type1_prob = 1 - stats.norm.cdf(x_crit, mu0, sigma)
    type2_prob = stats.norm.cdf(x_crit, mu1, sigma)
    power = 1 - type2_prob
    
    # Create plot
    fig = go.Figure()
    
    # Null Hypothesis
    fig.add_trace(go.Scatter(x=x, y=y0, name="Null Hypothesis (H₀)", 
                             fill='tozeroy', fillcolor='rgba(0,176,246,0.2)',
                             line=dict(color='blue')))
    
    # Alternative Hypothesis
    fig.add_trace(go.Scatter(x=x, y=y1, name="Alternative Hypothesis (H₁)", 
                             fill='tozeroy', fillcolor='rgba(231,107,243,0.2)',
                             line=dict(color='purple')))
    
    # Critical value line
    fig.add_vline(x=x_crit, line_dash="dash", line_color="red", 
                  annotation=dict(text="Critical Value", textangle=-90, yshift=10))
    
    # Type I Error
    x_type1 = x[x >= x_crit]
    y_type1 = stats.norm.pdf(x_type1, mu0, sigma)
    fig.add_trace(go.Scatter(x=x_type1, y=y_type1, fill='tozeroy', 
                             fillcolor='rgba(255,0,0,0.3)', name='Type I Error (α)',
                             line=dict(color='red')))
    
    # Type II Error
    x_type2 = x[x <= x_crit]
    y_type2 = stats.norm.pdf(x_type2, mu1, sigma)
    fig.add_trace(go.Scatter(x=x_type2, y=y_type2, fill='tozeroy', 
                             fillcolor='rgba(0,255,0,0.3)', name='Type II Error (β)',
                             line=dict(color='green')))
    
    # Annotations
    fig.add_annotation(x=mu0, y=max(y0)/2, text="No Effect", showarrow=True, arrowhead=2, ax=0, ay=-40)
    fig.add_annotation(x=mu1, y=max(y1)/2, text="Treatment Effect", showarrow=True, arrowhead=2, ax=0, ay=-40)
    fig.add_annotation(x=(x_crit + 5)/2, y=max(y0)/4, text="Reject H₀", showarrow=False)
    fig.add_annotation(x=x_crit/2, y=max(y0)/4, text="Fail to Reject H₀", showarrow=False)
    
    fig.update_layout(
        title="Understanding Type I and Type II Errors",
        xaxis_title="Test Statistic (e.g., Treatment Effect)",
        yaxis_title="Probability Density",
        xaxis=dict(range=[0, 5]),
        legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=0),
        height=600,  # Increase the height of the plot
        annotations=[
            dict(x=0.5, y=1.05, xref="paper", yref="paper", text=f"Type I Error (α): {type1_prob:.2%}", showarrow=False),
            dict(x=0.5, y=1.10, xref="paper", yref="paper", text=f"Type II Error (β): {type2_prob:.2%}", showarrow=False),
            dict(x=0.5, y=1.15, xref="paper", yref="paper", text=f"Power (1-β): {power:.2%}", showarrow=False)
        ],
        margin=dict(t=150)  # Increase top margin to accommodate annotations
    )
    
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("How to Interpret This Plot")
    st.markdown("""
    Imagine we're testing a new medicine. Here's how to understand the plot:

    1. **Blue Curve (Null Hypothesis, H₀)**: This represents the distribution of results if the medicine has no effect.
       - Center: Average outcome without treatment
       - Spread: Natural variation in outcomes

    2. **Purple Curve (Alternative Hypothesis, H₁)**: This shows the distribution if the medicine does have an effect.
       - Shifted right: Indicates a positive effect
       - Overlap with blue: Difficulty in distinguishing effect from no effect

    3. **Red Line (Critical Value)**: Our decision threshold
       - Right of line: We conclude the medicine works
       - Left of line: We conclude no significant effect

    4. **Red Area (Type I Error, α)**: Chance of falsely claiming the medicine works
       - "False Positive" or "False Alarm"

    5. **Green Area (Type II Error, β)**: Chance of missing a real effect of the medicine
       - "False Negative" or "Missed Detection"

    6. **Test Statistic (X-axis)**: Measures the observed effect (e.g., improvement in patient condition)
       - Larger values suggest stronger treatment effect

    **Key Takeaways:**
    - Separation between curves: Easier to detect true effects
    - Overlap of curves: Risk of errors
    - Moving red line right: Reduces false positives, but may miss real effects
    - Moving red line left: Catches more real effects, but risks false positives

    **Try This:**
    1. Move the Alternative Mean slider. What happens to the purple curve and the errors?
    2. Adjust the Standard Deviation. How does this affect our ability to detect effects?
    3. Change the Significance Level. Watch how this moves the red line and affects errors.

    Remember: In real studies, we only see one sample, not the full distributions. This plot helps us understand the underlying challenges in making correct decisions from data!
    """)




with tab3:
    st.header("Solved Numericals")
    
    st.markdown("""
    ### Example 1: Medical Test
    A new medical test for a disease has the following characteristics:
    - Significance level (α) = 0.05
    - Power (1 - β) = 0.8
    
    Calculate:
    1. Probability of Type I error
    2. Probability of Type II error
    """)
    
    if st.button("Show Solution"):
        st.markdown("""
        **Solution:**
        1. Probability of Type I error = α = 0.05 (5%)
        2. Power = 1 - β = 0.8
           So, β = 1 - 0.8 = 0.2 (20%)
        
        Interpretation:
        - There's a 5% chance of falsely diagnosing a healthy person as sick (Type I error)
        - There's a 20% chance of missing the disease in a sick person (Type II error)
        - The test has an 80% chance of correctly identifying the disease when it's present
        """)

with tab4:
    st.header("Quiz Time!")
    
    st.markdown("""
    Test your understanding with these simple questions:
    """)
    
    q1 = st.radio(
        "1. What happens to Type II error when we decrease the significance level?",
        ["Decreases", "Increases", "Stays the same", "Becomes zero"]
    )
    
    if st.button("Check Answer"):
        if q1 == "Increases":
            st.success("Correct! 🎉")
            st.markdown("""
            **Explanation:**
            When we decrease the significance level (α), we make it harder to reject the null hypothesis. 
            This means we're less likely to make a Type I error (false positive), but more likely to make a Type II error (false negative).
            
            Think of it like a very strict judge. They're less likely to convict an innocent person (less Type I errors) 
            but more likely to let a guilty person go free (more Type II errors).
            
            Example: If we set a very low α of 0.01 for a medical test, we're less likely to tell healthy people they're sick, 
            but we might miss more cases of actually sick people.
            """)
        else:
            st.error("Not quite. Try again!")

    q2 = st.radio(
        "2. Which of the following will help reduce both Type I and Type II errors?",
        ["Increasing sample size", "Decreasing significance level", "Increasing standard deviation", "None of the above"]
    )

    if st.button("Check Answer", key="q2"):
        if q2 == "Increasing sample size":
            st.success("Correct! 🎉")
            st.markdown("""
            **Explanation:**
            Increasing the sample size helps reduce both Type I and Type II errors. 
            
            With a larger sample, we get more precise estimates of population parameters. This increased precision allows us to:
            1. More accurately reject the null hypothesis when it's false (reducing Type II errors)
            2. More accurately retain the null hypothesis when it's true (reducing Type I errors)

            Example: In a clinical trial, testing a new drug on 1000 patients instead of 100 gives us more reliable results, 
            reducing the chances of both falsely claiming the drug works and missing its actual effects.
            """)
        else:
            st.error("Not quite. Try again!")

    q3 = st.radio(
        "3. What is the power of a hypothesis test?",
        ["Probability of making a Type I error", "Probability of making a Type II error", 
         "Probability of correctly rejecting a false null hypothesis", "Significance level of the test"]
    )

    if st.button("Check Answer", key="q3"):
        if q3 == "Probability of correctly rejecting a false null hypothesis":
            st.success("Correct! 🎉")
            st.markdown("""
            **Explanation:**
            The power of a hypothesis test is the probability of correctly rejecting a false null hypothesis. It's calculated as 1 - β, where β is the probability of a Type II error.

            In simpler terms, power is the test's ability to detect a real effect when it exists.

            Example: If a test for a certain disease has 80% power, it means that if 100 people actually have the disease, 
            the test will correctly identify about 80 of them. The higher the power, the more reliable the test is at 
            detecting real effects.
            """)
        else:
            st.error("Not quite. Try again!")

# Footer
st.markdown("---")
st.markdown("© 2024 Type I and II Errors Explorer. Created with 💖 using Streamlit and Plotly.")
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from scipy import stats

st.set_page_config(layout="wide", page_title="One-tailed and Two-tailed Tests")

# Custom CSS for better styling
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .st-emotion-cache-16idsys p {
        font-size: 1.2rem;
    }
    h1, h2, h3 {
        color: #0066cc;
    }
    .highlight {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎯 One-tailed and Two-tailed Tests: Interactive Demo")

st.markdown("""
Welcome to this interactive demonstration of one-tailed and two-tailed hypothesis tests! 
We'll explore the differences between these types of tests and when to use each one.
""")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Introduction", "One-tailed Tests", "Two-tailed Tests", "Interactive Example", "Quiz"])

if page == "Introduction":
    st.header("📚 Introduction to One-tailed and Two-tailed Tests")
    
    st.markdown("""
    In hypothesis testing, we often need to decide between using a one-tailed or two-tailed test. 
    The choice depends on the nature of the research question, not on the sample data.

    Let's break down the key concepts:

    1. **Null Hypothesis (H₀)**: This is the default position, often stating that there's no effect or no difference.

    2. **Alternative Hypothesis (H₁ or Hₐ)**: This is what we're testing for, the possibility of an effect or difference.

    3. **One-tailed Test**: Used when we're only interested in an effect in one direction (greater than or less than).

    4. **Two-tailed Test**: Used when we're interested in an effect in either direction (not equal to).
    """)
    
    st.image("https://raw.githubusercontent.com/venugopal-adep/streamlit-demo/main/One-tailed%20and%20Two-tailed%20Tests.png", 
             caption="One-tailed and Two-tailed Tests")

elif page == "One-tailed Tests":
    st.header("👆 One-tailed Tests")
    
    st.markdown("""
    A one-tailed test is used when we're only interested in an effect in one specific direction. 
    There are two types of one-tailed tests:

    1. **Greater than type**: H₁: μ > μ₀
    2. **Less than type**: H₁: μ < μ₀

    Where μ is the population mean and μ₀ is the hypothesized value.
    """)

    st.subheader("When to use a one-tailed test")
    st.markdown("""
    Use a one-tailed test when:
    - You have a specific directional hypothesis
    - You're only interested in an effect in one direction
    - You want more statistical power to detect an effect in the direction of interest

    **Example**: A company introduces a new training program and wants to know if it increases employee productivity. 
    They're not interested in whether it might decrease productivity.

    H₀: μ ≤ μ₀ (The new program doesn't increase productivity)
    H₁: μ > μ₀ (The new program increases productivity)
    """)

    # Interactive visualization for one-tailed test
    st.subheader("Interactive One-tailed Test Visualization")
    tail = st.radio("Select the tail:", ["Right-tailed", "Left-tailed"])
    
    x = np.linspace(-4, 4, 1000)
    y = stats.norm.pdf(x, 0, 1)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Standard Normal Distribution'))
    
    if tail == "Right-tailed":
        critical_value = 1.645  # For α = 0.05
        fig.add_trace(go.Scatter(x=[critical_value, critical_value], y=[0, stats.norm.pdf(critical_value, 0, 1)], 
                                 mode='lines', name='Critical Value', line=dict(color='red', dash='dash')))
        fig.add_trace(go.Scatter(x=x[x>critical_value], y=y[x>critical_value], 
                                 fill='tozeroy', fillcolor='rgba(255,0,0,0.2)', line_color='rgba(255,0,0,0)', 
                                 name='Rejection Region'))
    else:
        critical_value = -1.645  # For α = 0.05
        fig.add_trace(go.Scatter(x=[critical_value, critical_value], y=[0, stats.norm.pdf(critical_value, 0, 1)], 
                                 mode='lines', name='Critical Value', line=dict(color='red', dash='dash')))
        fig.add_trace(go.Scatter(x=x[x<critical_value], y=y[x<critical_value], 
                                 fill='tozeroy', fillcolor='rgba(255,0,0,0.2)', line_color='rgba(255,0,0,0)', 
                                 name='Rejection Region'))

    fig.update_layout(title=f"{tail} Test",
                      xaxis_title="Z-score",
                      yaxis_title="Probability Density")
    
    st.plotly_chart(fig, use_container_width=True)

elif page == "Two-tailed Tests":
    st.header("👆👇 Two-tailed Tests")
    
    st.markdown("""
    A two-tailed test is used when we're interested in an effect in either direction. 
    The alternative hypothesis for a two-tailed test is:

    H₁: μ ≠ μ₀

    Where μ is the population mean and μ₀ is the hypothesized value.
    """)

    st.subheader("When to use a two-tailed test")
    st.markdown("""
    Use a two-tailed test when:
    - You don't have a specific directional hypothesis
    - You're interested in any deviation from the null hypothesis, regardless of direction
    - You want to be more conservative in your analysis

    **Example**: A researcher is studying the effect of a new drug on blood pressure. 
    They want to know if the drug changes blood pressure in either direction.

    H₀: μ = μ₀ (The drug doesn't affect blood pressure)
    H₁: μ ≠ μ₀ (The drug affects blood pressure, either increasing or decreasing it)
    """)

    # Interactive visualization for two-tailed test
    st.subheader("Interactive Two-tailed Test Visualization")
    
    x = np.linspace(-4, 4, 1000)
    y = stats.norm.pdf(x, 0, 1)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Standard Normal Distribution'))
    
    critical_value = 1.96  # For α = 0.05
    fig.add_trace(go.Scatter(x=[-critical_value, -critical_value], y=[0, stats.norm.pdf(critical_value, 0, 1)], 
                             mode='lines', name='Critical Values', line=dict(color='red', dash='dash')))
    fig.add_trace(go.Scatter(x=[critical_value, critical_value], y=[0, stats.norm.pdf(critical_value, 0, 1)], 
                             mode='lines', showlegend=False, line=dict(color='red', dash='dash')))
    fig.add_trace(go.Scatter(x=x[x<-critical_value], y=y[x<-critical_value], 
                             fill='tozeroy', fillcolor='rgba(255,0,0,0.2)', line_color='rgba(255,0,0,0)', 
                             name='Rejection Regions'))
    fig.add_trace(go.Scatter(x=x[x>critical_value], y=y[x>critical_value], 
                             fill='tozeroy', fillcolor='rgba(255,0,0,0.2)', line_color='rgba(255,0,0,0)', 
                             showlegend=False))

    fig.update_layout(title="Two-tailed Test",
                      xaxis_title="Z-score",
                      yaxis_title="Probability Density")
    
    st.plotly_chart(fig, use_container_width=True)

elif page == "Interactive Example":
    st.header("🧪 Interactive Example: Coffee and Productivity")

    st.markdown("""
    Let's explore an example of hypothesis testing using both one-tailed and two-tailed tests.

    **Scenario**: A company wants to investigate if drinking coffee affects employee productivity. 
    The average productivity score is 100 units per day.

    1. For a one-tailed test, we'll assume they're interested in whether coffee increases productivity.
    2. For a two-tailed test, we'll assume they're interested in any change in productivity.

    Let's say we collect data from 50 employees who drink coffee regularly.
    """)

    # User inputs
    sample_mean = st.number_input("Sample Mean Productivity", value=102.5, step=0.1)
    sample_size = st.number_input("Sample Size", value=50, min_value=30, step=1)
    pop_std = st.number_input("Population Standard Deviation", value=10.0, min_value=0.1, step=0.1)
    null_mean = 100  # The average productivity score

    # Calculate Z-score
    z_score = (sample_mean - null_mean) / (pop_std / np.sqrt(sample_size))

    # Calculate p-values
    p_value_one_tailed = 1 - stats.norm.cdf(z_score)
    p_value_two_tailed = 2 * (1 - stats.norm.cdf(abs(z_score)))

    st.markdown(f"""
    **Results:**
    - Z-score: {z_score:.4f}
    - One-tailed p-value: {p_value_one_tailed:.4f}
    - Two-tailed p-value: {p_value_two_tailed:.4f}
    """)

    # Plotting
    x = np.linspace(-4, 4, 1000)
    y = stats.norm.pdf(x, 0, 1)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Standard Normal Distribution'))
    fig.add_trace(go.Scatter(x=[z_score, z_score], y=[0, stats.norm.pdf(z_score, 0, 1)], 
                             mode='lines', name='Observed Z-score', line=dict(color='red', dash='dash')))

    # One-tailed test
    critical_value_one_tailed = stats.norm.ppf(0.95)  # For α = 0.05
    fig.add_trace(go.Scatter(x=[critical_value_one_tailed, critical_value_one_tailed], 
                             y=[0, stats.norm.pdf(critical_value_one_tailed, 0, 1)], 
                             mode='lines', name='One-tailed Critical Value', line=dict(color='green', dash='dash')))

    # Two-tailed test
    critical_value_two_tailed = stats.norm.ppf(0.975)  # For α = 0.05
    fig.add_trace(go.Scatter(x=[-critical_value_two_tailed, -critical_value_two_tailed], 
                             y=[0, stats.norm.pdf(critical_value_two_tailed, 0, 1)], 
                             mode='lines', name='Two-tailed Critical Values', line=dict(color='orange', dash='dash')))
    fig.add_trace(go.Scatter(x=[critical_value_two_tailed, critical_value_two_tailed], 
                             y=[0, stats.norm.pdf(critical_value_two_tailed, 0, 1)], 
                             mode='lines', showlegend=False, line=dict(color='orange', dash='dash')))

    fig.update_layout(title="One-tailed vs Two-tailed Test Visualization",
                      xaxis_title="Z-score",
                      yaxis_title="Probability Density")

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Interpretation:**
    - For the one-tailed test (H₁: μ > 100), we reject H₀ if the p-value < 0.05.
    - For the two-tailed test (H₁: μ ≠ 100), we reject H₀ if the p-value < 0.05.

    Notice how the one-tailed test is more likely to reject H₀ when the effect is in the hypothesized direction.
    """)

elif page == "Quiz":
    st.header("🧠 Test Your Knowledge")
    
    q1 = st.radio(
        "1. When should you use a one-tailed test?",
        ("When you have a large sample size",
         "When you're interested in effects in both directions",
         "When you have a specific directional hypothesis",
         "When your data is normally distributed")
    )
    
    if st.button("Check Answer"):
        if q1 == "When you have a specific directional hypothesis":
            st.markdown("""
            ✅ Correct! 
            
            You should use a one-tailed test when you have a specific directional hypothesis. This means you're only 
            interested in an effect in one direction (either greater than or less than the null hypothesis value).

            For example, if you're testing a new drug and you're only interested in whether it increases lifespan 
            (not if it might decrease it), you would use a one-tailed test.

            Remember:
            - One-tailed tests have more power to detect an effect in the specified direction.
            - However, they cannot detect effects in the opposite direction.
            - The choice between one-tailed and two-tailed tests should be made before collecting data, based on your research question.
            """)
        else:
            st.markdown("""
            ❌ Incorrect. 
            
            The correct answer is: "When you have a specific directional hypothesis"

            - Having a large sample size or normally distributed data doesn't determine whether you should use a one-tailed or two-tailed test.
            - If you're interested in effects in both directions, you should use a two-tailed test, not a one-tailed test.

            Remember, the choice between one-tailed and two-tailed tests depends on your research question and hypothesis, 
            not on the characteristics of your data.
            """)
    
    st.markdown("""
    ### Additional Resources
    
    To learn more about one-tailed and two-tailed tests:
    
    - [Khan Academy: One-tailed and two-tailed tests](https://www.khanacademy.org/math/statistics-probability/significance-tests-one-sample-t/more-significance-testing-videos/v/one-tailed-and-two-tailed-tests)
    - [StatTrek: Hypothesis Test: Difference Between Means](https://stattrek.com/hypothesis-test/difference-in-means.aspx)
    - [University of Michigan""")
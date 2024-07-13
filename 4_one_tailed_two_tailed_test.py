import streamlit as st
import plotly.graph_objects as go
import numpy as np
from scipy import stats

st.set_page_config(layout="wide", page_title="One-tailed and Two-tailed Tests", page_icon="🎯")

# Custom CSS for better styling
st.markdown("""
<style>
    body {
        color: #333;
        background-color: #f0f8ff;
    }
    .main > div {
        padding: 2rem;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #0066cc;
        color: white;
    }
    .st-emotion-cache-16idsys p {
        font-size: 1.1rem;
        line-height: 1.6;
    }
    h1, h2, h3 {
        color: #0066cc;
    }
    .highlight {
        background-color: #e6f3ff;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #0066cc;
    }
    .quiz-question {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .quiz-answer {
        margin-top: 1rem;
        padding: 1rem;
        background-color: #e6f3ff;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎯 One-tailed and Two-tailed Tests")
st.write("**Developed by : Venugopal Adep**")

st.markdown("""
Welcome to this exciting journey into the world of hypothesis testing! 
Get ready to explore the fascinating differences between one-tailed and two-tailed tests through interactive examples and quizzes.
""")

tabs = st.tabs(["📚 Introduction", "👆 One-tailed Tests", "👆👇 Two-tailed Tests", "🧪 Interactive Example", "🧮 Solved Numericals", "🧠 Quiz"])

with tabs[0]:
    st.header("📚 Introduction to One-tailed and Two-tailed Tests")
    
    st.markdown("""
    In the realm of hypothesis testing, choosing between a one-tailed and two-tailed test is crucial. 
    Let's break down these key concepts:
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🎯 One-tailed Test")
        st.markdown("""
        - Tests for an effect in one specific direction
        - More powerful for detecting a one-sided effect
        - Used when you have a directional hypothesis
        """)
    with col2:
        st.subheader("🎯🎯 Two-tailed Test")
        st.markdown("""
        - Tests for an effect in either direction
        - More conservative approach
        - Used when you're interested in any deviation from the null hypothesis
        """)

    st.image("https://raw.githubusercontent.com/venugopal-adep/streamlit-demo/main/One-tailed%20and%20Two-tailed%20Tests.png", 
             caption="Visual comparison of One-tailed and Two-tailed Tests")

with tabs[1]:
    st.header("👆 One-tailed Tests")
    
    st.markdown("""
    A one-tailed test is your go-to choice when you're specifically interested in an effect going in one direction. 
    It's like looking through a telescope pointed at a specific star!
    """)

    st.subheader("Types of One-tailed Tests")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Greater than type**: 
        - H₁: μ > μ₀
        - Looking for an increase
        """)
    with col2:
        st.markdown("""
        **Less than type**: 
        - H₁: μ < μ₀
        - Looking for a decrease
        """)

    st.subheader("When to use a one-tailed test")
    st.markdown("""
    Choose a one-tailed test when:
    - You have a specific directional hypothesis
    - You're only interested in an effect in one direction
    - You want more statistical power to detect an effect in the direction of interest
    """)

    st.markdown("""
    <div class="highlight">
    <strong>Example:</strong> A sports drink company claims their new formula increases endurance. 
    They're not interested in whether it might decrease endurance.

    H₀: μ ≤ μ₀ (The new formula doesn't increase endurance)
    H₁: μ > μ₀ (The new formula increases endurance)
    </div>
    """, unsafe_allow_html=True)

    # Interactive visualization for one-tailed test
    st.subheader("🔍 Interactive One-tailed Test Visualization")
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

with tabs[2]:
    st.header("👆👇 Two-tailed Tests")
    
    st.markdown("""
    A two-tailed test is like casting a wide net - you're interested in catching any significant difference, 
    regardless of direction. It's perfect when you want to know if there's any effect at all, positive or negative.
    """)

    st.subheader("Characteristics of Two-tailed Tests")
    st.markdown("""
    - Alternative hypothesis: H₁: μ ≠ μ₀
    - Looks for differences in both directions
    - More conservative than one-tailed tests
    - Suitable for exploratory research
    """)

    st.markdown("""
    <div class="highlight">
    <strong>Example:</strong> A researcher is studying the effect of a new meditation app on stress levels. 
    They want to know if the app changes stress levels in either direction.

    H₀: μ = μ₀ (The app doesn't affect stress levels)
    H₁: μ ≠ μ₀ (The app affects stress levels, either increasing or decreasing them)
    </div>
    """, unsafe_allow_html=True)

    # Interactive visualization for two-tailed test
    st.subheader("🔍 Interactive Two-tailed Test Visualization")
    
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

with tabs[3]:
    st.header("🧪 Interactive Example: Coffee and Productivity")

    st.markdown("""
    Let's dive into a real-world scenario to see how one-tailed and two-tailed tests work in practice!

    **Scenario**: A tech startup wants to investigate if their new 'power coffee' affects employee productivity. 
    The average productivity score in the industry is 100 units per day.

    1. For a one-tailed test, we'll assume they're interested in whether the coffee increases productivity.
    2. For a two-tailed test, we'll assume they're interested in any change in productivity.

    Let's collect data from employees who drink this new coffee regularly.
    """)

    # User inputs
    sample_mean = st.slider("Sample Mean Productivity", min_value=90.0, max_value=110.0, value=102.5, step=0.1)
    sample_size = st.slider("Sample Size", min_value=30, max_value=100, value=50, step=1)
    pop_std = st.slider("Population Standard Deviation", min_value=5.0, max_value=20.0, value=10.0, step=0.1)
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
    Play around with the sliders to see how changes in the sample affect the results!
    """)

with tabs[4]:
    st.header("🧮 Solved Numericals")


    st.markdown("""
    Step 1: Calculate the test statistic (t-score)
    t = (x̄ - μ₀) / (s / √n)
    t = (240 - 250) / (30 / √36) = -2

    Step 2: Find the critical value
    For a one-tailed test with α = 0.05 and df = 35, t_critical = -1.690

    Step 3: Compare the test statistic with the critical value
    -2 < -1.690, so we reject the null hypothesis.

    Conclusion: There is sufficient evidence to support the claim that the energy drink decreases reaction time.
    """)

    st.subheader("Example 2: Two-tailed Test")
    st.markdown("""
    A researcher wants to know if a new teaching method affects test scores. The average test score is 75. 
    They test the new method on 50 students and find a mean score of 78 with a standard deviation of 8.

    Let's test if there's a significant difference at a 5% significance level.

    Given:
    - H₀: μ = 75 (The new method doesn't affect test scores)
    - H₁: μ ≠ 75 (The new method affects test scores)

    Step 1: Calculate the test statistic (z-score)
    z = (x̄ - μ₀) / (σ / √n)
    z = (78 - 75) / (8 / √50) ≈ 2.65

    Step 2: Find the critical values
    For a two-tailed test with α = 0.05, z_critical = ±1.96

    Step 3: Compare the test statistic with the critical values
    2.65 > 1.96, so we reject the null hypothesis.

    Conclusion: There is sufficient evidence to conclude that the new teaching method affects test scores.
    """)

    st.markdown("""
    These examples demonstrate how to apply one-tailed and two-tailed tests in real-world scenarios. 
    Notice how the interpretation changes based on the type of test we're conducting!
    """)

with tabs[5]:
    st.header("🧠 Quiz: Test Your Knowledge")
    
    st.markdown("""
    Let's see how well you understand one-tailed and two-tailed tests! Answer these questions to test your knowledge.
    """)

    # Question 1
    st.subheader("Question 1")
    st.markdown("""
    <div class="quiz-question">
    A researcher is testing a new diet pill. They want to know if it leads to weight loss. 
    Which type of test should they use?

    a) One-tailed test
    b) Two-tailed test
    c) No test needed
    d) It depends on the sample size
    </div>
    """, unsafe_allow_html=True)

    q1_answer = st.radio("Select your answer for Question 1:", 
                         ["a) One-tailed test", "b) Two-tailed test", "c) No test needed", "d) It depends on the sample size"],
                         key="q1")

    if st.button("Check Answer", key="check_q1"):
        if q1_answer == "a) One-tailed test":
            st.markdown("""
            <div class="quiz-answer">
            ✅ Correct! 

            A one-tailed test is appropriate here because the researcher has a specific directional hypothesis. 
            They're only interested in whether the pill leads to weight loss (a decrease in weight), not if it might 
            cause weight gain.

            Example: If the average weight before the diet pill is 70 kg, our hypotheses would be:
            - H₀: μ ≥ 70 kg (The pill doesn't lead to weight loss)
            - H₁: μ < 70 kg (The pill leads to weight loss)

            This allows us to focus our statistical power on detecting the effect we're interested in - weight loss.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="quiz-answer">
            ❌ Incorrect. 

            The correct answer is a) One-tailed test.

            In this case, the researcher is only interested in whether the pill leads to weight loss. They're not 
            concerned about potential weight gain. This specific directional interest makes a one-tailed test 
            more appropriate.

            Remember, we use one-tailed tests when we have a specific directional hypothesis and are only interested 
            in an effect in one direction.
            </div>
            """, unsafe_allow_html=True)

    # Question 2
    st.subheader("Question 2")
    st.markdown("""
    <div class="quiz-question">
    A company is testing a new website design. They want to know if it affects the time users spend on the site, 
    regardless of whether it increases or decreases that time. Which type of test should they use?

    a) One-tailed test
    b) Two-tailed test
    c) No test needed
    d) It depends on the current average time spent on the site
    </div>
    """, unsafe_allow_html=True)

    q2_answer = st.radio("Select your answer for Question 2:", 
                         ["a) One-tailed test", "b) Two-tailed test", "c) No test needed", "d) It depends on the current average time spent on the site"],
                         key="q2")

    if st.button("Check Answer", key="check_q2"):
        if q2_answer == "b) Two-tailed test":
            st.markdown("""
            <div class="quiz-answer">
            ✅ Correct! 

            A two-tailed test is appropriate here because the company is interested in any change in time spent on the site, 
            whether it's an increase or a decrease.

            Example: If the current average time spent on the site is 5 minutes, our hypotheses would be:
            - H₀: μ = 5 minutes (The new design doesn't affect time spent on the site)
            - H₁: μ ≠ 5 minutes (The new design affects time spent on the site, either increasing or decreasing it)

            This allows us to detect any significant change in either direction, which aligns with the company's interest.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="quiz-answer">
            ❌ Incorrect. 

            The correct answer is b) Two-tailed test.

            In this scenario, the company wants to know if the new design affects the time spent on the site in either 
            direction. They're not just looking for an increase or just a decrease, but any significant change.

            Remember, we use two-tailed tests when we're interested in detecting effects in both directions, or when 
            we don't have a specific directional hypothesis.
            </div>
            """, unsafe_allow_html=True)

    # Question 3
    st.subheader("Question 3")
    st.markdown("""
    <div class="quiz-question">
    Which of the following statements is true about one-tailed tests?

    a) They are always more powerful than two-tailed tests
    b) They can detect effects in both directions
    c) They have more statistical power to detect an effect in the direction of interest
    d) They should be used when you have no specific hypothesis
    </div>
    """, unsafe_allow_html=True)

    q3_answer = st.radio("Select your answer for Question 3:", 
                         ["a) They are always more powerful than two-tailed tests", 
                          "b) They can detect effects in both directions", 
                          "c) They have more statistical power to detect an effect in the direction of interest", 
                          "d) They should be used when you have no specific hypothesis"],
                         key="q3")

    if st.button("Check Answer", key="check_q3"):
        if q3_answer == "c) They have more statistical power to detect an effect in the direction of interest":
            st.markdown("""
            <div class="quiz-answer">
            ✅ Correct! 

            One-tailed tests do indeed have more statistical power to detect an effect in the direction of interest.

            Example: Let's say we're testing if a new fertilizer increases plant growth. The average growth without 
            the fertilizer is 10 cm.

            - For a one-tailed test (H₁: μ > 10 cm), we might reject H₀ if the sample mean is 11.5 cm.
            - For a two-tailed test (H₁: μ ≠ 10 cm), we might need the sample mean to be 12 cm to reject H₀.

            This shows how the one-tailed test can detect smaller effects in the direction of interest. However, 
            remember that this comes at the cost of not being able to detect effects in the opposite direction.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="quiz-answer">
            ❌ Incorrect. 

            The correct answer is c) They have more statistical power to detect an effect in the direction of interest.

            Let's break down why the other options are incorrect:

            a) While one-tailed tests are more powerful in one direction, they're not always more powerful overall.
            b) One-tailed tests can only detect effects in one direction, not both.
            d) One-tailed tests should be used when you have a specific directional hypothesis, not when you have no hypothesis.

            Remember, the increased power of one-tailed tests in the direction of interest comes at the cost of not 
            being able to detect effects in the opposite direction. Always choose your test based on your research 
            question and hypothesis!
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    Great job on completing the quiz! Remember, understanding when to use one-tailed vs. two-tailed tests is crucial 
    in statistical analysis. Keep practicing with real-world scenarios to reinforce your knowledge.
    """)

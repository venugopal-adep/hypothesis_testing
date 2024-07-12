import streamlit as st
import plotly.graph_objects as go
import numpy as np
from scipy import stats

st.set_page_config(page_title="Hypothesis Testing Simplified", layout="wide")

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
.info-box {
    background-color: #e6f3ff;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
}
.quiz-question {
    background-color: #f0f2f6;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("🎓 Hypothesis Testing Simplified")

tab1, tab2, tab3, tab4 = st.tabs(["📚 Key Terms", "🎮 Interactive Demo", "🧑‍⚖️ Real-World Example", "🧠 Quiz"])

with tab1:
    st.header("Key Terms in Hypothesis Testing - Explained Simply")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("P-Value")
        st.markdown("""
        <div class="info-box">
        Think of the p-value as the probability of a fluke result. It's like asking:
        "If nothing special is happening, how likely are we to see results like this?"
        
        🎲 Example: Imagine you're testing a "lucky" coin. You flip it 100 times and get 60 heads.
        The p-value tells you how likely it is to get 60 or more heads with a fair coin.
        A small p-value (like 0.01) means it's very unlikely - your coin might actually be biased!
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("Significance Level (α)")
        st.markdown("""
        <div class="info-box">
        This is like setting the bar for what counts as "surprising enough" to reject your initial assumption.
        
        🎯 Example: If you set α to 0.05 (5%), you're saying:
        "I'll only believe something unusual is happening if there's less than a 5% chance of seeing these results by random chance."
        It's like only being surprised by a 1-in-20 or rarer event.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Acceptance or Rejection Region")
        st.markdown("""
        <div class="info-box">
        Imagine a dartboard where the bullseye is your initial guess (null hypothesis).
        The rejection region is like the area outside the dartboard.
        
        🎯 Example: If your dart (test result) lands on the board, you stick with your initial guess.
        If it lands off the board (in the rejection region), you think, "Hmm, maybe my initial guess was wrong."
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("Types of Errors")
        st.markdown("""
        <div class="info-box">
        • Type I Error: Crying wolf (false alarm)
          You conclude something special is happening when it's actually just chance.
          
        • Type II Error: Missing the real deal
          You fail to notice when something genuinely unusual is occurring.
        
        ⚖️ Example: In a court case, Type I is convicting an innocent person, 
        while Type II is letting a guilty person go free.
        </div>
        """, unsafe_allow_html=True)

    st.subheader("Why do we say 'Fail to Reject H₀' instead of 'Accept H₀'?")
    st.markdown("""
    <div class="info-box">
    We use "fail to reject" because we're never 100% certain that the null hypothesis is true. 
    We're just saying we don't have enough evidence to reject it.

    🕵️ Think of it like a detective who doesn't have enough evidence to arrest a suspect. 
    They're not saying the suspect is innocent, just that they can't prove guilt beyond reasonable doubt.
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.header("Interactive T-Distribution Demo")

    st.markdown("""
    <div class="info-box">
    This interactive plot shows how changing your sample data affects the test results. 
    Play with the sliders to see how the t-statistic and p-value change!
    
    The t-distribution is used when we don't know the population standard deviation, which is often the case in real-world scenarios.
    </div>
    """, unsafe_allow_html=True)

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

        st.write(f"T-Statistic: {t_stat:.4f}")
        st.write(f"P-value: {p_value:.4f}")
        
        if p_value < alpha:
            st.error("Reject the null hypothesis")
        else:
            st.success("Fail to reject the null hypothesis")

        st.markdown("""
        <div class="info-box">
        <h4>Impact of Parameters:</h4>
        • Sample Mean: Shifts the t-statistic. Further from null hypothesis = stronger evidence against it.<br>
        • Standard Deviation: Affects spread. Larger SD = less certainty, wider distribution.<br>
        • Sample Size: Larger size = narrower distribution, more certainty.<br>
        • Significance Level: Sets the threshold for rejection. Lower α = stricter test.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box">
        <h4>Formulas:</h4>
        • T-Statistic: t = (x̄ - μ₀) / (s / √n)<br>
        Where x̄ = sample mean, μ₀ = null hypothesis mean, s = sample standard deviation, n = sample size<br>
        • P-value: 2 * P(T > |t|) where T follows t-distribution with (n-1) degrees of freedom
        </div>
        """, unsafe_allow_html=True)

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

        # Annotations
        fig.add_annotation(x=-critical_value, y=0.1, text="Rejection Region", showarrow=False, yshift=10)
        fig.add_annotation(x=critical_value, y=0.1, text="Rejection Region", showarrow=False, yshift=10)
        fig.add_annotation(x=0, y=0.2, text="Acceptance Region", showarrow=False, yshift=10)

        fig.update_layout(
            title='T-Distribution with Rejection Regions',
            xaxis_title='T-value',
            yaxis_title='Probability Density',
            height=500,
            margin=dict(l=0, r=0, t=30, b=0)
        )

        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Real-World Example: The Case of the Speeding Judge")

    st.markdown("""
    <div class="info-box">
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
    <div class="info-box">
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
    <div class="quiz-question">
    <h3>1. What does a small p-value indicate?</h3>
    </div>
    """, unsafe_allow_html=True)
    q1 = st.radio("Select your answer:", 
        ("Strong evidence against the null hypothesis", "Strong evidence for the null hypothesis", "No evidence either way"),
        key="q1")
    if st.button("Check Answer", key="b1"):
        if q1 == "Strong evidence against the null hypothesis":
            st.success("Correct! A small p-value suggests that what we observed would be rare if the null hypothesis were true.")
            st.markdown("""
            <div class="info-box">
            Imagine you're flipping a coin and get 9 heads out of 10 flips. If the coin is fair (null hypothesis), 
            this outcome is quite rare. The p-value tells you just how rare. A small p-value means "Wow, this almost never 
            happens with a fair coin!" - which makes you doubt that the coin is actually fair.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Not quite. Think about what a small probability means in terms of how likely your observation is under the null hypothesis.")
    
    st.markdown("""
    <div class="quiz-question">
    <h3>2. What is the significance level (α) commonly used in hypothesis testing?</h3>
    </div>
    """, unsafe_allow_html=True)
    q2 = st.radio("Select your answer:", ("0.01", "0.05", "0.1", "0.5"), key="q2")
    if st.button("Check Answer", key="b2"):
        if q2 == "0.05":
            st.success("Correct! 0.05 or 5% is the most commonly used significance level in many fields.")
            st.markdown("""
            <div class="info-box">
            Think of 0.05 as a balance between being too strict and too lenient. It's like saying, "I'll only cry wolf 
            if there's less than a 1 in 20 chance that what I'm seeing is just random chance." It's strict enough to 
            avoid too many false alarms, but not so strict that we miss important effects.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Not quite. While other levels are sometimes used, there's one that's most common in practice.")
    
    st.markdown("""
    <div class="quiz-question">
    <h3>3. What happens if the test statistic falls in the rejection region?</h3>
    </div>
    """, unsafe_allow_html=True)
    q3 = st.radio("Select your answer:", 
        ("We fail to reject the null hypothesis", "We reject the null hypothesis", "We accept the alternative hypothesis"),
        key="q3")
    if st.button("Check Answer", key="b3"):
        if q3 == "We reject the null hypothesis":
            st.success("Correct! When the test statistic falls in the rejection region, we reject the null hypothesis.")
            st.markdown("""
            <div class="info-box">
            Imagine you're a detective, and the rejection region is like finding strong evidence at a crime scene. 
            If your test statistic (evidence) falls in this region, it's like saying, "This evidence is too strong to ignore. 
            We can't stick with our initial assumption of innocence." In statistical terms, we're saying the data is too 
            unlikely under the null hypothesis, so we reject it.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Not quite. Think about what it means when our evidence (test statistic) falls in an area we've designated for 'strong evidence against the null hypothesis'.")

st.markdown("---")

import streamlit as st
import numpy as np
from scipy import stats
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="Store Checkout Time Analysis", layout="wide")

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
    h1, h2, h3 {
        color: #0066cc;
    }
    .highlight {
        background-color: #e6f3ff;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #0066cc;
        margin-bottom: 1rem;
    }
    .example {
        background-color: #f0fff0;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #00cc66;
        margin-bottom: 1rem;
    }
    .quiz-question {
        background-color: #fff0f5;
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
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🛒 Hypothesis Example : Store Checkout Time Analysis")
st.write("**Developed by : Venugopal Adep**")

st.markdown("""
Welcome to our interactive exploration of store checkout times! We'll use some fancy statistical tools to figure out 
if customers are waiting too long in line. Don't worry if you're not a math whiz - we'll explain everything in simple terms!
""")

# Create tabs
tabs = st.tabs(["📝 Problem", "🔬 Hypothesis", "🧪 Test It!", "⚠️ Possible Errors", "🧠 Quiz Time"])

with tabs[0]:
    st.header("📝 The Problem: Long Lines at Checkout")
    
    st.markdown("""
    <div class="highlight">
    Imagine you're the manager of a busy supermarket. Lately, you've been getting complaints about long waiting times 
    at the checkout. You've always aimed to keep the average wait under 15 minutes, but you're worried it might have 
    crept up above that.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="example">
    <strong>Real-world example:</strong> Think of the last time you were in a long checkout line. Maybe you were 
    getting fidgety, checking your watch, or even considering abandoning your cart. As a store manager, you definitely 
    don't want that happening to your customers!
    </div>
    """, unsafe_allow_html=True)

with tabs[1]:
    st.header("🔬 Our Hypothesis: What Are We Testing?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="highlight">
        <h3>Null Hypothesis (H₀):</h3>
        The average waiting time is still 15 minutes or less.
        
        In math-speak: H₀: μ ≤ 15 minutes
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        Think of this as the "everything is fine" hypothesis. It's like saying, "Nothing to see here, folks! 
        Wait times are still within our 15-minute goal."
        """)
    
    with col2:
        st.markdown("""
        <div class="highlight">
        <h3>Alternative Hypothesis (Hₐ):</h3>
        The average waiting time has increased to more than 15 minutes.
        
        In math-speak: Hₐ: μ > 15 minutes
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        This is our "Houston, we have a problem" hypothesis. It's suggesting that wait times have indeed 
        gotten worse and are now exceeding our 15-minute target.
        """)

    st.markdown("""
    <div class="example">
    <strong>Everyday example:</strong> It's like suspecting your teenager is staying up past their bedtime. 
    Your null hypothesis might be "They're in bed by 10 PM as agreed" (H₀), while your alternative hypothesis 
    is "They're staying up later than 10 PM" (Hₐ). You'd need evidence to reject your null hypothesis and 
    conclude they're indeed staying up late!
    </div>
    """, unsafe_allow_html=True)

with tabs[2]:
    st.header("🧪 Let's Test It!")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        Adjust these values to see how different scenarios play out:
        """)
        sample_mean = st.number_input("Average Wait Time (min)", min_value=10.0, max_value=20.0, value=16.0, step=0.1)
        sample_size = st.number_input("Number of Customers", min_value=30, max_value=500, value=100, step=10)
        population_std = st.number_input("Wait Time Variation (min)", min_value=1.0, max_value=5.0, value=3.0, step=0.1)
        alpha = st.selectbox("Confidence Level", options=[0.90, 0.95, 0.99], index=1, 
                             format_func=lambda x: f"{x:.0%}")
    
    with col2:
        # Calculate test statistic and p-value
        null_mean = 15
        z_stat = (sample_mean - null_mean) / (population_std / np.sqrt(sample_size))
        p_value = 1 - stats.norm.cdf(z_stat)

        # Visualization
        x = np.linspace(-4, 4, 1000)
        y = stats.norm.pdf(x, 0, 1)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Normal Distribution'))

        critical_value = stats.norm.ppf(1 - (1-alpha))
        fig.add_trace(go.Scatter(x=[critical_value, critical_value], y=[0, stats.norm.pdf(critical_value, 0, 1)], 
                                 mode='lines', name='Critical Value', line=dict(color='red', dash='dash')))

        # Add rejection region
        x_fill = x[x > critical_value]
        y_fill = y[x > critical_value]
        fig.add_trace(go.Scatter(x=x_fill, y=y_fill, fill='tozeroy', fillcolor='rgba(255,0,0,0.2)', 
                                 line_color='rgba(255,0,0,0)', name='Rejection Region'))

        # Add test statistic line
        fig.add_trace(go.Scatter(x=[z_stat, z_stat], y=[0, stats.norm.pdf(z_stat, 0, 1)], 
                                 mode='lines', name='Test Statistic', 
                                 line=dict(color='lime', width=3)))

        # Add annotation for test statistic
        fig.add_annotation(x=z_stat, y=stats.norm.pdf(z_stat, 0, 1) / 2,
                           text="Test Statistic",
                           showarrow=True,
                           arrowhead=2,
                           arrowsize=1,
                           arrowwidth=2,
                           arrowcolor="lime")

        fig.update_layout(title="Our Hypothesis Test Visualized",
                          xaxis_title="Standard Deviations from the Mean",
                          yaxis_title="Probability",
                          height=400)

        st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    **Test Results:**
    - Test statistic: {z_stat:.2f}
    - P-value: {p_value:.4f}
    - Critical value: {critical_value:.2f}

    **Conclusion:** We {"reject" if p_value < 1-alpha else "fail to reject"} the null hypothesis.

    <div class="highlight">
    In everyday language: There {"is" if p_value < 1-alpha else "isn't"} strong evidence to suggest that the average 
    waiting time at checkouts has become worse than 15 minutes. 
    {"You might want to open more checkout lanes!" if p_value < 1-alpha else "Things seem to be running smoothly!"}
    </div>
    """, unsafe_allow_html=True)

with tabs[3]:
    st.header("⚠️ When Things Go Wrong: Possible Errors")
    
    st.markdown("""
    Even with careful testing, we can sometimes make mistakes. In statistics, we have names for these mistakes:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="highlight">
        <h3>Type I Error (False Alarm)</h3>
        We conclude wait times are over 15 minutes when they're actually not.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        This is like pulling the fire alarm when there's no fire. We might waste resources opening 
        more checkout lanes when we didn't really need to.
        """)
    
    with col2:
        st.markdown("""
        <div class="highlight">
        <h3>Type II Error (Missed Problem)</h3>
        We conclude wait times are fine when they're actually over 15 minutes.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        This is like ignoring the smoke alarm because we think it's just burnt toast. We might let a 
        real problem with long wait times go unaddressed.
        """)

    st.markdown("""
    <div class="example">
    <strong>Real-life example:</strong> Imagine you're a doctor testing for a disease. A Type I error would be 
    telling a healthy patient they're sick (false positive). A Type II error would be telling a sick patient 
    they're healthy (false negative). Both can have serious consequences!
    </div>
    """, unsafe_allow_html=True)

with tabs[4]:
    st.header("🧠 Quiz Time!")
    
    questions = [
        {
            "question": "In our checkout time scenario, what does the null hypothesis (H₀) suggest?",
            "options": [
                "The average waiting time is exactly 15 minutes",
                "The average waiting time is more than 15 minutes",
                "The average waiting time is 15 minutes or less",
                "The average waiting time is not 15 minutes"
            ],
            "correct": 2,
            "explanation": """
            The null hypothesis suggests that the average waiting time is 15 minutes or less. This is correct because:

            1. In hypothesis testing, the null hypothesis typically represents the status quo or the current assumption.
            2. In this scenario, we're testing if the waiting time has become worse (increased beyond 15 minutes).
            3. Therefore, the null hypothesis assumes that the waiting time hasn't increased beyond our target of 15 minutes.

            Think of it like this: If you're checking if a bus is late, your null hypothesis might be "The bus 
            is on time or early." You'd need strong evidence to conclude it's actually late.
            """
        },
        {
            "question": "What does a Type I error represent in our checkout time scenario?",
            "options": [
                "Concluding wait times are fine when they're actually over 15 minutes",
                "Concluding wait times are over 15 minutes when they're actually fine",
                "Always concluding wait times are over 15 minutes",
                "Never concluding wait times are over 15 minutes"
            ],
            "correct": 1,
            "explanation": """
            A Type I error occurs when we reject the null hypothesis when it's actually true. In our scenario, this means:

            1. We conclude that wait times are over 15 minutes (rejecting the null hypothesis)
            2. But in reality, wait times are 15 minutes or less (the null hypothesis was true)

            This is like a "false alarm". We think there's a problem when there actually isn't one.

            Real-world example: It's like a smoke detector going off because of steam from a shower, not actual smoke. 
            You react as if there's a fire (reject the null hypothesis of "no fire") when there isn't one (null hypothesis is true).
            """
        },
        {
            "question": "If we decrease our significance level (α) from 0.05 to 0.01, what happens?",
            "options": [
                "We become more likely to commit a Type I error",
                "We become less likely to commit a Type I error",
                "We become more likely to commit a Type II error",
                "Both b and c"
            ],
            "correct": 3,
            "explanation": """
            Decreasing the significance level from 0.05 to 0.01 results in both b and c:

            1. We become less likely to commit a Type I error:
               - The significance level (α) is the probability of committing a Type I error.
               - By decreasing α, we're directly decreasing the chance of a Type I error.

            2. We become more likely to commit a Type II error:
               - As we make it harder to reject the null hypothesis (by lowering α), we increase the chance of 
                 failing to reject it when we should (Type II error).

            Real-world example: Imagine you're a judge setting the standard for "guilty beyond reasonable doubt." 
            If you raise this standard (like lowering α):
            - You're less likely to convict an innocent person (less Type I error)
            - But you're more likely to let a guilty person go free (more Type II error)

            This illustrates the constant trade-off between Type I and Type II errors in hypothesis testing.
            """
        }
    ]

    for i, q in enumerate(questions):
        st.markdown(f"""
        <div class="quiz-question">
        <h3>Question {i+1}:</h3>
        <p>{q['question']}</p>
        </div>
        """, unsafe_allow_html=True)

        answer = st.radio(f"Your answer for Question {i+1}:", q['options'], key=f"q{i+1}")

        if st.button(f"Check Answer", key=f"check_q{i+1}"):
            if q['options'].index(answer) == q['correct']:
                st.markdown(f"""
                <div class="quiz-answer">
                ✅ Correct! 

                {q['explanation']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="quiz-answer">
                ❌ Not quite. 

                The correct answer is: {q['options'][q['correct']]}

                {q['explanation']}
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")

st.markdown("---")
st.markdown("© 2024 Store Checkout Time Analysis. Developed by Venugopal Adep.")
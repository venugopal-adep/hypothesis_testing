import streamlit as st
import plotly.graph_objects as go
import numpy as np
from scipy import stats

# Set page config
st.set_page_config(page_title="Introduction to Hypothesis Testing", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
    body {
        color: #333;
        background-color: #f0f2f6;
    }
    .main > div {
        padding: 1rem;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    h1, h2, h3 {
        color: #1e88e5;
    }
    .highlight {
        background-color: #e3f2fd;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 5px solid #1e88e5;
    }
    .stButton>button {
        background-color: #1e88e5;
        color: white;
    }
    .stSelectbox {
        color: #1e88e5;
    }
    .small-font {
        font-size: 0.9rem;
    }
    .result-box {
        background-color: #f1f8e9;
        border-radius: 5px;
        padding: 1rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🔬 Introduction to Hypothesis Testing")
st.write ('**Developed by : Venugopal Adep**')

# Custom z-test function
def proportions_ztest(count, nobs, value=None, alternative='two-sided', prop_var=False):
    count = np.asarray(count)
    nobs = np.asarray(nobs)
    
    prop = count / nobs
    value = 0 if value is None else value

    p_pool = np.sum(count) / np.sum(nobs)
    var = p_pool * (1 - p_pool) * np.sum(1/nobs)
    
    z_stat = (prop[0] - prop[1] - value) / np.sqrt(var)
    
    if alternative == 'two-sided':
        p_value = 2 * (1 - stats.norm.cdf(np.abs(z_stat)))
    elif alternative == 'larger':
        p_value = 1 - stats.norm.cdf(z_stat)
    elif alternative == 'smaller':
        p_value = stats.norm.cdf(z_stat)
    else:
        raise ValueError('alternative must be "two-sided", "larger" or "smaller"')

    return z_stat, p_value

# Tabs
tab1, tab2, tab3 = st.tabs(["📚 Basics", "🧪 Interactive Example", "🧠 Quiz"])

with tab1:
    st.header("📚 Hypothesis Testing Basics")
    
    st.subheader("What is Hypothesis Testing?")
    st.markdown("""
    Imagine you're a detective trying to solve a mystery. You have a hunch (hypothesis), and you need to gather evidence (data) to see if your hunch is right. That's hypothesis testing in a nutshell!
    """)
    
    st.subheader("Key Terms")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        1. **Null Hypothesis (H₀)**: Your initial assumption. Like saying "nothing special is happening."
        2. **Alternative Hypothesis (Hₐ)**: The claim you're testing. The "something interesting is happening" idea.
        """)
    with col2:
        st.markdown("""
        3. **p-value**: A measure of how surprising your results are if H₀ is true.
        4. **Significance Level (α)**: The threshold for deciding when to reject H₀. Usually 0.05.
        """)
    
    st.subheader("Steps in Hypothesis Testing")
    st.markdown("""
    1. 🤔 State your hypotheses (H₀ and Hₐ)
    2. 📏 Choose a significance level (usually 0.05)
    3. 📊 Collect data and calculate test statistic
    4. 🧮 Find the p-value
    5. 🏆 Make a decision: reject H₀ if p-value < significance level
    """)

with tab2:
    st.header("🧪 Interactive Example: New Ad Campaign")
    
    st.markdown("""
    Let's play the role of a marketing analyst! We're testing if a new ad increases our online store's sales.
    Adjust the sliders below to see how different scenarios affect our decision.
    """)
    
    col1, col2 = st.columns([1,3])
    
    with col1:
        st.markdown('<p class="small-font">Adjust parameters:</p>', unsafe_allow_html=True)
        old_rate = st.slider("Old Ad Conversion (%)", min_value=1.0, max_value=10.0, value=5.0, step=0.1)
        new_rate = st.slider("New Ad Conversion (%)", min_value=1.0, max_value=10.0, value=5.5, step=0.1)
        sample_size = st.slider("Sample Size", min_value=100, max_value=10000, value=1000, step=100)
        alpha = st.selectbox("Significance Level (α)", options=[0.01, 0.05, 0.1], index=1)
    
    # Calculate test statistic and p-value
    old_successes = int(old_rate / 100 * sample_size)
    new_successes = int(new_rate / 100 * sample_size)
    
    z_stat, p_value = proportions_ztest([new_successes, old_successes], [sample_size, sample_size], 
                                        alternative='larger')
    
    # Visualization
    x = np.linspace(-4, 4, 1000)
    y = stats.norm.pdf(x, 0, 1)
    
    fig = go.Figure()
    
    # Add shaded rejection region
    critical_value = stats.norm.ppf(1 - alpha)
    x_fill = np.linspace(critical_value, 4, 100)
    y_fill = stats.norm.pdf(x_fill, 0, 1)
    fig.add_trace(go.Scatter(x=x_fill, y=y_fill, fill='tozeroy', fillcolor='rgba(255,0,0,0.2)', line_color='rgba(255,0,0,0)',
                             name='Rejection Region'))

    # Add normal distribution curve
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Normal Distribution', line=dict(color='#1e88e5')))
    
    # Add critical value line
    fig.add_trace(go.Scatter(x=[critical_value, critical_value], y=[0, stats.norm.pdf(critical_value, 0, 1)], 
                             mode='lines', name='Critical Value', line=dict(color='red', dash='dash')))
    
    # Add test statistic line
    fig.add_trace(go.Scatter(x=[z_stat, z_stat], y=[0, stats.norm.pdf(z_stat, 0, 1)], 
                             mode='lines', name='Test Statistic', line=dict(color='green', dash='dash')))
    
    fig.update_layout(title="Hypothesis Test Visualization",
                      xaxis_title="Z-score",
                      yaxis_title="Probability Density",
                      plot_bgcolor='rgba(0,0,0,0)',
                      height=400,
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    
    with col2:
        st.plotly_chart(fig, use_container_width=True)
    
    # Results
    st.subheader("📊 Test Results")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        🔢 **Test Statistics:**
        - Z-statistic: {z_stat:.4f}
        - Critical value: {critical_value:.4f}
        - P-value: {p_value:.4f}
        """)
    with col2:
        st.markdown(f"""
        🎯 **Decision Rules:**
        - Reject H₀ if Z-statistic > Critical value
        - Reject H₀ if P-value < α (Significance level)
        """)
    
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    if z_stat > critical_value and p_value < alpha:
        st.success(f"""
        **Conclusion:** We reject the null hypothesis!
        - Z-statistic ({z_stat:.4f}) > Critical value ({critical_value:.4f})
        - P-value ({p_value:.4f}) < α ({alpha})
        
        There's strong evidence that the new ad is better.
        """)
    elif z_stat > critical_value or p_value < alpha:
        st.warning(f"""
        **Conclusion:** Conflicting results
        - Z-statistic ({z_stat:.4f}) {'>' if z_stat > critical_value else '<='} Critical value ({critical_value:.4f})
        - P-value ({p_value:.4f}) {'<' if p_value < alpha else '>='} α ({alpha})
        
        This is unusual and might indicate a need for further investigation.
        """)
    else:
        st.info(f"""
        **Conclusion:** We fail to reject the null hypothesis.
        - Z-statistic ({z_stat:.4f}) <= Critical value ({critical_value:.4f})
        - P-value ({p_value:.4f}) >= α ({alpha})
        
        We don't have enough evidence to say the new ad is better.
        """)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.header("🧠 Quiz Time!")
    
    st.markdown("Test your newfound knowledge with this quick quiz!")
    
    q1 = st.radio(
        "1. In our ad campaign example, what was the null hypothesis?",
        ["a) The new ad is better than the old ad",
         "b) The new ad is worse than the old ad",
         "c) There's no difference between the new and old ad",
         "d) We need more data to decide"]
    )
    
    if st.button("Check Answer", key="check_q1"):
        if q1 == "c) There's no difference between the new and old ad":
            st.success("🎉 Correct! The null hypothesis assumes no effect or no difference.")
        else:
            st.error("Not quite. Remember, the null hypothesis typically assumes no effect or no difference.")
    
    q2 = st.radio(
        "2. If our p-value is 0.03 and our significance level (α) is 0.05, what do we conclude?",
        ["a) We fail to reject the null hypothesis",
         "b) We reject the null hypothesis",
         "c) We need more data",
         "d) The test is inconclusive"]
    )
    
    if st.button("Check Answer", key="check_q2"):
        if q2 == "b) We reject the null hypothesis":
            st.success("🎉 Correct! Since 0.03 < 0.05, we reject the null hypothesis.")
        else:
            st.error("Not quite. Remember, we reject the null hypothesis when the p-value is less than our significance level.")

    q3 = st.radio(
        "3. What does a larger sample size generally do to your hypothesis test?",
        ["a) It always leads to rejecting the null hypothesis",
         "b) It makes the test less reliable",
         "c) It increases the power of the test",
         "d) It has no effect on the test"]
    )
    
    if st.button("Check Answer", key="check_q3"):
        if q3 == "c) It increases the power of the test":
            st.success("🎉 Correct! A larger sample size generally increases the power of the test, making it more likely to detect a real effect if one exists.")
        else:
            st.error("Not quite. A larger sample size generally increases the power of the test, making it more likely to detect a real effect if one exists.")

st.markdown("---")
st.markdown("© 2024 Introduction to Hypothesis Testing. Developed by Venugopal Adep.")
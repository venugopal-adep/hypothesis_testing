import streamlit as st
import plotly.graph_objects as go
import numpy as np
from scipy import stats

st.set_page_config(layout="wide", page_title="Statistical Inference Explorer", page_icon="🎯")

# Custom CSS for improved styling
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stApp {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
    }
    .plot-container {
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
        padding: 1rem;
        background-color: white;
    }
    .info-box {
        background-color: #e6f3ff;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .solved-example {
        background-color: #e6ffe6;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    .quiz-question {
        background-color: #fff0e6;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎯 Statistical Inference Explorer")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Interactive Plot", "🧮 Solved Examples", "🧠 Quiz", "📚 Learn More"])

with tab1:
    st.header("Confidence Intervals vs Hypothesis Testing")

    st.markdown("""
    <div class="info-box">
        <h3>Key Concepts:</h3>
        <ol>
            <li>A 95% confidence interval contains all values of μ₀ for which the null hypothesis will not be rejected at a 5% significance level.</li>
            <li>The confidence interval and hypothesis test are complementary approaches to statistical inference.</li>
            <li>If μ₀ is within the confidence interval, we fail to reject H₀. If it's outside, we reject H₀.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col2:
        st.subheader("📐 Sample Parameters")
        sample_mean = st.number_input("Sample Mean", value=10.0, step=0.1)
        sample_std = st.number_input("Sample Standard Deviation", value=2.0, min_value=0.1, step=0.1)
        sample_size = st.number_input("Sample Size", value=30, min_value=2, step=1)
        confidence_level = st.slider("Confidence Level", min_value=0.8, max_value=0.99, value=0.95, step=0.01)
        null_hypothesis = st.number_input("Null Hypothesis (μ₀)", value=sample_mean, step=0.1)

    # Calculate confidence interval
    def calculate_ci(mean, std, n, conf_level):
        se = std / np.sqrt(n)
        z_score = stats.norm.ppf((1 + conf_level) / 2)
        margin_of_error = z_score * se
        lower_bound = mean - margin_of_error
        upper_bound = mean + margin_of_error
        return lower_bound, upper_bound

    lower, upper = calculate_ci(sample_mean, sample_std, sample_size, confidence_level)

    # Plotting function
    def plot_ci_and_hypothesis(mean, std, n, lower, upper, null_hypothesis):
        # Set fixed x-axis range
        x_min = 0  # You can adjust this value as needed
        x_max = 20  # You can adjust this value as needed
        
        x = np.linspace(x_min, x_max, 1000)
        y = stats.norm.pdf(x, mean, std/np.sqrt(n))
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Sampling Distribution', line=dict(color='blue')))
        fig.add_vrect(x0=lower, x1=upper, fillcolor="rgba(0,100,80,0.2)", layer="below", line_width=0,
                      annotation_text="Confidence Interval", annotation_position="top left")
        fig.add_vline(x=mean, line_dash="dash", line_color="green", annotation_text="Sample Mean")
        fig.add_vline(x=null_hypothesis, line_dash="dash", line_color="red", annotation_text="Null Hypothesis")
        
        fig.update_layout(title='Confidence Interval and Hypothesis Test Visualization',
                          xaxis_title='Population Mean', yaxis_title='Probability Density',
                          showlegend=False, 
                          xaxis=dict(range=[x_min, x_max]),  # Set fixed x-axis range
                          yaxis=dict(range=[0, stats.norm.pdf(mean, mean, std/np.sqrt(n)) * 1.1]))  # Set y-axis range
        return fig

    with col1:
        st.plotly_chart(plot_ci_and_hypothesis(sample_mean, sample_std, sample_size, lower, upper, null_hypothesis), use_container_width=True)

    st.subheader("🧮 Calculations")
    st.markdown(f"""
    <div class="info-box">
        <h4>Confidence Interval:</h4>
        CI = x̄ ± (z * (s / √n))
        <br>Where:
        <ul>
            <li>x̄ = sample mean = {sample_mean:.2f}</li>
            <li>s = sample standard deviation = {sample_std:.2f}</li>
            <li>n = sample size = {sample_size}</li>
            <li>z = z-score for {confidence_level:.0%} confidence = {stats.norm.ppf((1 + confidence_level) / 2):.3f}</li>
        </ul>
        <strong>Result: ({lower:.3f}, {upper:.3f})</strong>
    </div>
    
    <div class="info-box">
        <h4>Hypothesis Test:</h4>
        H₀: μ = {null_hypothesis:.2f}
        <br>H₁: μ ≠ {null_hypothesis:.2f}
        <br>
        <strong>Result: {
            "Fail to reject H₀" if lower <= null_hypothesis <= upper 
            else "Reject H₀"
        }</strong>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.header("Solved Examples")
    
    st.markdown("""
    <div class="solved-example">
    <h3>Example 1: Confidence Interval for Mean Weight Loss</h3>
    <p><strong>Problem:</strong> A nutritionist is testing a new diet plan. In a sample of 36 participants, the mean weight loss was 4.2 kg with a standard deviation of 1.8 kg. Calculate a 95% confidence interval for the mean weight loss in the population.</p>
    <p><strong>Solution:</strong></p>
    <ol>
        <li>Sample mean (x̄) = 4.2 kg</li>
        <li>Sample standard deviation (s) = 1.8 kg</li>
        <li>Sample size (n) = 36</li>
        <li>For 95% confidence, z-score = 1.96</li>
        <li>Standard error (SE) = s / √n = 1.8 / √36 = 0.3</li>
        <li>Margin of error = z * SE = 1.96 * 0.3 = 0.588</li>
        <li>Confidence Interval = x̄ ± margin of error = 4.2 ± 0.588</li>
    </ol>
    <p>Therefore, the 95% confidence interval is (3.612 kg, 4.788 kg).</p>
    <p>Interpretation: We can be 95% confident that the true population mean weight loss falls between 3.612 kg and 4.788 kg.</p>
    </div>
    
    <div class="solved-example">
    <h3>Example 2: Hypothesis Test for Mean Weight Loss</h3>
    <p><strong>Problem:</strong> Using the same data as Example 1, test the hypothesis that the mean weight loss is different from 3.5 kg at a 5% significance level.</p>
    <p><strong>Solution:</strong></p>
    <ol>
        <li>Null Hypothesis (H₀): μ = 3.5 kg</li>
        <li>Alternative Hypothesis (H₁): μ ≠ 3.5 kg</li>
        <li>We already calculated the 95% CI: (3.612 kg, 4.788 kg)</li>
        <li>The null hypothesis value (3.5 kg) is outside this interval</li>
    </ol>
    <p>Since 3.5 kg is outside the 95% confidence interval, we reject the null hypothesis at a 5% significance level.</p>
    <p>Conclusion: There is sufficient evidence to conclude that the true mean weight loss is different from 3.5 kg.</p>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.header("Quiz Time!")
    
    questions = [
        {
            "question": "What does a 95% confidence interval mean?",
            "options": ["95% of the data falls within this range", "We are 95% certain the true parameter is in this range", "95% of samples will contain the true parameter"],
            "correct": "95% of samples will contain the true parameter",
            "explanation": """A 95% confidence interval means that if we were to repeat our sampling process many times and 
            calculate the interval each time, about 95% of these intervals would contain the true population parameter. 
            It's like a fishing net: if we cast our net (calculate the interval) 100 times, about 95 of those casts would 
            catch the true parameter. For example, if we calculate a 95% CI for average weight loss to be (3.5 kg, 4.5 kg), 
            it means that if we repeated this study many times, about 95% of the calculated intervals would contain the 
            true population mean weight loss."""
        },
        {
            "question": "If the null hypothesis value falls outside the confidence interval, what do we conclude?",
            "options": ["Fail to reject H₀", "Reject H₀", "Not enough information"],
            "correct": "Reject H₀",
            "explanation": """When the null hypothesis value falls outside the confidence interval, we reject H₀. 
            This is because the confidence interval contains all plausible values for the population parameter 
            that are consistent with the sample data. If the null hypothesis value is not in this interval, 
            it's considered unlikely to be the true population parameter. For instance, if our 95% CI for mean 
            weight loss is (3.5 kg, 4.5 kg) and our null hypothesis is that the mean weight loss is 3 kg, 
            we would reject this hypothesis because 3 kg is not within our interval of plausible values."""
        },
        {
            "question": "How does increasing sample size generally affect the width of a confidence interval?",
            "options": ["Widens it", "Narrows it", "Has no effect"],
            "correct": "Narrows it",
            "explanation": """Increasing the sample size generally narrows the confidence interval. This is because a larger sample 
            size provides more information about the population, reducing uncertainty. Think of it like taking more measurements 
            to get a more precise estimate. For example, if we increase our sample of weight loss measurements from 30 people to 
            300 people, our confidence interval might narrow from (3.5 kg, 4.5 kg) to (3.8 kg, 4.2 kg), giving us a more precise 
            estimate of the true average weight loss."""
        }
    ]

    for i, q in enumerate(questions):
        st.markdown(f"""
        <div class="quiz-question">
        <h3>Question {i+1}</h3>
        <p>{q["question"]}</p>
        </div>
        """, unsafe_allow_html=True)
        response = st.radio(f"Select your answer for Question {i+1}:", q["options"], key=f"q{i}")
        if st.button(f"Check Answer {i+1}"):
            if response == q["correct"]:
                st.success("🎉 Correct!")
            else:
                st.error("❌ Incorrect. Try again!")
            st.info(f"Explanation: {q['explanation']}")
        st.markdown("---")

with tab4:
    st.header("Learn More")
    st.markdown("""
    Want to dive deeper into statistical inference? Check out these resources:
    
    1. [Khan Academy: Confidence Intervals](https://www.khanacademy.org/math/statistics-probability/confidence-intervals-one-sample)
    2. [StatQuest: Hypothesis Testing and p-values](https://www.youtube.com/watch?v=vemZtEM63GY)
    3. [Statistics How To: Confidence Intervals vs Hypothesis Tests](https://www.statisticshowto.com/probability-and-statistics/hypothesis-testing/confidence-interval-hypothesis-testing/)
    4. [OpenIntro Statistics (free teximport streamlit as st
import plotly.graph_objects as go
import numpy as np
from scipy import stats

st.set_page_config(layout="wide", page_title="Statistical Inference Explorer", page_icon="🎯")

# Custom CSS for improved styling
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stApp {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
    }
    .plot-container {
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
        padding: 1rem;
        background-color: white;
    }
    .info-box {
        background-color: #e6f3ff;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .solved-example {
        background-color: #e6ffe6;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    .quiz-question {
        background-color: #fff0e6;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎯 Statistical Inference Explorer")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Interactive Plot", "🧮 Solved Examples", "🧠 Quiz", "📚 Learn More"])

with tab1:
    st.header("Confidence Intervals vs Hypothesis Testing")

    st.markdown("""
    <div class="info-box">
        <h3>Key Concepts:</h3>
        <ol>
            <li>A 95% confidence interval contains all values of μ₀ for which the null hypothesis will not be rejected at a 5% significance level.</li>
            <li>The confidence interval and hypothesis test are complementary approaches to statistical inference.</li>
            <li>If μ₀ is within the confidence interval, we fail to reject H₀. If it's outside, we reject H₀.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col2:
        st.subheader("📐 Sample Parameters")
        sample_mean = st.number_input("Sample Mean", value=10.0, step=0.1)
        sample_std = st.number_input("Sample Standard Deviation", value=2.0, min_value=0.1, step=0.1)
        sample_size = st.number_input("Sample Size", value=30, min_value=2, step=1)
        confidence_level = st.slider("Confidence Level", min_value=0.8, max_value=0.99, value=0.95, step=0.01)
        null_hypothesis = st.number_input("Null Hypothesis (μ₀)", value=sample_mean, step=0.1)

    # Calculate confidence interval
    def calculate_ci(mean, std, n, conf_level):
        se = std / np.sqrt(n)
        z_score = stats.norm.ppf((1 + conf_level) / 2)
        margin_of_error = z_score * se
        lower_bound = mean - margin_of_error
        upper_bound = mean + margin_of_error
        return lower_bound, upper_bound

    lower, upper = calculate_ci(sample_mean, sample_std, sample_size, confidence_level)

    # Plotting function
    def plot_ci_and_hypothesis(mean, std, n, lower, upper, null_hypothesis):
        # Set fixed x-axis range
        x_min = 0  # You can adjust this value as needed
        x_max = 20  # You can adjust this value as needed
        
        x = np.linspace(x_min, x_max, 1000)
        y = stats.norm.pdf(x, mean, std/np.sqrt(n))
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Sampling Distribution', line=dict(color='blue')))
        fig.add_vrect(x0=lower, x1=upper, fillcolor="rgba(0,100,80,0.2)", layer="below", line_width=0,
                      annotation_text="Confidence Interval", annotation_position="top left")
        fig.add_vline(x=mean, line_dash="dash", line_color="green", annotation_text="Sample Mean")
        fig.add_vline(x=null_hypothesis, line_dash="dash", line_color="red", annotation_text="Null Hypothesis")
        
        fig.update_layout(title='Confidence Interval and Hypothesis Test Visualization',
                          xaxis_title='Population Mean', yaxis_title='Probability Density',
                          showlegend=False, 
                          xaxis=dict(range=[x_min, x_max]),  # Set fixed x-axis range
                          yaxis=dict(range=[0, stats.norm.pdf(mean, mean, std/np.sqrt(n)) * 1.1]))  # Set y-axis range
        return fig

    with col1:
        st.plotly_chart(plot_ci_and_hypothesis(sample_mean, sample_std, sample_size, lower, upper, null_hypothesis), use_container_width=True)

    st.subheader("🧮 Calculations")
    st.markdown(f"""
    <div class="info-box">
        <h4>Confidence Interval:</h4>
        CI = x̄ ± (z * (s / √n))
        <br>Where:
        <ul>
            <li>x̄ = sample mean = {sample_mean:.2f}</li>
            <li>s = sample standard deviation = {sample_std:.2f}</li>
            <li>n = sample size = {sample_size}</li>
            <li>z = z-score for {confidence_level:.0%} confidence = {stats.norm.ppf((1 + confidence_level) / 2):.3f}</li>
        </ul>
        <strong>Result: ({lower:.3f}, {upper:.3f})</strong>
    </div>
    
    <div class="info-box">
        <h4>Hypothesis Test:</h4>
        H₀: μ = {null_hypothesis:.2f}
        <br>H₁: μ ≠ {null_hypothesis:.2f}
        <br>
        <strong>Result: {
            "Fail to reject H₀" if lower <= null_hypothesis <= upper 
            else "Reject H₀"
        }</strong>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.header("Solved Examples")
    
    st.markdown("""
    <div class="solved-example">
    <h3>Example 1: Confidence Interval for Mean Weight Loss</h3>
    <p><strong>Problem:</strong> A nutritionist is testing a new diet plan. In a sample of 36 participants, the mean weight loss was 4.2 kg with a standard deviation of 1.8 kg. Calculate a 95% confidence interval for the mean weight loss in the population.</p>
    <p><strong>Solution:</strong></p>
    <ol>
        <li>Sample mean (x̄) = 4.2 kg</li>
        <li>Sample standard deviation (s) = 1.8 kg</li>
        <li>Sample size (n) = 36</li>
        <li>For 95% confidence, z-score = 1.96</li>
        <li>Standard error (SE) = s / √n = 1.8 / √36 = 0.3</li>
        <li>Margin of error = z * SE = 1.96 * 0.3 = 0.588</li>
        <li>Confidence Interval = x̄ ± margin of error = 4.2 ± 0.588</li>
    </ol>
    <p>Therefore, the 95% confidence interval is (3.612 kg, 4.788 kg).</p>
    <p>Interpretation: We can be 95% confident that the true population mean weight loss falls between 3.612 kg and 4.788 kg.</p>
    </div>
    
    <div class="solved-example">
    <h3>Example 2: Hypothesis Test for Mean Weight Loss</h3>
    <p><strong>Problem:</strong> Using the same data as Example 1, test the hypothesis that the mean weight loss is different from 3.5 kg at a 5% significance level.</p>
    <p><strong>Solution:</strong></p>
    <ol>
        <li>Null Hypothesis (H₀): μ = 3.5 kg</li>
        <li>Alternative Hypothesis (H₁): μ ≠ 3.5 kg</li>
        <li>We already calculated the 95% CI: (3.612 kg, 4.788 kg)</li>
        <li>The null hypothesis value (3.5 kg) is outside this interval</li>
    </ol>
    <p>Since 3.5 kg is outside the 95% confidence interval, we reject the null hypothesis at a 5% significance level.</p>
    <p>Conclusion: There is sufficient evidence to conclude that the true mean weight loss is different from 3.5 kg.</p>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.header("Quiz Time!")
    
    questions = [
        {
            "question": "What does a 95% confidence interval mean?",
            "options": ["95% of the data falls within this range", "We are 95% certain the true parameter is in this range", "95% of samples will contain the true parameter"],
            "correct": "95% of samples will contain the true parameter",
            "explanation": """A 95% confidence interval means that if we were to repeat our sampling process many times and 
            calculate the interval each time, about 95% of these intervals would contain the true population parameter. 
            It's like a fishing net: if we cast our net (calculate the interval) 100 times, about 95 of those casts would 
            catch the true parameter. For example, if we calculate a 95% CI for average weight loss to be (3.5 kg, 4.5 kg), 
            it means that if we repeated this study many times, about 95% of the calculated intervals would contain the 
            true population mean weight loss."""
        },
        {
            "question": "If the null hypothesis value falls outside the confidence interval, what do we conclude?",
            "options": ["Fail to reject H₀", "Reject H₀", "Not enough information"],
            "correct": "Reject H₀",
            "explanation": """When the null hypothesis value falls outside the confidence interval, we reject H₀. 
            This is because the confidence interval contains all plausible values for the population parameter 
            that are consistent with the sample data. If the null hypothesis value is not in this interval, 
            it's considered unlikely to be the true population parameter. For instance, if our 95% CI for mean 
            weight loss is (3.5 kg, 4.5 kg) and our null hypothesis is that the mean weight loss is 3 kg, 
            we would reject this hypothesis because 3 kg is not within our interval of plausible values."""
        },
        {
            "question": "How does increasing sample size generally affect the width of a confidence interval?",
            "options": ["Widens it", "Narrows it", "Has no effect"],
            "correct": "Narrows it",
            "explanation": """Increasing the sample size generally narrows the confidence interval. This is because a larger sample 
            size provides more information about the population, reducing uncertainty. Think of it like taking more measurements 
            to get a more precise estimate. For example, if we increase our sample of weight loss measurements from 30 people to 
            300 people, our confidence interval might narrow from (3.5 kg, 4.5 kg) to (3.8 kg, 4.2 kg), giving us a more precise 
            estimate of the true average weight loss."""
        }
    ]

    for i, q in enumerate(questions):
        st.markdown(f"""
        <div class="quiz-question">
        <h3>Question {i+1}</h3>
        <p>{q["question"]}</p>
        </div>
        """, unsafe_allow_html=True)
        response = st.radio(f"Select your answer for Question {i+1}:", q["options"], key=f"q{i}")
        if st.button(f"Check Answer {i+1}"):
            if response == q["correct"]:
                st.success("🎉 Correct!")
            else:
                st.error("❌ Incorrect. Try again!")
            st.info(f"Explanation: {q['explanation']}")
        st.markdown("---")

with tab4:
    st.header("Learn More")
    st.markdown("""
    Want to dive deeper into statistical inference? Check out these resources:
    
    1. [Khan Academy: Confidence Intervals](https://www.khanacademy.org/math/statistics-probability/confidence-intervals-one-sample)
    2. [StatQuest: Hypothesis Testing and p-values](https://www.youtube.com/watch?v=vemZtEM63GY)
    3. [Statistics How To: Confidence Intervals vs Hypothesis Tests](https://www.statisticshowto.com/probability-and-statistics/hypothesis-testing/confidence-interval-hypothesis-testing/)
    4. [OpenIntro Statistics (free textbook)](https://www.openintro.org/book/os/)
    5. [Interactive Statistics Visualizations](https://seeing-theory.brown.edu/index.html)
    
    Remember, practice makes perfect! Try working through more examples and problems to solidify your understanding.
    """)

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit | © 2024 Statistical Inference Explorer")tbook)](https://www.openintro.org/book/os/)
    5. [Interactive Statistics Visualizations](https://seeing-theory.brown.edu/index.html)
    
    Remember, practice makes perfect! Try working through more examples and problems to solidify your understanding.
    """)

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit | © 2024 Statistical Inference Explorer")
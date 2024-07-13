import streamlit as st
import plotly.graph_objects as go
import numpy as np
from scipy import stats
import pandas as pd

st.set_page_config(layout="wide", page_title="Hypothesis Testing Steps")

# Custom CSS for better styling
st.markdown("""
<style>
    body {
        color: #333;
        background-color: #f0f8ff;
    }
    .main > div {
        padding-top: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .st-emotion-cache-16idsys p {
        font-size: 1.2rem;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    .highlight {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #3498db;
    }
    .solved-example {
        background-color: #f1f8e9;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #8bc34a;
        margin-top: 1rem;
    }
    .quiz-question {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #ff9800;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 Hypothesis Testing Steps")
st.write('**Developed by : Venugopal Adep**')

st.markdown("""
Welcome, statistical explorer! 🌟 Embark on an exciting journey through the world of hypothesis testing. 
We'll uncover the mysteries of data analysis using a real-world scenario: testing if a new teaching method improves student test scores.
""")

# Tabs for navigation
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🌈 Introduction", "🎯 Hypothesis Setup", "📊 Test Statistic", 
    "🔬 Data Analysis", "🧠 Decision Making", "🏆 Quiz Time"
])

with tab1:
    st.header("📚 Introduction to Hypothesis Testing")
    
    st.markdown("""
    Hypothesis testing is like being a detective in the world of statistics! 🕵️‍♀️ It helps us make educated guesses about large groups based on smaller samples.
    
    Here's our mission:
    1. 📝 Write down our guesses (hypotheses)
    2. 🧮 Choose a way to measure our results
    3. 🎚️ Decide how sure we want to be
    4. 🔍 Collect and analyze clues (data)
    5. 🏁 Make a final decision
    
    Let's dive into each step using our teaching method mystery!
    """)
    
    st.image("https://www.simplypsychology.org/wp-content/uploads/hypothesis-testing.jpg", caption="The Hypothesis Testing Process")

with tab2:
    st.header("1️⃣ Setting up the Hypotheses")
    
    st.markdown("""
    Imagine we're educational detectives 🕵️‍♂️🕵️‍♀️:
    - The average test score with the old teaching method is 70.
    - We suspect the new method might boost this average.
    
    Let's write down our guesses:
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="highlight">
        <h3>Null Hypothesis (H₀)</h3>
        The new teaching method doesn't change anything (average score stays at 70)
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="highlight">
        <h3>Alternative Hypothesis (H₁)</h3>
        The new teaching method works magic (average score goes above 70)
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.header("2️⃣ Choosing a Test Statistic")
    
    st.markdown("""
    We need a special tool to measure our results. In our case, we'll use the Z-test because:
    - We're looking at the average score of a large group
    - We know how much scores usually vary
    - We're testing more than 30 students
    """)
    
    st.latex(r"Z = \frac{\bar{x} - \mu_0}{\sigma / \sqrt{n}}")
    
    st.markdown("""
    This formula is like a magical spell ✨:
    - x̄ is the average score we find
    - μ₀ is the old average score (70)
    - σ is how much scores usually bounce around
    - n is how many students we test
    """)

    st.subheader("📊 Test Statistic Selection Guide")
    
    st.markdown("""
    Choosing the right test statistic is crucial for accurate hypothesis testing. Here's a handy guide to help you select the appropriate test based on your data and research question:
    """)

    test_statistic_data = {
        "Test Statistic": ["Z-test", "T-test", "Chi-Square test", "F-test", "ANOVA"],
        "When to Use": [
            "Large sample (n > 30), known population standard deviation",
            "Small sample (n < 30) or unknown population standard deviation",
            "Categorical data, testing independence or goodness of fit",
            "Comparing variances of two populations",
            "Comparing means of three or more groups"
        ],
        "Example Scenario": [
            "Testing if a new drug affects average blood pressure in a large group",
            "Comparing average test scores between two small classes",
            "Testing if gender is related to preference for different ice cream flavors",
            "Comparing the variability of crop yields between two farming methods",
            "Comparing average salaries across multiple job sectors"
        ]
    }

    df = pd.DataFrame(test_statistic_data)
    
    st.table(df.style.set_properties(**{'text-align': 'left'})
             .set_table_styles([dict(selector='th', props=[('text-align', 'center')])]))

    st.markdown("""
    <div class="highlight">
    <h4>💡 Pro Tip:</h4>
    Remember, choosing the right test statistic is just the first step. Always consider your sample size, data type, and research question when designing your hypothesis test!
    </div>
    """, unsafe_allow_html=True)

with tab4:
    st.header("3️⃣ Setting the Significance Level & 4️⃣ Analyzing Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        alpha = st.slider("Choose how sure you want to be (significance level α):", 0.01, 0.10, 0.05, 0.01)
        st.markdown(f"You've selected α = {alpha} (that's {alpha*100}% chance of being wrong)")
        
        n = st.number_input("How many students are we testing?", min_value=31, value=50)
        sigma = st.number_input("How much do scores usually vary? (σ)", min_value=1.0, value=15.0)
        effect_size = st.slider("How much do you think scores will improve?", -10.0, 10.0, 2.0, 0.1)
    
    with col2:
        mu = 70  # null hypothesis mean
        
        # Simulating data
        np.random.seed(42)
        sample_data = np.random.normal(mu + effect_size, sigma, n)
        sample_mean = np.mean(sample_data)
        
        # Calculating Z-score and p-value
        z_score = (sample_mean - mu) / (sigma / np.sqrt(n))
        p_value = 1 - stats.norm.cdf(z_score)
        
        st.markdown(f"📊 Average score we found: **{sample_mean:.2f}**")
        st.markdown(f"🧮 Z-score (our magic number): **{z_score:.2f}**")
        st.markdown(f"🎲 p-value (chance of being wrong): **{p_value:.4f}**")
    
    # Plotting
    fig = go.Figure()
    x = np.linspace(mu - 4*sigma/np.sqrt(n), mu + 4*sigma/np.sqrt(n), 1000)
    y = stats.norm.pdf(x, mu, sigma/np.sqrt(n))
    
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='If nothing changed', line=dict(color='royalblue')))
    fig.add_trace(go.Scatter(x=[sample_mean], y=[0], mode='markers', name='What we found',
                             marker=dict(size=12, color='red', symbol='star')))
    
    fig.add_shape(type="line", x0=mu + stats.norm.ppf(1-alpha) * sigma/np.sqrt(n), y0=0, 
                  x1=mu + stats.norm.ppf(1-alpha) * sigma/np.sqrt(n), y1=max(y),
                  line=dict(color="green", width=2, dash="dash"))
    
    fig.update_layout(title="Our Results vs What We Expected",
                      xaxis_title="Average Score",
                      yaxis_title="How likely",
                      legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.header("5️⃣ Making a Decision")
    
    if p_value < alpha:
        st.markdown(f"""
        <div class="highlight">
        <h3>Conclusion: The new method works! 🎉</h3>
        Our chance of being wrong ({p_value:.4f}) is less than what we're okay with ({alpha})
        
        We can say the new teaching method really does improve scores!
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="highlight">
        <h3>Conclusion: We're not sure if the new method works 🤔</h3>
        Our chance of being wrong ({p_value:.4f}) is more than what we're okay with ({alpha})
        
        We can't say for sure if the new teaching method makes a difference.
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="solved-example">
    <h3>🧮 Solved Example</h3>
    Let's say we tested 50 students, and their average score was 75. We know scores usually vary by about 15 points.
    
    1. Calculate the Z-score:
       Z = (75 - 70) / (15 / √50) = 2.36
    
    2. Find the p-value:
       p-value = 1 - 0.9909 = 0.0091
    
    3. Compare to α (let's say 0.05):
       0.0091 < 0.05
    
    Conclusion: We reject the null hypothesis! The new method seems to work!
    </div>
    """, unsafe_allow_html=True)

with tab6:
    st.header("🏆 Quiz Time")
    
    st.markdown("""
    Let's test your newfound knowledge with some fun questions!
    """)
    
    q1 = st.radio(
        "1. What happens to the chance of making a mistake (Type I error) if we want to be more sure (lower α)?",
        ("It goes up", "It goes down", "It stays the same")
    )
    
    if st.button("Check Answer for Question 1"):
        if q1 == "It goes down":
            st.markdown("""
            <div class="quiz-question">
            ✅ Correct! You're a hypothesis testing wizard! 🧙‍♂️
            
            When we lower α (like changing from 0.05 to 0.01), we're saying "I want to be really, really sure before I say the new method works." 
            It's like setting a higher bar for evidence. This makes it harder to accidentally say the method works when it doesn't (Type I error).
            
            Example: Imagine you're testing a new diet. If you set α to 0.05, you might say it works if you lose just a little weight. 
            But if you set α to 0.01, you'd need to lose more weight before you'd say the diet really works. You're less likely to be fooled by normal weight fluctuations.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="quiz-question">
            ❌ Not quite, but don't worry! Let's break it down:
            
            The correct answer is: It goes down.
            
            Think of α like a threshold for believing something works. A lower α means you need stronger evidence. 
            This makes it harder to accidentally say something works when it doesn't (Type I error).
            
            Example: If you're testing a new medicine, a lower α means you need to see better results before you say it works. 
            This reduces the chance of approving a medicine that doesn't actually help.
            </div>
            """, unsafe_allow_html=True)
    
    q2 = st.radio(
        "2. What does a p-value tell us?",
        ("The probability the null hypothesis is true", 
         "The probability of getting our results if the null hypothesis is true", 
         "The probability the alternative hypothesis is true")
    )
    
    if st.button("Check Answer for Question 2"):
        if q2 == "The probability of getting our results if the null hypothesis is true":
            st.markdown("""
            <div class="quiz-question">
            ✅ Bravo! You've cracked the p-value code! 🕵️‍♀️
            
            The p-value is like asking, "If nothing actually changed (null hypothesis is true), what are the odds we'd see results this extreme?"
            
            Example: Imagine you're flipping a coin. You flip it 100 times and get 60 heads. The p-value would tell you, 
            "If this coin was fair (null hypothesis), what's the chance we'd see 60 or more heads out of 100 flips?" 
            If this chance (p-value) is really small, you might start to suspect the coin isn't fair after all!
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="quiz-question">
            ❌ Close, but not quite. Let's clarify:
            
            The correct answer is: The probability of getting our results if the null hypothesis is true.
            
            The p-value doesn't tell us if the null hypothesis is true or false. It tells us how surprising our results would be if nothing had changed.
            
            Example: If you're testing a "lucky" rabbit's foot, and you win 8 out of 10 games (when you usually win 5), the p-value tells you 
            how often you'd win 8 or more games if the foot wasn't actually lucky. If this p-value is very small, you might start to wonder if the foot really is lucky!
            </div>
            """, unsafe_allow_html=True)
    
    q3 = st.radio(
        "3. What does rejecting the null hypothesis mean?",
        ("We've proven the alternative hypothesis", 
         "We have evidence supporting the alternative hypothesis", 
         "The null hypothesis is definitely false")
    )
    
    if st.button("Check Answer for Question 3"):
        if q3 == "We have evidence supporting the alternative hypothesis":
            st.markdown("""
            <div class="quiz-question">
            ✅ Fantastic! You're thinking like a true scientist! 🧑‍🔬
            
            Rejecting the null hypothesis means we have good evidence for the alternative, but it's not absolute proof.
            
            Example: Imagine you're testing if a new fertilizer helps plants grow taller. If you reject the null hypothesis, 
            you're saying, "Based on our data, it looks like this fertilizer really does help plants grow taller!" 
            But you're not saying it's 100% certain or that it will work in all situations. You're just saying the evidence points that way.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="quiz-question">
            ❌ Not quite right, but you're on the right track! Let's explain:
            
            The correct answer is: We have evidence supporting the alternative hypothesis.
            
            Rejecting the null doesn't mean we've proven anything with 100% certainty. It just means the evidence strongly suggests the alternative hypothesis might be true.
            
            Example: If you're testing a new exercise program and reject the null hypothesis that it doesn't improve fitness, you're saying, "Our data suggests this program does improve fitness." 
            But you're not claiming it's proven beyond all doubt or that it works for everyone. You're just saying the evidence points in that direction.
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    ### 🌟 Bonus Resources
    
    Want to become a hypothesis testing superhero? Check out these awesome resources:
    - [Khan Academy: Hypothesis Testing](https://www.khanacademy.org/math/statistics-probability/significance-tests-one-sample) - Learn from the masters!
    - [StatQuest: Hypothesis Testing and p-values](https://www.youtube.com/watch?v=vemZtEM63GY) - Visual explanations that stick!
    - [Crash Course Statistics: Hypothesis Testing](https://www.youtube.com/watch?v=WWdpLbbBveo) - Fast, fun, and informative!
    """)



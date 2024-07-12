import streamlit as st
import plotly.graph_objects as go
import numpy as np
from scipy import stats

# Set page config
st.set_page_config(layout="wide", page_title="Justice System Error Explorer", page_icon="⚖️")

# Custom CSS
st.markdown("""
<style>
    .main {max-width: 1200px; margin: 0 auto;}
    .stApp {padding-top: 1rem; background-color: #f0f4f8;}
    .st-emotion-cache-10trblm {text-align: center;}
    .info-box {background-color: #e1e5eb; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    .quiz-container {background-color: #d0e1f9; padding: 20px; border-radius: 10px; margin-top: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    .stTabs {background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    .plot-container {display: flex; justify-content: space-between;}
    .plot {width: 70%;}
    .sliders {width: 25%; padding-left: 20px;}
    .stButton>button {background-color: #4e8cff; color: white;}
    .stButton>button:hover {background-color: #3a7be0;}
</style>
""", unsafe_allow_html=True)

# Title and introduction
st.title("⚖️ Justice System Error Explorer")
st.markdown("Explore the intricacies of Type I and Type II errors in the context of the justice system.")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["📚 Concept", "📊 Visualization", "🧮 Case Studies", "🧠 Quiz"])

with tab1:
    st.header("Understanding Errors in the Justice System")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-box">
        <h3>🚨 Type I Error (False Conviction)</h3>
        <ul>
        <li>Convicting an innocent person</li>
        <li>Probability = α (significance level)</li>
        <li>"Sending an innocent person to jail"</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="info-box">
        <h3>😴 Type II Error (False Acquittal)</h3>
        <ul>
        <li>Failing to convict a guilty person</li>
        <li>Probability = β</li>
        <li>"Letting a criminal go free"</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <h3>🔑 Key Concepts in the Justice System</h3>
    <ul>
        <li>α: The risk of wrongful convictions</li>
        <li>β: The risk of wrongful acquittals</li>
        <li>Power (1 - β): The ability to convict truly guilty individuals</li>
        <li>Tradeoff: A stricter justice system (lower α) might increase wrongful acquittals (higher β)</li>
        <li>Better evidence and thorough investigations help reduce both types of errors</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.header("Interactive Visualization: Justice System Errors")
    
    col1, col2 = st.columns([0.7, 0.3])
    
    with col2:
        st.subheader("Adjust Court Parameters")
        innocence_mean = st.slider("Innocence Evidence Mean", 0.0, 5.0, 2.5, 0.1)
        guilt_mean = st.slider("Guilt Evidence Mean", 0.0, 5.0, 3.5, 0.1)
        evidence_variability = st.slider("Evidence Variability", 0.1, 2.0, 1.0, 0.1)
        conviction_threshold = st.slider("Conviction Threshold", 0.01, 0.10, 0.05, 0.01)
    
    # Calculate critical value and probabilities
    z_crit = stats.norm.ppf(1 - conviction_threshold)
    evidence_threshold = innocence_mean + z_crit * evidence_variability
    
    x = np.linspace(0, 5, 1000)
    y_innocent = stats.norm.pdf(x, innocence_mean, evidence_variability)
    y_guilty = stats.norm.pdf(x, guilt_mean, evidence_variability)
    
    false_conviction_rate = 1 - stats.norm.cdf(evidence_threshold, innocence_mean, evidence_variability)
    false_acquittal_rate = stats.norm.cdf(evidence_threshold, guilt_mean, evidence_variability)
    conviction_power = 1 - false_acquittal_rate
    
    # Create plot
    fig = go.Figure()
    
    # Innocent Population
    fig.add_trace(go.Scatter(x=x, y=y_innocent, name="Innocent Population", 
                             fill='tozeroy', fillcolor='rgba(0,176,246,0.2)',
                             line=dict(color='blue')))
    
    # Guilty Population
    fig.add_trace(go.Scatter(x=x, y=y_guilty, name="Guilty Population", 
                             fill='tozeroy', fillcolor='rgba(231,107,243,0.2)',
                             line=dict(color='purple')))
    
    # Evidence threshold line
    fig.add_vline(x=evidence_threshold, line_dash="dash", line_color="red", 
                  annotation=dict(text="Conviction Threshold", textangle=-90, yshift=10))
    
    # Type I Error (False Conviction)
    x_type1 = x[x >= evidence_threshold]
    y_type1 = stats.norm.pdf(x_type1, innocence_mean, evidence_variability)
    fig.add_trace(go.Scatter(x=x_type1, y=y_type1, fill='tozeroy', 
                             fillcolor='rgba(255,0,0,0.3)', name='False Conviction (Type I)',
                             line=dict(color='red')))
    
    # Type II Error (False Acquittal)
    x_type2 = x[x <= evidence_threshold]
    y_type2 = stats.norm.pdf(x_type2, guilt_mean, evidence_variability)
    fig.add_trace(go.Scatter(x=x_type2, y=y_type2, fill='tozeroy', 
                             fillcolor='rgba(0,255,0,0.3)', name='False Acquittal (Type II)',
                             line=dict(color='green')))
    
    # Annotations
    fig.add_annotation(x=innocence_mean, y=max(y_innocent)/2, text="Typical Innocent", showarrow=True, arrowhead=2, ax=0, ay=-40)
    fig.add_annotation(x=guilt_mean, y=max(y_guilty)/2, text="Typical Guilty", showarrow=True, arrowhead=2, ax=0, ay=-40)
    fig.add_annotation(x=(evidence_threshold + 5)/2, y=max(y_innocent)/4, text="Convicted", showarrow=False)
    fig.add_annotation(x=evidence_threshold/2, y=max(y_innocent)/4, text="Acquitted", showarrow=False)
    
    fig.update_layout(
        title="Understanding Errors in the Justice System",
        xaxis_title="Strength of Evidence",
        yaxis_title="Probability Density",
        xaxis=dict(range=[0, 5]),
        legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=0),
        height=600,
        annotations=[
            dict(x=0.5, y=1.05, xref="paper", yref="paper", text=f"False Conviction Rate: {false_conviction_rate:.2%}", showarrow=False),
            dict(x=0.5, y=1.10, xref="paper", yref="paper", text=f"False Acquittal Rate: {false_acquittal_rate:.2%}", showarrow=False),
            dict(x=0.5, y=1.15, xref="paper", yref="paper", text=f"Conviction Power: {conviction_power:.2%}", showarrow=False)
        ],
        margin=dict(t=150)
    )
    
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("How to Interpret This Court Case Visualization")
    st.markdown("""
    This plot represents how evidence is distributed in court cases:

    1. **Blue Curve (Innocent Population)**: Distribution of evidence for innocent individuals
       - Center: Typical evidence level for innocent people
       - Spread: Variation in evidence among innocent individuals

    2. **Purple Curve (Guilty Population)**: Distribution of evidence for guilty individuals
       - Shifted right: Indicates stronger evidence against guilty individuals
       - Overlap with blue: Difficulty in distinguishing guilt from innocence

    3. **Red Line (Conviction Threshold)**: The evidence level required for conviction
       - Right of line: Evidence strong enough for conviction
       - Left of line: Insufficient evidence for conviction

    4. **Red Area (False Conviction)**: Chance of wrongly convicting an innocent person
       - "Type I Error" or "Miscarriage of Justice"

    5. **Green Area (False Acquittal)**: Chance of failing to convict a guilty person
       - "Type II Error" or "Letting a Criminal Go Free"

    6. **Evidence Strength (X-axis)**: Measures the strength of evidence in a case
       - Larger values suggest stronger evidence of guilt

    **Key Takeaways:**
    - Separation between curves: Easier to distinguish guilt from innocence
    - Overlap of curves: Risk of judicial errors
    - Moving red line right: Reduces false convictions, but may let more guilty people go free
    - Moving red line left: Convicts more guilty people, but risks more false convictions

    **Experiment:**
    1. Adjust the "Guilt Evidence Mean". How does this affect the justice system's accuracy?
    2. Change the "Evidence Variability". How does this impact the court's ability to make correct judgments?
    3. Modify the "Conviction Threshold". Observe how this affects false convictions and acquittals.

    Remember: In real court cases, we don't see these full distributions. This visualization helps us understand the challenges in making just decisions based on available evidence!
    """)

with tab3:
    st.header("Real Court Case Studies")
    
    st.markdown("""
    <div class="info-box">
    <h3>Case Study: The Impact of DNA Evidence</h3>
    In a murder trial, the following probabilities were estimated:
    - False Conviction Rate (α) = 0.01 (1%)
    - False Acquittal Rate (β) = 0.2 (20%)
    
    Questions:
    1. What's the probability of wrongly convicting an innocent person?
    2. What's the probability of correctly convicting a guilty person (Power)?
    3. How might introducing DNA evidence change these probabilities?
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Reveal Analysis"):
        st.markdown("""
        <div class="info-box">
        <h4>Analysis:</h4>
        1. Probability of wrongly convicting an innocent person = α = 0.01 (1%)
        2. Power = 1 - β = 1 - 0.2 = 0.8 (80%)
        3. Introducing DNA evidence:
           - Likely decreases α (fewer innocent people convicted)
           - Likely decreases β (fewer guilty people acquitted)
           - Increases overall accuracy and power of the justice system
        
        <h4>Real-world Interpretation:</h4>
        - There's a 1% chance of sending an innocent person to jail (1 out of 100 cases)
        - The court has an 80% chance of correctly convicting a guilty person
        - 20% of guilty individuals might be wrongly acquitted
        
        DNA evidence could significantly improve these numbers by providing more conclusive evidence, 
        potentially reducing both types of errors and increasing the court's ability to make correct judgments.
        </div>
        """, unsafe_allow_html=True)

with tab4:
    st.header("Justice System Quiz")
    
    st.markdown("""
    <div class="quiz-container">
    Test your understanding of errors in the justice system:
    </div>
    """, unsafe_allow_html=True)
    
    q1 = st.radio(
        "1. What happens to false acquittals (Type II errors) when we make the justice system stricter (lower α)?",
        ["Decrease", "Increase", "Stay the same", "Become zero"]
    )
    
    if st.button("Check Answer", key="q1"):
        if q1 == "Increase":
            st.success("Correct! 🎉")
            st.markdown("""
            <div class="info-box">
            <h4>Explanation:</h4>
            When we make the justice system stricter (lower α), we require more evidence to convict. 
            This means we're less likely to convict innocent people (fewer Type I errors), but more likely to let guilty people go free (more Type II errors).
            
            Think of it like a very cautious judge. They're less likely to convict without rock-solid evidence, 
            which protects the innocent but might also allow some guilty individuals to escape conviction.
            
            Example: If we require DNA evidence for all convictions, we'd have fewer wrongful convictions, 
            but we might fail to convict in cases where DNA evidence isn't available, even if other evidence suggests guilt.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Not quite. Consider how stricter conviction requirements might affect guilty individuals.")

    q2 = st.radio(
        "2. Which of the following would likely improve both types of errors in the justice system?",
        ["Increasing jail sentences", "Improving forensic technology", "Reducing the number of judges", "Speeding up trials"]
    )

    if st.button("Check Answer", key="q2"):
        if q2 == "Improving forensic technology":
            st.success("Correct! 🎉")
            st.markdown("""
            <div class="info-box">
            <h4>Explanation:</h4>
            Improving forensic technology helps reduce both Type I and Type II errors by providing more accurate and reliable evidence. 
            
            Better forensic tech allows us to:
            1. More accurately identify guilty individuals (reducing Type II errors)
            2. More confidently exonerate innocent individuals (reducing Type I errors)

            Example: Advanced DNA analysis techniques can provide stronger evidence of guilt or innocence, 
            helping courts make more accurate decisions in both convicting the guilty and acquitting the innocent.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Not quite. Think about what would improve the accuracy of evidence in court cases.")

    q3 = st.radio(
            "3. In the context of the justice system, what does 'power' refer to?",
            ["The authority of the judge", "The harshness of sentences", 
             "The ability to correctly convict guilty individuals", "The number of cases processed per year"]
        )
    
        if st.button("Check Answer", key="q3"):
            if q3 == "The ability to correctly convict guilty individuals":
                st.success("Correct! 🎉")
                st.markdown("""
                <div class="info-box">
                <h4>Explanation:</h4>
                In the context of hypothesis testing and the justice system analogy, 'power' refers to the ability to correctly convict guilty individuals. It's calculated as 1 - β, where β is the probability of a Type II error (false acquittal).
    
                In simpler terms, power is the justice system's ability to identify and convict truly guilty individuals when they are indeed guilty.
    
                Example: If the justice system has 80% power in identifying drug traffickers, it means that out of 100 actual drug traffickers brought to trial, about 80 would be correctly convicted. The higher the power, the more effective the system is at bringing guilty parties to justice.
    
                High power in a justice system is crucial because:
                1. It ensures that more criminals are correctly convicted and removed from society.
                2. It acts as a deterrent, as potential criminals know they're more likely to be caught and convicted.
                3. It increases public trust in the effectiveness of the legal system.
    
                However, it's important to balance this with maintaining a low Type I error rate to protect innocent individuals from wrongful conviction.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Not quite. Think about what 'power' means in terms of the justice system's effectiveness.")
    
# Footer
st.markdown("---")
st.markdown("© 2024 Justice System Error Explorer. Created with ⚖️ using Streamlit and Plotly.")

import streamlit as st
import plotly.graph_objects as go
import numpy as np
from scipy import stats

# Set page config
st.set_page_config(layout="wide", page_title="Justice System Error Explorer", page_icon="⚖️")

# Custom CSS
st.markdown("""
<style>
    body {font-family: Arial, sans-serif;}
    .main {padding: 1rem;}
    .stApp {background-color: #f0f4f8;}
    .st-emotion-cache-10trblm {text-align: center;}
    .info-box {background-color: #e1e5eb; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    .example-box {background-color: #d4edda; padding: 15px; border-radius: 10px; margin-top: 10px; border-left: 5px solid #28a745;}
    .quiz-container {background-color: #d0e1f9; padding: 20px; border-radius: 10px; margin-top: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    .stTabs {background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    .plot-container {display: flex; justify-content: space-between; align-items: flex-start;}
    .sliders {width: 30%; padding-right: 20px;}
    .plot {width: 70%;}
    .stButton>button {background-color: #4e8cff; color: white; border-radius: 5px; border: none; padding: 10px 20px; font-size: 16px;}
    .stButton>button:hover {background-color: #3a7be0;}
    h1, h2, h3 {color: #2c3e50;}
    .stSlider {margin-bottom: 20px;}
</style>
""", unsafe_allow_html=True)

# Title and introduction
st.title("⚖️ Type I and Type II Errors : Justice System Error Explorer")
st.write("**Developed by: Venugopal Adep**")
st.markdown("Dive into the world of legal decision-making and discover how errors can occur in the justice system.")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["📚 Concept", "📊 Interactive Demo", "🧮 Real-World Examples", "🧠 Quiz"])

with tab1:
    st.header("Understanding Errors in the Justice System")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-box">
        <h3>🚨 Type I Error: The Innocent Goes to Jail</h3>
        <ul>
        <li>What it is: Convicting an innocent person</li>
        <li>In stats speak: False Positive (α)</li>
        <li>Real-world impact: An innocent person loses their freedom</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="info-box">
        <h3>😴 Type II Error: The Guilty Walks Free</h3>
        <ul>
        <li>What it is: Failing to convict a guilty person</li>
        <li>In stats speak: False Negative (β)</li>
        <li>Real-world impact: A criminal remains in society</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <h3>🔑 Key Ideas to Remember</h3>
    <ul>
        <li>Balance is crucial: Reducing one type of error often increases the other</li>
        <li>The justice system's strength (Power) = Its ability to correctly convict the guilty</li>
        <li>Being too strict can lead to more innocent people in jail</li>
        <li>Being too lenient can let more criminals go free</li>
        <li>Better evidence and thorough investigations are the best way to improve accuracy</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="example-box">
    <h4>Real-life Example: The Coffee Shop Thief</h4>
    Imagine you're a cafe owner trying to catch a thief who's been stealing from the tip jar.

    <b>Type I Error (False Conviction):</b> You accuse and ban a regular customer based on shaky evidence. 
    You've just lost an innocent customer and potentially damaged your reputation.

    <b>Type II Error (False Acquittal):</b> You see someone suspicious but decide not to act. 
    If they were the thief, they'll continue stealing, harming your business and staff.

    <b>The Dilemma:</b> How strict should your policy be? Very strict policies might scare away innocent customers, 
    while very lenient ones might embolden the thief.

    Just like in the justice system, the key is finding the right balance and gathering solid evidence!
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.header("Interactive Demo: Justice System in Action")
    
    st.markdown("""
    Imagine you're designing a justice system. Use the sliders to adjust how the system works and see the impact on innocent and guilty individuals.
    """)
    
    col1, col2 = st.columns([3, 7])
    
    with col1:
        st.subheader("Adjust the System")
        innocence_mean = st.slider("Average Innocence Level", 0.0, 5.0, 2.5, 0.1, 
                                   help="Higher values mean innocent people generally have stronger evidence of innocence")
        guilt_mean = st.slider("Average Guilt Level", 0.0, 5.0, 3.5, 0.1,
                               help="Higher values mean guilty people generally have stronger evidence against them")
        evidence_variability = st.slider("Evidence Clarity", 0.1, 2.0, 1.0, 0.1,
                                         help="Lower values mean evidence is more clear-cut, higher values mean it's more ambiguous")
        conviction_threshold = st.slider("Conviction Strictness", 0.01, 0.10, 0.05, 0.01,
                                         help="Lower values mean the system is stricter, requiring more evidence to convict")
    
    with col2:
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
        fig.add_trace(go.Scatter(x=x, y=y_innocent, name="Innocent People", 
                                 fill='tozeroy', fillcolor='rgba(0,176,246,0.2)',
                                 line=dict(color='blue')))
        
        # Guilty Population
        fig.add_trace(go.Scatter(x=x, y=y_guilty, name="Guilty People", 
                                 fill='tozeroy', fillcolor='rgba(231,107,243,0.2)',
                                 line=dict(color='purple')))
        
        # Evidence threshold line
        fig.add_vline(x=evidence_threshold, line_dash="dash", line_color="red", 
                      annotation=dict(text="Conviction Line", textangle=-90, yshift=10))
        
        # Type I Error (False Conviction)
        x_type1 = x[x >= evidence_threshold]
        y_type1 = stats.norm.pdf(x_type1, innocence_mean, evidence_variability)
        fig.add_trace(go.Scatter(x=x_type1, y=y_type1, fill='tozeroy', 
                                 fillcolor='rgba(255,0,0,0.3)', name='Wrongly Convicted Innocent',
                                 line=dict(color='red')))
        
        # Type II Error (False Acquittal)
        x_type2 = x[x <= evidence_threshold]
        y_type2 = stats.norm.pdf(x_type2, guilt_mean, evidence_variability)
        fig.add_trace(go.Scatter(x=x_type2, y=y_type2, fill='tozeroy', 
                                 fillcolor='rgba(0,255,0,0.3)', name='Wrongly Freed Guilty',
                                 line=dict(color='green')))
        
        # Annotations
        fig.add_annotation(x=innocence_mean, y=max(y_innocent)/2, text="Typical Innocent Person", showarrow=True, arrowhead=2, ax=0, ay=-40)
        fig.add_annotation(x=guilt_mean, y=max(y_guilty)/2, text="Typical Guilty Person", showarrow=True, arrowhead=2, ax=0, ay=-40)
        fig.add_annotation(x=(evidence_threshold + 5)/2, y=max(y_innocent)/4, text="Convicted", showarrow=False)
        fig.add_annotation(x=evidence_threshold/2, y=max(y_innocent)/4, text="Acquitted", showarrow=False)
        
        fig.update_layout(
            title="How Evidence Affects Justice",
            xaxis_title="Strength of Evidence Against Someone",
            yaxis_title="How Common This Evidence Level Is",
            xaxis=dict(range=[0, 5]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=600,
            margin=dict(l=50, r=50, t=100, b=50),
            annotations=[
                dict(x=0.5, y=1.05, xref="paper", yref="paper", text=f"Innocent people wrongly convicted: {false_conviction_rate:.2%}", showarrow=False),
                dict(x=0.5, y=1.10, xref="paper", yref="paper", text=f"Guilty people wrongly freed: {false_acquittal_rate:.2%}", showarrow=False),
                dict(x=0.5, y=1.15, xref="paper", yref="paper", text=f"Chance of catching the truly guilty: {conviction_power:.2%}", showarrow=False)
            ]
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("What's Going On in This Picture?")
    st.markdown("""
    This graph shows how evidence is spread out in court cases:

    1. **Blue Mountain (Innocent People)**: Most innocent folks are on the left side, with less evidence against them.
    2. **Purple Mountain (Guilty People)**: Most guilty folks are on the right, with more evidence against them.
    3. **Red Line (Conviction Line)**: If someone's evidence is to the right of this line, they get convicted.
    4. **Red Area (Wrongly Convicted)**: Innocent people who end up on the wrong side of the line.
    5. **Green Area (Wrongly Freed)**: Guilty people who slip to the left of the line and go free.

    **Try This:**
    1. Move the "Average Guilt Level" slider right. See how it's now easier to tell innocent and guilty apart?
    2. Increase the "Evidence Clarity". Notice how the mountains get skinnier? This means less overlap and fewer mistakes!
    3. Slide the "Conviction Strictness" left. The red line moves right, convicting fewer innocent people but letting more guilty ones go.

    Remember, in real life, we don't get to see these full mountains. We just get one piece of evidence and have to decide. 
    This picture helps us understand why mistakes can happen and how we might make fewer of them!
    """)

with tab3:
    st.header("Real-World Justice Scenarios")
    
    st.markdown("""
    <div class="info-box">
    <h3>Case Study: DNA Evidence Revolution</h3>
    Imagine a murder trial from the 1980s. Back then, we estimated:
    - Chance of wrongly convicting an innocent person (α) = 5% (0.05)
    - Chance of freeing a guilty person (β) = 20% (0.2)
    
    Fast forward to today, with advanced DNA testing. Let's explore how this might change things.
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Reveal Analysis"):
        st.markdown("""
        <div class="info-box">
        <h4>Breaking it Down:</h4>
        1. In the 1980s:
           - 5% chance of sending an innocent person to jail (5 out of 100 cases)
           - 80% chance of correctly convicting a guilty person (1 - β = 1 - 0.2 = 0.8)
           - 20% of guilty individuals might walk free
        
        2. With modern DNA evidence:
           - α might drop to 1% (much less chance of convicting the innocent)
           - β might drop to 5% (much better at catching the guilty)
           - Power increases to 95% (1 - 0.05 = 0.95)
        
        <h4>What This Means in Real Life:</h4>
        - 1980s: If you were innocent, you had a 1 in 20 chance of being wrongly convicted. Scary!
        - Today: Your chances of a wrongful conviction might be more like 1 in 100. Much better!
        - For victims and society: We're much more likely to catch and convict the real criminals.
        
        <b>The Big Picture:</b> DNA evidence is like giving the justice system a pair of super-strong glasses. 
        It sees things much more clearly, making fewer mistakes in both directions. This is why many old cases 
        are being reopened and reviewed with new DNA evidence!
        </div>
        """, unsafe_allow_html=True)

with tab4:
    st.header("Test Your Justice System Smarts!")
    
    st.markdown("""
    <div class="quiz-container">
    Let's see how well you understand our justice system's challenges:
    </div>
    """, unsafe_allow_html=True)
    
    q1 = st.radio(
        "1. If we make our justice system super strict (lower α), what happens to the number of guilty people who might go free?",
        ["It goes down", "It goes up", "It stays the same", "It becomes zero"]
    )
    
    if st.button("Check Answer", key="q1"):
        if q1 == "It goes up":
            st.success("You got it! 🎉")
            st.markdown("""
            <div class="example-box">
            <h4>Here's Why:</h4>
            Think of it like a very picky restaurant critic. If they only give good reviews to "perfect"
restaurants, they might miss out on some really good places that have just a tiny flaw. 
            In the same way, a super strict justice system might let some guilty people go free because 
            the evidence isn't 100% perfect.

            Example: If we required video evidence for every crime, we'd rarely convict an innocent person, 
            but many guilty people would go free when there's no video available.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Not quite. Think about what happens when we set a very high bar for conviction.")

    q2 = st.radio(
        "2. Which of these would likely help reduce both types of errors in the justice system?",
        ["Harsher sentences", "Better forensic technology", "Faster trials", "More juries"]
    )

    if st.button("Check Answer", key="q2"):
        if q2 == "Better forensic technology":
            st.success("Spot on! 🎉")
            st.markdown("""
            <div class="example-box">
            <h4>Here's Why:</h4>
            Better forensic technology, like improved DNA testing or more accurate fingerprint analysis, 
            helps us gather stronger and more reliable evidence. This means:

            1. We're less likely to accuse innocent people (fewer Type I errors)
            2. We're better at identifying the truly guilty (fewer Type II errors)

            Think of it like upgrading from an old flip phone camera to a modern smartphone camera. 
            Suddenly, your pictures are clearer, and you can zoom in without everything getting blurry. 
            In the same way, better forensic tech gives us a clearer picture of what really happened in a crime.

            Example: In the past, we might have relied on eyewitness testimony, which can be unreliable. 
            Now, with DNA evidence, we can often tell with near certainty whether someone was at a crime scene.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Not quite. Consider which option would improve the quality of evidence in court cases.")

    q3 = st.radio(
        "3. In our justice system analogy, what does 'power' mean?",
        ["How long the sentences are", "How quickly trials are completed", 
         "How good we are at convicting guilty people", "How many police officers we have"]
    )

    if st.button("Check Answer", key="q3"):
        if q3 == "How good we are at convicting guilty people":
            st.success("You nailed it! 🎉")
            st.markdown("""
            <div class="example-box">
            <h4>Here's Why:</h4>
            In the context of our justice system analogy, 'power' refers to how good we are at correctly 
            identifying and convicting people who are actually guilty. It's calculated as 1 - β, where β 
            is the probability of a Type II error (letting a guilty person go free).

            Think of it like a basketball player's shooting percentage. A player with a high shooting percentage 
            (high power) is really good at making baskets when they take a shot. Similarly, a justice system 
            with high power is really good at convicting guilty people when they're brought to trial.

            Example: If our justice system has 80% power in identifying drug dealers, it means that out of 
            100 actual drug dealers brought to trial, about 80 would be correctly convicted. The higher the 
            power, the more effective the system is at bringing guilty parties to justice.

            Why it matters:
            1. It helps keep society safer by removing more criminals from the streets.
            2. It can deter crime, as potential criminals know they're more likely to get caught and convicted.
            3. It increases public trust in the legal system.

            Remember, though, we always want to balance this with keeping the Type I error rate (wrongly 
            convicting innocent people) as low as possible. It's a constant balancing act!
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Not quite. Think about what 'power' might mean in terms of the justice system's effectiveness.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #777;">
© 2024 Justice System Error Explorer | Developed by Venugopal Adep<br>
This interactive tool is for educational purposes only and does not represent any specific legal system.
</div>
""", unsafe_allow_html=True)

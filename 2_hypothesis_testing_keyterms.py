import streamlit as st
import numpy as np
from scipy import stats
import plotly.graph_objects as go

st.set_page_config(page_title="Understanding Evidence in Justice", layout="wide")

st.title("⚖️ Understanding Evidence in Justice")
st.write("**Developed by: Venugopal Adep**")

tab1, tab2, tab3, tab4 = st.tabs(["📚 Key Ideas", "🎮 Try It Yourself", "🧑‍⚖️ Real Example", "🧠 Quiz"])

with tab1:
    st.header("Key Ideas in Evaluating Evidence")
    
    st.subheader("Null Hypothesis (H₀)")
    st.write("Our starting assumption: 'The defendant is innocent' or 'Nothing has changed'.")
    
    st.subheader("Alternative Hypothesis (H₁)")
    st.write("What we're trying to prove: 'The defendant is guilty' or 'Something has changed'.")
    
    st.subheader("Significance Level (α)")
    st.write("How sure we need to be before rejecting H₀. Usually set at 0.05 (95% sure) or 0.01 (99% sure).")
    
    st.subheader("p-value")
    st.write("The probability of seeing our evidence (or more extreme) if H₀ is true. Smaller p-values suggest stronger evidence against H₀.")
    
    st.subheader("Type I Error")
    st.write("Rejecting H₀ when it's actually true. In justice, this means convicting an innocent person.")
    
    st.subheader("Type II Error")
    st.write("Failing to reject H₀ when it's actually false. In justice, this means letting a guilty person go free.")
    
    st.subheader("The Final Decision")
    st.write("We either 'reject H₀' (conclude guilt/change) or 'fail to reject H₀' (not enough evidence for guilt/change).")

with tab2:
    st.header("Try It Yourself: Evaluating Evidence")

    st.write("This interactive tool shows how the amount of evidence affects our decision.")
    
    col1, col2 = st.columns([1, 2])

    with col1:
        total_evidence = st.slider("Total pieces of evidence", 10, 1000, 100, key="total_evidence_1")
        incriminating_evidence = st.slider("Pieces of strong evidence", 0, total_evidence, total_evidence // 2, key="incriminating_evidence_1")
        alpha = st.select_slider("Significance Level (α)", options=[0.01, 0.05, 0.1], value=0.05, key="alpha_1")

        p_value = 1 - stats.binom.cdf(incriminating_evidence - 1, total_evidence, 0.5)

        st.write(f"p-value: {p_value:.4f}")
        
        if p_value < alpha:
            st.error("Reject H₀ (Evidence suggests guilt)")
        else:
            st.success("Fail to reject H₀ (Not enough evidence to conclude guilt)")

    with col2:
        x = np.linspace(0, total_evidence, 1000)
        y = stats.norm.pdf(x, total_evidence/2, np.sqrt(total_evidence/4))

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Evidence Distribution', line=dict(color='blue', width=2)))

        critical_value = stats.norm.ppf(1-alpha, total_evidence/2, np.sqrt(total_evidence/4))

        fig.add_trace(go.Scatter(
            x=np.concatenate([x[x <= critical_value], [critical_value]]),
            y=np.concatenate([y[x <= critical_value], [0]]),
            fill='tozeroy', fillcolor='rgba(0,255,0,0.3)', line_color='rgba(255,255,255,0)',
            name='Fail to Reject H₀'
        ))

        fig.add_trace(go.Scatter(
            x=np.concatenate([[critical_value], x[x > critical_value]]),
            y=np.concatenate([[0], y[x > critical_value]]),
            fill='tozeroy', fillcolor='rgba(255,0,0,0.3)', line_color='rgba(255,255,255,0)',
            name='Reject H₀'
        ))

        fig.add_vline(x=incriminating_evidence, line_dash="dash", line_color="black", 
                      annotation_text="Observed Evidence", annotation_position="top right")

        fig.add_vline(x=critical_value, line_dash="dash", line_color="red", 
                      annotation_text=f"Critical Value (α={alpha})", annotation_position="bottom right")

        fig.add_annotation(x=total_evidence/4, y=max(y), text="H₀: Innocent", showarrow=False, yshift=10)
        fig.add_annotation(x=3*total_evidence/4, y=max(y), text="H₁: Guilty", showarrow=False, yshift=10)
        fig.add_annotation(x=total_evidence/8, y=max(y)/2, text="Type II Error (β)", showarrow=False)
        fig.add_annotation(x=7*total_evidence/8, y=max(y)/2, text="Type I Error (α)", showarrow=False)

        fig.update_layout(
            title='Distribution of Evidence',
            xaxis_title='Amount of Incriminating Evidence',
            yaxis_title='Probability Density',
            height=600,
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)

    st.write("""
    What this shows:
    - H₀ (Null Hypothesis): The defendant is innocent
    - H₁ (Alternative Hypothesis): The defendant is guilty
    - The blue curve shows the distribution of evidence if H₀ is true
    - The green area is where we fail to reject H₀ (not enough evidence for guilt)
    - The red area is where we reject H₀ (strong evidence suggesting guilt)
    - α (alpha) is the significance level, representing the Type I error rate
    - β (beta) represents the Type II error rate (not directly shown)
    - The black line shows the observed evidence
    - If the black line is in the red area, we reject H₀ (conclude guilt)
    """)

with tab3:
    st.header("Real Example: Investigating a Traffic Claim")

    st.write("""
    Scenario: Someone claims that the rate of speeding at an intersection has increased. 
    Let's investigate this claim using our evidence evaluation tool.
    """)

    col1, col2 = st.columns([1, 2])

    with col1:
        usual_speeding_rate = st.slider("Usual speeding rate (%)", 5, 50, 20, key="usual_speeding_rate")
        cars_observed = st.slider("Number of cars observed", 50, 500, 100, key="cars_observed")
        speeders_observed = st.slider("Number of speeders observed", 0, cars_observed, 25, key="speeders_observed")
        alpha = st.select_slider("Significance Level (α)", options=[0.01, 0.05, 0.1], value=0.05, key="alpha_2")

        # Calculate p-value using binomial test
        p_value = 1 - stats.binom.cdf(speeders_observed - 1, cars_observed, usual_speeding_rate / 100)

        st.write(f"p-value: {p_value:.4f}")
        
        if p_value < alpha:
            st.error("Reject H₀ (Evidence suggests speeding has increased)")
        else:
            st.success("Fail to reject H₀ (Not enough evidence to conclude speeding has increased)")

    with col2:
        x = np.linspace(0, cars_observed, 1000)
        y = stats.norm.pdf(x, cars_observed * usual_speeding_rate / 100, np.sqrt(cars_observed * usual_speeding_rate / 100 * (1 - usual_speeding_rate / 100)))

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Speeding Distribution', line=dict(color='blue', width=2)))

        critical_value = stats.norm.ppf(1-alpha, cars_observed * usual_speeding_rate / 100, np.sqrt(cars_observed * usual_speeding_rate / 100 * (1 - usual_speeding_rate / 100)))

        fig.add_trace(go.Scatter(
            x=np.concatenate([x[x <= critical_value], [critical_value]]),
            y=np.concatenate([y[x <= critical_value], [0]]),
            fill='tozeroy', fillcolor='rgba(0,255,0,0.3)', line_color='rgba(255,255,255,0)',
            name='Fail to Reject H₀'
        ))

        fig.add_trace(go.Scatter(
            x=np.concatenate([[critical_value], x[x > critical_value]]),
            y=np.concatenate([[0], y[x > critical_value]]),
            fill='tozeroy', fillcolor='rgba(255,0,0,0.3)', line_color='rgba(255,255,255,0)',
            name='Reject H₀'
        ))

        fig.add_vline(x=speeders_observed, line_dash="dash", line_color="black", 
                      annotation_text="Observed Speeders", annotation_position="top right")

        fig.add_vline(x=critical_value, line_dash="dash", line_color="red", 
                      annotation_text=f"Critical Value (α={alpha})", annotation_position="bottom right")

        fig.add_annotation(x=cars_observed/4, y=max(y), text="H₀: No Increase", showarrow=False, yshift=10)
        fig.add_annotation(x=3*cars_observed/4, y=max(y), text="H₁: Speeding Increased", showarrow=False, yshift=10)
        fig.add_annotation(x=cars_observed/8, y=max(y)/2, text="Type II Error (β)", showarrow=False)
        fig.add_annotation(x=7*cars_observed/8, y=max(y)/2, text="Type I Error (α)", showarrow=False)

        fig.update_layout(
            title='Distribution of Speeders',
            xaxis_title='Number of Speeders',
            yaxis_title='Probability Density',
            height=600,
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)

    st.write("""
    How to interpret this:
    - H₀ (Null Hypothesis): The speeding rate hasn't increased
    - H₁ (Alternative Hypothesis): The speeding rate has increased
    - The blue curve shows the expected distribution of speeders if H₀ is true
    - The green area is where we fail to reject H₀ (not enough evidence of increased speeding)
    - The red area is where we reject H₀ (strong evidence suggesting increased speeding)
    - α (alpha) is the significance level, representing the Type I error rate
    - β (beta) represents the Type II error rate (not directly shown)
    - The black line shows the observed number of speeders
    - If the black line is in the red area, we reject H₀ (conclude speeding has increased)
    """)

with tab4:
    st.header("Quick Quiz")
    
    q1 = st.radio("1. What does a small p-value suggest?", 
        ("Strong evidence for H₀", "Strong evidence against H₀", "No conclusion possible"), key="q1")
    if st.button("Check", key="b1"):
        if q1 == "Strong evidence against H₀":
            st.success("Correct! A small p-value suggests strong evidence against the null hypothesis.")
        else:
            st.error("Not quite. Think about what a small probability means in terms of the null hypothesis.")
    
    q2 = st.radio("2. Why do we set a low significance level (α) in hypothesis testing?", 
        ("To increase the chance of rejecting H₀", "To protect against false positives", "To make calculations easier"), key="q2")
    if st.button("Check", key="b2"):
        if q2 == "To protect against false positives":
            st.success("Correct! A low α reduces the chance of Type I errors (false positives).")
        else:
            st.error("Think about the consequences of wrongly rejecting the null hypothesis.")
    
    q3 = st.radio("3. What does 'fail to reject H₀' mean?", 
        ("H₀ is definitely true", "H₁ is definitely true", "There isn't enough evidence to conclude H₁"), key="q3")
    if st.button("Check", key="b3"):
        if q3 == "There isn't enough evidence to conclude H₁":
            st.success("Correct! 'Fail to reject H₀' means we don't have enough evidence to support H₁, not that H₀ is definitely true.")
        else:
            st.error("Remember, we start with H₀ and only reject it if we have strong evidence against it.")

st.markdown("---")

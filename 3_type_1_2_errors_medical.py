import streamlit as st
import plotly.graph_objects as go
import numpy as np
from scipy import stats

# Set page config
st.set_page_config(layout="wide", page_title="Type I and Type II Errors in Medical Diagnosis", page_icon="🏥")

# Custom CSS
st.markdown("""
<style>
    .main {max-width: 1200px; margin: 0 auto;}
    .stApp {padding-top: 2rem;}
    .st-emotion-cache-10trblm {text-align: center;}
    .info-box {background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px;}
    .quiz-container {background-color: #e1e5eb; padding: 20px; border-radius: 10px; margin-top: 20px;}
    .example-box {border: 1px solid #4CAF50; padding: 10px; border-radius: 5px; margin-bottom: 10px;}
</style>
""", unsafe_allow_html=True)

# Title and introduction
st.title("🏥 Type I and Type II Errors in Medical Diagnosis")
st.markdown("""
This interactive demo explores Type I and Type II errors in the context of cancer diagnosis.
Understand these concepts through examples, visualizations, and a quiz!
""")

# Sidebar navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Choose a section", ["Concept Explanation", "Interactive Visualization", "Quiz"])

if page == "Concept Explanation":
    st.header("Understanding Type I and Type II Errors")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Type I Error (False Positive)")
        st.markdown("""
        <div class="example-box">
        <strong>Definition:</strong> Rejecting a true null hypothesis
        <br><strong>In our example:</strong> Diagnosing cancer when the patient doesn't have it
        <br><strong>Consequence:</strong> Unnecessary treatment, anxiety, and medical costs
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.subheader("Type II Error (False Negative)")
        st.markdown("""
        <div class="example-box">
        <strong>Definition:</strong> Failing to reject a false null hypothesis
        <br><strong>In our example:</strong> Not diagnosing cancer when the patient actually has it
        <br><strong>Consequence:</strong> Delayed treatment, potentially worse prognosis
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <h3>Key Concepts in Medical Testing</h3>
    <ul>
        <li><strong>Sensitivity:</strong> The ability of a test to correctly identify patients with the disease (True Positive Rate)</li>
        <li><strong>Specificity:</strong> The ability of a test to correctly identify patients without the disease (True Negative Rate)</li>
        <li><strong>Prevalence:</strong> The proportion of the population that has the disease</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Formulas")
    st.latex(r"\text{Sensitivity} = \frac{\text{True Positives}}{\text{True Positives} + \text{False Negatives}}")
    st.latex(r"\text{Specificity} = \frac{\text{True Negatives}}{\text{True Negatives} + \text{False Positives}}")
    st.latex(r"\text{Type I Error Rate} = 1 - \text{Specificity}")
    st.latex(r"\text{Type II Error Rate} = 1 - \text{Sensitivity}")

elif page == "Interactive Visualization":
    st.header("Interactive Medical Test Simulator")
    
    # Parameters
    prevalence = st.slider("Disease Prevalence (%)", 0.1, 20.0, 5.0, 0.1) / 100
    sensitivity = st.slider("Test Sensitivity (%)", 50.0, 99.9, 90.0, 0.1) / 100
    specificity = st.slider("Test Specificity (%)", 50.0, 99.9, 95.0, 0.1) / 100
    
    population = 10000
    
    # Calculate outcomes
    true_positives = prevalence * population * sensitivity
    false_negatives = prevalence * population * (1 - sensitivity)
    false_positives = (1 - prevalence) * population * (1 - specificity)
    true_negatives = (1 - prevalence) * population * specificity
    
    # Create confusion matrix
    confusion_matrix = go.Figure(data=[go.Table(
        header=dict(values=['', 'Test Positive', 'Test Negative'],
                    fill_color='paleturquoise',
                    align='center'),
        cells=dict(values=[['Actually Positive', 'Actually Negative'],
                           [f'{true_positives:.0f}', f'{false_positives:.0f}'],
                           [f'{false_negatives:.0f}', f'{true_negatives:.0f}']],
                   fill_color=[['lightcyan', 'lightcyan'],
                               ['lightgreen', 'tomato'],
                               ['tomato', 'lightgreen']],
                   align='center'))
    ])
    confusion_matrix.update_layout(width=500, height=300, margin=dict(l=40, r=40, t=20, b=20))
    
    st.plotly_chart(confusion_matrix)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Type I Error Rate", f"{(1 - specificity):.2%}")
        st.metric("False Positive Cases", f"{false_positives:.0f}")
    
    with col2:
        st.metric("Type II Error Rate", f"{(1 - sensitivity):.2%}")
        st.metric("False Negative Cases", f"{false_negatives:.0f}")
    
    st.markdown("""
    <div class="info-box">
    <h3>Interpretation</h3>
    <ul>
        <li>Green cells represent correct diagnoses</li>
        <li>Red cells represent errors (Type I and Type II)</li>
        <li>Adjust the sliders to see how changing parameters affects the outcomes</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

elif page == "Quiz":
    st.header("Test Your Understanding")
    
    st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
    
    q1 = st.radio(
        "1. In the context of cancer diagnosis, what is a Type I error?",
        ["Diagnosing cancer when the patient doesn't have it", "Not diagnosing cancer when the patient has it", "Correctly diagnosing cancer", "Correctly identifying a patient without cancer"]
    )
    
    q2 = st.radio(
        "2. Which of the following would reduce the Type II error rate in a medical test?",
        ["Increasing specificity", "Decreasing sensitivity", "Increasing sensitivity", "Decreasing prevalence"]
    )
    
    q3 = st.radio(
        "3. If a test has high specificity but low sensitivity, which type of error is more likely?",
        ["Type I error (false positive)", "Type II error (false negative)", "Both errors are equally likely", "Neither error is likely"]
    )
    
    if st.button("Check Answers"):
        score = 0
        
        if q1 == "Diagnosing cancer when the patient doesn't have it":
            st.success("Question 1: Correct!")
            score += 1
        else:
            st.error("Question 1: Incorrect")
        st.markdown("""
        Explanation: A Type I error occurs when we reject a true null hypothesis. In this case, it means 
        diagnosing cancer (rejecting the null hypothesis that the patient doesn't have cancer) when the 
        patient actually doesn't have cancer.
        """)
        
        if q2 == "Increasing sensitivity":
            st.success("Question 2: Correct!")
            score += 1
        else:
            st.error("Question 2: Incorrect")
        st.markdown("""
        Explanation: Sensitivity is the ability of a test to correctly identify patients with the disease. 
        Increasing sensitivity reduces the false negative rate, which is equivalent to the Type II error rate.
        """)
        
        if q3 == "Type II error (false negative)":
            st.success("Question 3: Correct!")
            score += 1
        else:
            st.error("Question 3: Incorrect")
        st.markdown("""
        Explanation: High specificity means the test is good at correctly identifying patients without the disease, 
        reducing Type I errors. Low sensitivity means the test is not as good at identifying patients with the disease, 
        increasing the likelihood of Type II errors (false negatives).
        """)
        
        st.subheader(f"Your score: {score}/3")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("© 2024 Type I and Type II Errors in Medical Diagnosis. Created with Streamlit and Plotly.")
import streamlit as st
from dotenv import load_dotenv
import os
from PIL import Image
from llm.Brain import get_ai_crtique
import altair as alt
import pandas as pd
import numpy as np
from Visualisation.Graph import plot_pie_chart
import matplotlib.pyplot as plt


load_dotenv()

st.title("The Design Critique")
image = st.file_uploader("Upload Your Design Here", type = ["png", "jpg", "jpeg"])

if image is not None:
    Design = Image.open(image)
    st.image(Design, caption = "Your Design", width = 300)

    if "button1_clicked" not in st.session_state:
        st.session_state.button1_clicked = False

    if st.button("Get Feedback"):
        st.session_state.button1_clicked = True
        with st.spinner("Analyzing your design..."):
            feedback = get_ai_crtique(Design)
            scores_data = feedback["critique_scores"]
            st.session_state.critique_data = feedback
# Get the keys (categories) and scores (values) from the nested dictionary
        categories = [key.replace('_', ' ').title() for key in scores_data.keys()] # Clean up keys for chart labels
        scores = [scores_data[key]["score"] for key in scores_data.keys()]

# Ensure the list of categories closes the circle for the radar chart
        categories.append(categories[0]) 
        scores.append(scores[0])
        # st.write(feedback)



        if 'critique_data' in st.session_state:
            critique_data = st.session_state.critique_data
            overall_score = critique_data['overall_score']

            
            # Use a container or columns for the main content
            st.header("Design Analysis")
            
            col_img, col_score = st.columns([0.6, 0.4]) # 60% width for image/chart, 40% for score/suggestion
            
            with col_score:
                # Display the overall score prominently
                st.metric(
                    label="Overall Design Grade", 
                    value=f"{overall_score:.2f}/10", 
                    delta="AI Generated Score",
                    
                     # Optional descriptive text
                    delta_color="normal"
                )
                st.subheader("What to Change?")
            if st.session_state.button1_clicked:

                st.subheader("Color Usage")
                st.write("Score:")
                st.info(critique_data['critique_scores']['color_palette']['score'])
                st.info(critique_data['critique_scores']['color_palette']['critique'])

                st.subheader("Typography")
                st.write("Score:")
                st.info(critique_data['critique_scores']['typography']['score'])
                st.info(critique_data['critique_scores']['typography']['critique'])

                st.subheader("Layout and Balance")
                st.write("Score:")
                st.info(critique_data['critique_scores']['layout_and_balance']['score'])
                st.info(critique_data['critique_scores']['layout_and_balance']['critique'])

                st.subheader("Concept and Originality")
                st.write("Score:")
                st.info(critique_data['critique_scores']['concept_and_originality']['score'])
                st.info(critique_data['critique_scores']['concept_and_originality']['critique'])

                st.subheader("Overall Actionable Suggestion")
                st.write(critique_data['actionable_suggestion'])
                
                

                
            with col_img:
                
                

# 1. Prepare Your Data
                first = scores[0]%10
                second = scores[1]%10
                third = scores[2]%10
                fourth = scores[3]%10
                fifth = (10-(sum(scores)/5))%10

                values = [first, second, third, fourth, fifth]  # Assuming the last category is "Others" to make total 10

                # The labels for each slice
                categories = [categories[0], categories[1], categories[2], categories[3], 'Need Improvement']

                
                # 2. Create the Figure and Axes
                fig, ax = plt.subplots()

                # 3. Plot the Bar Chart (Horizontal)
                # Use ax.barh() for a horizontal chart
                ax.barh(categories, values, color='skyblue') # Added an optional color

                # 4. Customize the Chart (Note the flipped labels)
                ax.set_xlabel('Scores')
                ax.set_ylabel('Categories')
                ax.set_title('Design Critique Breakdown')

                # 5. Display the Chart
                st.pyplot(fig)

            























                # first = scores[0]%10
                # second = scores[1]%10
                # third = scores[2]%10
                # fourth = scores[3]%10
                # fifth = (10-(sum(scores)/5))%10
                # sizes = [first, second, third, fourth, fifth]  # Assuming the last category is "Others" to make total 10

                # # The labels for each slice
                # labels = [categories[0], categories[1], categories[2], categories[3], 'Need Improvement']

                # # Optional: Custom colors for the slices
                # colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']

                # # Optional: 'Explode' a slice to make it stand out (a list of values, where 0 means no explode)
                # # We will "explode" the largest slice (Rent)
                # explode = (0, 0, 0, 0, 0.1)

                # # Create the pie chart
                

                # fig, ax = plt.subplots(figsize=(6, 6)) 

                # # 3. Create the Pie Chart using the Axes object (ax)
                # ax.pie(
                #     sizes,
                #     explode=explode,
                #     labels=labels,
                #     colors=colors,
                #     autopct='%1.1f%%', # Format the percentage (e.g., 40.0%)
                #     # shadow=True,
                #     startangle=90
                # )

                # # 4. Ensure the pie chart is drawn as a circle (not an oval)
                # ax.axis('equal') 
                # ax.set_title('Design Critique Breakdown', fontsize=14)


                # # 5. Display the chart using st.pyplot()
                # # st.subheader("Your Pie Chart")
                # st.pyplot(fig)
                                            
                                    
import streamlit as st
import openai

st.set_page_config(
    page_title="AI Health & Fitness Planner",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)


def call_openai_api(prompt, api_key, model="gpt-4"):
    try:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert in health, fitness, and dietary planning."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ Error: {str(e)}"

def main():
    st.title("🏋️‍♂️ AI-Powered Health & Fitness Planner")

    
    with st.sidebar:
        st.header("🔑 API Configuration")
        openai_api_key = st.text_input(
            "Enter your OpenAI API Key",
            type="password",
            help="Input your OpenAI API key to enable the service."
        )

        if not openai_api_key:
            st.error(" Your API Key Missing!")
            st.stop()

    
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=10, max_value=100, step=1)
        weight = st.number_input("Weight (kg)", min_value=0.0, max_value=300.0, step=1.0)
        height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, step=0.1)
        activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
    with col2:
        sex = st.selectbox("Sex", ["Male", "Female", "Other"])
        dietary_preferences = st.selectbox("Dietary Preferences", ["Vegetarian", "Keto", "Gluten Free", "Low Carb", "Dairy Free"])
        fitness_goal = st.selectbox("Fitness Goals", ["Lose Weight", "Gain Muscle", "Endurance", "Stay Fit"])


    if st.button("🎯 Generate My Personalized Plan"):
        with st.spinner("Generating your health and fitness plans..."):
            user_profile = f"""
            Age: {age}
            Weight: {weight} kg
            Height: {height} cm
            Sex: {sex}
            Activity Level: {activity_level}
            Dietary Preferences: {dietary_preferences}
            Fitness Goal: {fitness_goal}
            """

            dietary_prompt = f"""
            Based on the following profile, create a personalized dietary plan:
            {user_profile}
            """
            dietary_plan = call_openai_api(dietary_prompt, openai_api_key)

            fitness_prompt = f"""
            Based on the following profile, create a personalized fitness plan:
            {user_profile}
            """
            fitness_plan = call_openai_api(fitness_prompt, openai_api_key)

      
        if dietary_plan and fitness_plan:
            st.markdown("### 🍽️ Dietary Plan")
            st.write(dietary_plan)

            st.markdown("### 🏋️ Fitness Plan")
            st.write(fitness_plan)
        else:
            st.error("❌ Failed to generate plans. Please try again.")

if __name__ == "__main__":
    main()

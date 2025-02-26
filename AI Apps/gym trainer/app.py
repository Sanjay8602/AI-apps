import streamlit as st
import google.generativeai as genai


genai.configure(api_key="YOUR_GEMINI_API_KEY") 



def generate_plan(goal, preferences, time_available):
    try:
        prompt = f"""
        You are a professional fitness trainer and dietician.
        My goal is: {goal}.
        My dietary preferences or restrictions are: {preferences}.
        I can work out for {time_available} minutes daily.
        Provide me with a detailed and personalized exercise plan and diet plan.
        """
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)

        if response and response.text:
            return response.text
        else:
            return "Sorry, I couldn't generate a plan. Please try again!"
    except Exception as e:
        return f"Error: {e}"


def main():
    st.set_page_config(page_title="AI Gym Trainer", layout="centered")


    st.title("🏋️‍♂️ AI Gym Trainer")
    st.write("Get a personalized **Diet Plan** and **Exercise Plan** based on your fitness goals!")


    with st.form("input_form"):
        goal = st.text_input("🎯 Your Fitness Goal:", placeholder="e.g., Lose weight, Build muscle, Stay fit")
        preferences = st.text_input("🥗 Dietary Preferences or Restrictions:", placeholder="e.g., Vegetarian, Vegan, Keto")
        time_available = st.number_input("⏳ Daily Workout Time (in minutes):", min_value=10, max_value=180, step=10)

        submitted = st.form_submit_button("Generate Plan")


    if submitted:
        if goal and preferences and time_available:
            st.info("Generating your personalized plan... ⏳")
            plan = generate_plan(goal, preferences, time_available)
            st.subheader("📝 Your Personalized Plan:")
            st.write(plan)
        else:
            st.warning("Please fill in all the fields to generate a plan.")


    st.markdown("---")
    st.markdown("**Created with ❤️ using Streamlit and Google Gemini API**")


if __name__ == "__main__":
    main()

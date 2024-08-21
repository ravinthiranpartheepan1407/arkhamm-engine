import streamlit as st
import urllib.request
import json
import os
import ssl

st.set_page_config(
    page_title="Arkhamm Fitness & Nutrition Sandbox"
)

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] > .main {
        background-color: 'black';
        color: 'white';
    }
    # [data-testid="stHeader"] {
    #     display: none;
    # }
    # [data-testid="stToolbar"] {
    #     display: none;
    # }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar menu
st.sidebar.title("Arkhamm Menu")
app_mode = st.sidebar.selectbox("Choose the app mode", ["Personalized Diet Plan", "Arkhamm Fitness LLM"])

# Function to allow self-signed HTTPS certificates
def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True)

# Arkhamm Fitness LLM app
def arkhamm_fitness_llm():
    st.title("Arkhamm Fitness LLM")
    api_key = st.text_input("Enter your API key:", type="password")
    prompt = st.text_area("Enter your prompt here:")

    if st.button("Process"):
        if not api_key:
            st.error("Please provide an API key.")
        elif not prompt:
            st.error("Enter your prompt.")
        elif not is_fitness_related(prompt):
            st.error("Irrelevant prompt.")
        else:
            with st.spinner('Processing...'):
                response = get_response(prompt, api_key)
                st.success("Done!")
                st.write("Response:")
                st.write(response)

# Function to check if the prompt is fitness-related
def is_fitness_related(prompt):
    fitness_keywords = [
        'bmi', 'weight loss', 'muscle gain', 'fitness', 'nutrition', 'diet', 'calories',
        'protein', 'carbohydrates', 'fats', 'workout', 'exercise', 'meal plan',
        'food allergy', 'belly fat', 'weight gain', 'goal duration', 'fitness goals'
    ]
    return any(keyword.lower() in prompt.lower() for keyword in fitness_keywords)

# Function to get response from Azure-based LLM
def get_response(prompt, api_key):
    data = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 1024,
        "temperature": 0.7,
        "top_p": 1,
        "stream": False
    }

    body = str.encode(json.dumps(data))

    url = 'https://Phi-3-small-8k-instruct-ygbal.eastus2.models.ai.azure.com/chat/completions'
    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        result_json = json.loads(result)
        return result_json['choices'][0]['message']['content']
    except urllib.error.HTTPError as error:
        return f"The request failed with status code: {error.code}\n{error.read().decode('utf8', 'ignore')}"

# Personalized Diet Plan app
def personalized_diet_plan():
    st.title("Personalized Diet Plan")

    if "current_screen" not in st.session_state:
        st.session_state.current_screen = 1

    if st.session_state.current_screen == 1:
        diet_screen1()
    elif st.session_state.current_screen == 2:
        diet_screen2()
    elif st.session_state.current_screen == 3:
        diet_screen3()
    elif st.session_state.current_screen == 4:
        diet_screen4()
    elif st.session_state.current_screen == 5:
        diet_screen5()
    elif st.session_state.current_screen == 6:
        process_diet_results()

def diet_screen1():
    st.header("Let's get started with your fitness goals")
    st.text("Please enter your personal information")

    st.session_state.age = st.number_input("Enter your age:", min_value=1, max_value=100, step=1)
    st.session_state.bmi = st.number_input("Enter your BMI:", min_value=10.0, max_value=50.0, step=0.1)
    st.session_state.health_condition = st.text_input("Enter any health conditions (comma separated):")
    st.session_state.food_allergies = st.text_input("Enter any food allergies (comma separated):")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("Back", on_click=go_to_screen, args=(st.session_state.current_screen - 1,))
    with col2:
        st.button("Next", on_click=go_to_screen, args=(st.session_state.current_screen + 1,))

def diet_screen2():
    st.header("What is your main fitness goal?")
    st.text("Select the goal that matters to you most. You can specify more details later.")

    goals = [
        "Belly fat loss", "Weight gain", "Muscle building", "Improving endurance", "Maintaining current weight"
    ]

    st.session_state.fitness_goal = st.radio("Choose your fitness goal", goals)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("Back", on_click=go_to_screen, args=(st.session_state.current_screen - 1,))
    with col2:
        st.button("Next", on_click=go_to_screen, args=(st.session_state.current_screen + 1,))

def diet_screen3():
    st.header("What is your target goal duration?")
    st.text("How long do you plan to achieve this goal?")

    st.session_state.goal_duration = st.slider("Choose your goal duration (in weeks):", min_value=1, max_value=52, value=12)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("Back", on_click=go_to_screen, args=(st.session_state.current_screen - 1,))
    with col2:
        st.button("Next", on_click=go_to_screen, args=(st.session_state.current_screen + 1,))

def diet_screen4():
    st.header("How often do you exercise per week?")
    st.text("This will help us customize your diet plan based on your activity level.")

    st.session_state.exercise_frequency = st.radio("Choose your exercise frequency", ["0-1 times", "2-3 times", "4-5 times", "6-7 times"])

    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("Back", on_click=go_to_screen, args=(st.session_state.current_screen - 1,))
    with col2:
        st.button("Next", on_click=go_to_screen, args=(st.session_state.current_screen + 1,))

def diet_screen5():
    st.header("Please provide details about your working hours")
    st.text("This will help us create a diet plan that fits into your daily routine.")

    st.session_state.working_hours = st.slider("Enter your working hours per day:", min_value=0, max_value=24, value=8)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("Back", on_click=go_to_screen, args=(st.session_state.current_screen - 1,))
    with col2:
        st.button("Next", on_click=go_to_screen, args=(st.session_state.current_screen + 1,))

def process_diet_results():
    st.header("Processing your personalized diet plan...")

    # Compile the answers from all screens
    answers = {
        "age": st.session_state.age,
        "bmi": st.session_state.bmi,
        "health_condition": st.session_state.health_condition,
        "food_allergies": st.session_state.food_allergies,
        "fitness_goal": st.session_state.fitness_goal,
        "goal_duration": st.session_state.goal_duration,
        "exercise_frequency": st.session_state.exercise_frequency,
        "working_hours": st.session_state.working_hours
    }

    # Generate the prompt
    prompt = f"""
    Based on the provided personal and fitness information, could you recommend a personalized diet plan including specific meals 
    for breakfast, mid-breakfast, lunch, mid-lunch, and dinner, with measured grams of food? Here are the details:
    - Age: {answers['age']}
    - BMI: {answers['bmi']}
    - Health conditions: {answers['health_condition']}
    - Food allergies: {answers['food_allergies']}
    - Fitness goal: {answers['fitness_goal']}
    - Goal duration: {answers['goal_duration']} weeks
    - Exercise frequency: {answers['exercise_frequency']}
    - Working hours: {answers['working_hours']} hours/day
    """

    api_key = st.text_input("Enter your API key:", type="password")

    if api_key:
        with st.spinner("Getting your personalized diet plan..."):
            response = get_response(prompt, api_key)
            st.success("Here is your personalized diet plan!")
            st.write(response)
    else:
        st.error("API key missing. Please provide your API key in the Arkhamm Fitness LLM section.")

# Function to handle screen navigation
def go_to_screen(screen_number):
    st.session_state.current_screen = screen_number

# Main app logic
if app_mode == "Arkhamm Fitness LLM":
    arkhamm_fitness_llm()
else:
    personalized_diet_plan()

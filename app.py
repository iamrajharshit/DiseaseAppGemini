import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
from dotenv import load_dotenv
load_dotenv()
key = os.getenv("API_KEY")
#LLM part#############################################################################################
import google.generativeai as genai
def ask_order(message,Profile_prompt):
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-pro',safety_settings=[
        {"category":'HARM_CATEGORY_HARASSMENT',
                            "threshold":'BLOCK_NONE'},
                            {"category":'HARM_CATEGORY_DANGEROUS_CONTENT',
                            "threshold":'BLOCK_NONE'},
                            {"category":'HARM_CATEGORY_HATE_SPEECH',
                            "threshold":'BLOCK_NONE'}
    ])
    chat = model.start_chat(history=[])
    # we can add pre prompt
    response=chat.send_message(Profile_prompt) #first we share the profile
    response=chat.send_message(message,generation_config=genai.types.GenerationConfig(candidate_count=1,
                                                                                        temperature=0.3))
    return response.text
###################################################################################################
st.set_page_config(page_title="Health Assistant",
                   layout="wide",
                   page_icon="🧑‍⚕️")

    
working_dir = os.path.dirname(os.path.abspath(__file__))



diabetes_model = pickle.load(open(f'{working_dir}/saved_models/diabetes_model.sav', 'rb'))

heart_disease_model = pickle.load(open(f'{working_dir}/saved_models/heart_disease_model.sav', 'rb'))

parkinsons_model = pickle.load(open(f'{working_dir}/saved_models/parkinsons_model.sav', 'rb'))


with st.sidebar:
    selected = option_menu('Multiple Disease Prediction System',

                           ['Diabetes Prediction',
                            'Heart Disease Prediction',
                            'Parkinsons Prediction'],
                           menu_icon='hospital-fill',
                           icons=['activity', 'heart', 'person'],
                           default_index=0)


# Diabetes Prediction Page
if selected == 'Diabetes Prediction':

    
    st.title('Diabetes Prediction using ML')

   
    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.text_input('Number of Pregnancies')

    with col2:
        Glucose = st.text_input('Glucose Level')

    with col3:
        BloodPressure = st.text_input('Blood Pressure value')

    with col1:
        SkinThickness = st.text_input('Skin Thickness value')

    with col2:
        Insulin = st.text_input('Insulin Level')

    with col3:
        BMI = st.text_input('BMI value')

    with col1:
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')

    with col2:
        Age = st.text_input('Age of the Person')

    #added for llm
    user_diab_prompt=f"The person medical report with data, Number of Pregnancies={Pregnancies},Glucose Level={Glucose},Blood Pressure value={BloodPressure},Skin Thickness value={SkinThickness},Insulin Level={Insulin},BMI value={BMI},Diabetes Pedigree Function value={DiabetesPedigreeFunction},Age of the Person={Age}"
    
    diab_diagnosis = ''

    

    if st.button('Diabetes Test Result'):

        user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin,
                      BMI, DiabetesPedigreeFunction, Age]

        user_input = [float(x) for x in user_input]

        diab_prediction = diabetes_model.predict([user_input])

        if diab_prediction[0] == 1:
            diab_diagnosis = 'The person is diabetic'
            
        else:
            diab_diagnosis = 'The person is not diabetic'

    st.success(diab_diagnosis)
    st.title('Report')
    st.markdown(ask_order(diab_diagnosis,user_diab_prompt))
    

# Heart Disease Prediction Page
if selected == 'Heart Disease Prediction':

    # page title
    st.title('Heart Disease Prediction using ML')

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.text_input('Age')

    with col2:
        sex = st.text_input('Sex')

    with col3:
        cp = st.text_input('Chest Pain types')

    with col1:
        trestbps = st.text_input('Resting Blood Pressure')

    with col2:
        chol = st.text_input('Serum Cholestoral in mg/dl')

    with col3:
        fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')

    with col1:
        restecg = st.text_input('Resting Electrocardiographic results')

    with col2:
        thalach = st.text_input('Maximum Heart Rate achieved')

    with col3:
        exang = st.text_input('Exercise Induced Angina')

    with col1:
        oldpeak = st.text_input('ST depression induced by exercise')

    with col2:
        slope = st.text_input('Slope of the peak exercise ST segment')

    with col3:
        ca = st.text_input('Major vessels colored by flourosopy')

    with col1:
        thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect')

    User_Heart_prompt="The person medical report with data, Age={age}, Sex={sex}, Chest Pain types={cp}, Resting Blood Pressure={trestbps}, Serum Cholestoral in mg/dl={chol}, Fasting Blood Sugar > 120 mg/dl={fbs}, Maximum Heart Rate achieved={thalach}, Exercise Induced Angina={exang}, ST depression induced by exercise{oldpeak}, Slope of the peak exercise ST segment={slope}, Major vessels colored by flourosopy={ca}, thal: 0 = normal; 1 = fixed defect; 2 = reversable defect, here thal={thal}"

    heart_diagnosis = ''


    

    if st.button('Heart Disease Test Result'):

        user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]

        user_input = [float(x) for x in user_input]

        heart_prediction = heart_disease_model.predict([user_input])

        if heart_prediction[0] == 1:
            heart_diagnosis = 'The person is having heart disease'
            
        else:
            heart_diagnosis = 'The person does not have any heart disease'

    st.success(heart_diagnosis)
    st.title('Report')
    st.markdown(ask_order(heart_diagnosis,User_Heart_prompt)) #llm reply

# Parkinson's Prediction Page
if selected == "Parkinsons Prediction":

    
    st.title("Parkinson's Disease Prediction using ML")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        fo = st.text_input('MDVP:Fo(Hz)')

    with col2:
        fhi = st.text_input('MDVP:Fhi(Hz)')

    with col3:
        flo = st.text_input('MDVP:Flo(Hz)')

    with col4:
        Jitter_percent = st.text_input('MDVP:Jitter(%)')

    with col5:
        Jitter_Abs = st.text_input('MDVP:Jitter(Abs)')

    with col1:
        RAP = st.text_input('MDVP:RAP')

    with col2:
        PPQ = st.text_input('MDVP:PPQ')

    with col3:
        DDP = st.text_input('Jitter:DDP')

    with col4:
        Shimmer = st.text_input('MDVP:Shimmer')

    with col5:
        Shimmer_dB = st.text_input('MDVP:Shimmer(dB)')

    with col1:
        APQ3 = st.text_input('Shimmer:APQ3')

    with col2:
        APQ5 = st.text_input('Shimmer:APQ5')

    with col3:
        APQ = st.text_input('MDVP:APQ')

    with col4:
        DDA = st.text_input('Shimmer:DDA')

    with col5:
        NHR = st.text_input('NHR')

    with col1:
        HNR = st.text_input('HNR')

    with col2:
        RPDE = st.text_input('RPDE')

    with col3:
        DFA = st.text_input('DFA')

    with col4:
        spread1 = st.text_input('spread1')

    with col5:
        spread2 = st.text_input('spread2')

    with col1:
        D2 = st.text_input('D2')

    with col2:
        PPE = st.text_input('PPE')

    
    user_parkinsons_diagnosis = f''

    Parkinsons_prompt="The person medical report with data, Average vocal fundamental frequency={fo}, Maximum vocal fundamental frequency={fhi},Minimum vocal fundamental frequency={flo},Three nonlinear measures of fundamental frequency variation PPE={PPE} spread1={spread1} spread2={spread2},Two nonlinear dynamical complexity measures={D2} RPDE={RPDE},MDVP:Jitter(Abs)={Jitter_Abs}"
   
    if st.button("Parkinson's Test Result"):

        user_input = [fo, fhi, flo, Jitter_percent, Jitter_Abs,
                      RAP, PPQ, DDP,Shimmer, Shimmer_dB, APQ3, APQ5,
                      APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]

        user_input = [float(x) for x in user_input]

        parkinsons_prediction = parkinsons_model.predict([user_input])

        if parkinsons_prediction[0] == 1:
            parkinsons_diagnosis = "The person has Parkinson's disease"
           
        else:
            parkinsons_diagnosis = "The person does not have Parkinson's disease"

        

    st.success(parkinsons_diagnosis)
    #added chat bot
    st.title('Report')
    st.markdown(ask_order(parkinsons_diagnosis,user_parkinsons_diagnosis))

    
#chat convo part
# if selected == 'Diabetes Prediction':
#     pass

# if selected == 'Heart Disease Prediction':
#     pass

# if selected == "Parkinsons Prediction":
#     pass


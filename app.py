import streamlit as st
import pandas as pd
import pickle 
from sklearn.ensemble import RandomForestClassifier 
from sklearn.preprocessing import StandardScaler,LabelEncoder


st.set_page_config(page_title="Loan Status Prediction",page_icon=":moneybag:",layout="wide")

@st.cache_data

def load_model():
    with open ('model/model.pkl','rb') as file:
        model = pickle.load(file)
    
    with open ('model/scaler.pkl','rb') as file:
        scaler = pickle.load(file)
        
    return model,scaler

model,scaler  = load_model()

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #2c2f33;
        color: #ffffff;
    }
    .sidebar .sidebar-content {
        background-color: #23272a;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
    }
    .st-bk {
        background-color: #2e2e2e;
        color: #ffffff;
        border: 1px solid #4CAF50;
        border-radius: 5px;
        padding: 5px;
        margin-bottom: 10px;
    }
    .st-markdown h3, .st-markdown h4 {
        color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)



st.title("Loan Status Prediction")
st.write("""
This loan status prediction tool helps you determine the likelihood of your loan application being approved based on various personal and financial factors. 
Simply fill in the details on the left sidebar, and click the 'Predict Loan Status' button to see the result.
""")
st.markdown("---")


st.sidebar.header('LOAN APP INPUTS')
st.sidebar.title("User Input Features")

def user_input_features():

    st.sidebar.markdown("### Personal Information")
    Gender = st.sidebar.selectbox('Gender',['Male','Female'])
    Married = st.sidebar.selectbox('Married',['Yes','No'])
   


    st.sidebar.markdown("### Property Information")
    Property_Area = st.sidebar.selectbox('Property_Area',['Rural','Semiurban','Urban'])
    

    st.sidebar.markdown("### Financial Information")
    ApplicantIncome = st.sidebar.slider('ApplicantIncome',min_value=0,max_value = 100000,value= 5000,step = 1000)
    CoapplicantIncome = st.sidebar.slider('CoapplicantIncome',min_value=0,max_value = 50000, value=2000, step = 500)
    LoanAmount = st.sidebar.slider('LoanAmount',min_value=0,max_value = 500,value=100,step = 10)
    Credit_History = st.sidebar.selectbox('Credit_History',[0.0,1.0])
    LoanTerm = st.sidebar.slider('LoanTerm',min_value=0,max_value = 480,value=360, step = 12)
    
    data = ({'Gender':Gender, 'Married':Married,  'Property_Area':Property_Area,
              'ApplicantIncome':ApplicantIncome, 'CoapplicantIncome':CoapplicantIncome, 'LoanAmount':LoanAmount,
       'Credit_History':Credit_History, 'LoanTerm':LoanTerm})
    
    features = pd.DataFrame(data,index=[0])

    label_encoder = {'Gender': LabelEncoder().fit(['Male','Female']),
                     'Married':LabelEncoder().fit(['Yes','No']),
                     'Property_Area':LabelEncoder().fit(['Rural','Semiurban','Urban'])}
    
    for colunm,le in label_encoder.items():
        features[colunm] = le.transform(features[colunm])

    
    num_cols = ['ApplicantIncome','CoapplicantIncome','LoanAmount','LoanTerm']
    features[num_cols] = scaler.transform(features[num_cols])
    
    return features



df = user_input_features()

expected_columns = ['Gender', 'Married','Property_Area',
'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
'Credit_History', 'LoanTerm',]


df = df[expected_columns]

st.subheader('User Input parameters')
st.write(df)

st.subheader('Prediction')
button = st.button ('Predict Loan Status')

if button:
    prediction = model.predict(df)
    if prediction == 1:
        st.success('Loan is approved')
        st.write('You are eligible for the Loan')
        st.ballon()
    else:
        st.error('Loan is not approved')
        st.write('you are in eligible for the loan')
        st.snow()




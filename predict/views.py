from django.shortcuts import get_object_or_404, render
import pandas as pd
import random 
from django.contrib import messages
import pickle

from .models import Symptom, Disease
# Create your views here.

# causing some problem in prediction
""" def automate_predicted_checking(result, test_input_features):
    df_train = pd.read_csv("ml_model/data/splitted_train_first.csv")
    predicted_disease_dict = {}
    for r in result:
        symptoms_lst = list()
        for i in range(df_train.shape[0]):  
            if df_train.iloc[i,-1]==r[0]: 
                for j in range(df_train.shape[1]):
                        if df_train.iloc[i,j]==1: 
                            symptoms_lst.append(df_train.columns[j]) 
                break
        predicted_disease_dict[r[0]] = symptoms_lst 
        
    predicted_disease_precent_dict = {}
    for name,feats in predicted_disease_dict.items():
        similar_count = 0
        for symptom in test_input_features:
            if symptom in feats:
                similar_count+=1 
        predicted_disease_precent_dict[name] = round(similar_count*100/len(feats), 3) 
    # print(predicted_disease_precent_dict)
    return sorted(predicted_disease_precent_dict.items(), key=lambda x: x[1], reverse=True)  """


def make_prediction(user_symptoms):
    symptom_list =  ["itching","skin_rash","nodal_skin_eruptions","dischromic _patches","continuous_sneezing","shivering","chills","watering_from_eyes","stomach_pain","acidity","ulcers_on_tongue","vomiting","cough","chest_pain","yellowish_skin","nausea","loss_of_appetite","abdominal_pain","yellowing_of_eyes","burning_micturition","spotting_ urination","passage_of_gases","internal_itching","indigestion","muscle_wasting","patches_in_throat","high_fever","extra_marital_contacts","fatigue","weight_loss","restlessness","lethargy","irregular_sugar_level","blurred_and_distorted_vision","obesity","excessive_hunger","increased_appetite","polyuria","sunken_eyes","dehydration","diarrhoea","breathlessness","family_history","mucoid_sputum","headache","dizziness","loss_of_balance","lack_of_concentration","stiff_neck","depression","irritability","visual_disturbances","back_pain","weakness_in_limbs","neck_pain","weakness_of_one_body_side","altered_sensorium","dark_urine","sweating","muscle_pain","mild_fever","swelled_lymph_nodes","malaise","red_spots_over_body","joint_pain","pain_behind_the_eyes","constipation","toxic_look_(typhos)","belly_pain","yellow_urine","receiving_blood_transfusion","receiving_unsterile_injections","coma","stomach_bleeding","acute_liver_failure","swelling_of_stomach","distention_of_abdomen","history_of_alcohol_consumption","fluid_overload","phlegm","blood_in_sputum","throat_irritation","redness_of_eyes","sinus_pressure","runny_nose","congestion","loss_of_smell","fast_heart_rate","rusty_sputum","pain_during_bowel_movements","pain_in_anal_region","bloody_stool","irritation_in_anus","cramps","bruising","swollen_legs","swollen_blood_vessels","prominent_veins_on_calf","weight_gain","cold_hands_and_feets","mood_swings","puffy_face_and_eyes","enlarged_thyroid","brittle_nails","swollen_extremeties","abnormal_menstruation","muscle_weakness","anxiety","slurred_speech","palpitations","drying_and_tingling_lips","knee_pain","hip_joint_pain","swelling_joints","painful_walking","movement_stiffness","spinning_movements","unsteadiness","pus_filled_pimples","blackheads","scurring","bladder_discomfort","foul_smell_of urine","continuous_feel_of_urine","skin_peeling","silver_like_dusting","small_dents_in_nails","inflammatory_nails","blister","red_sore_around_nose","yellow_crust_ooze"]

    input_data = []
    for symptom in symptom_list:
        if symptom in user_symptoms:
            input_data.append(1)
        else:
            input_data.append(0)
    # print(input_data)

    with open('ml_model/final1_model.sav', 'rb') as f:
        model = pickle.load(f)
    prediction1 = model.predict([input_data])
    # print("------",prediction1, type(prediction1)) 
    return prediction1
    # return automate_predicted_checking(prediction1, user_symptoms)  
     
# --start----
def index(request):  
    
    predicted_disease_description = list()
    if request.method =="POST": 
        user_symptoms = []
        form_data = request.POST
        for i in form_data:
            if i!="csrfmiddlewaretoken" and form_data.get(i)!="none":
                user_symptoms.append(form_data.get(i)) 
        predicted_disease= "" 
        if len(user_symptoms)==0:
            predicted_disease = "No Symptom!"
            messages.success(request, "No Symptom!")
        # elif len(user_symptoms)<=2:
        #     messages.success(request, "Select more than two symtpoms for prediction.")
        else:
            prediction2 = make_prediction(user_symptoms) 
            print(prediction2)

            for p in prediction2:
                disease = Disease.objects.get(name = p[0])
                predicted_disease_description.append({ "id":disease.id, "name":disease.name, "description":disease.description,"percentage":p[1] }) 
    else:
        disease_list = Disease.objects.all()
        id_lst = list()
        for i in disease_list:
            id_lst.append(i.id)
        for i in range(6): 
            disease = Disease.objects.get(id=random.choice(id_lst))
            predicted_disease_description.append({ "id":disease.id, "prevention": disease.prevention, "name":disease.name, "description":disease.description, "percentage":100})
   
    symptom_list = Symptom.objects.all().order_by("name") 
    return render(request, 'predict/index.html', {
        'symptom_list': symptom_list,
        'predicted_disease_description': predicted_disease_description
    })


def disease_detail(request, id):
    disease = get_object_or_404(Disease, id=id) 
    return render(request, "predict/detail.html", {
        "disease": disease
    })



""" 
# Used for creating disease dataset
    df = pd.read_csv("ml_model/data/disease_description.csv")
    for i in range(df.shape[0]):
        Disease.objects.create(name = df.loc[i,'Disease'].strip(), description= df.loc[i,'Description']) 

    # used to create symptom data
    symptom_list =  ["itching", "skin_rash", "nodal_skin_eruptions", "continuous_sneezing", "shivering", "chills", "joint_pain", "stomach_pain", "acidity", "ulcers_on_tongue", "muscle_wasting", "vomiting", "burning_micturition", "spotting_ urination", "fatigue", "weight_gain", "anxiety", "cold_hands_and_feets", "mood_swings", "weight_loss", "restlessness", "lethargy", "patches_in_throat", "irregular_sugar_level", "cough", "high_fever", "sunken_eyes", "breathlessness", "sweating", "dehydration", "indigestion", "headache", "yellowish_skin", "dark_urine", "nausea", "loss_of_appetite", "pain_behind_the_eyes", "back_pain", "constipation", "abdominal_pain", "diarrhoea", "mild_fever", "yellow_urine", "yellowing_of_eyes", "acute_liver_failure", "swelling_of_stomach", "swelled_lymph_nodes", "malaise", "blurred_and_distorted_vision", "phlegm", "throat_irritation", "redness_of_eyes", "sinus_pressure", "runny_nose", "congestion", "chest_pain", "weakness_in_limbs", "fast_heart_rate", "pain_during_bowel_movements", "pain_in_anal_region", "bloody_stool", "irritation_in_anus", "neck_pain", "dizziness", "cramps", "bruising", "obesity", "swollen_legs", "swollen_blood_vessels", "puffy_face_and_eyes", "enlarged_thyroid", "brittle_nails", "swollen_extremeties", "excessive_hunger", "extra_marital_contacts", "drying_and_tingling_lips", "slurred_speech", "knee_pain", "hip_joint_pain", "muscle_weakness", "stiff_neck", "swelling_joints", "movement_stiffness", "spinning_movements", "loss_of_balance", "unsteadiness", "weakness_of_one_body_side", "loss_of_smell", "bladder_discomfort", "foul_smell_of urine", "continuous_feel_of_urine", "passage_of_gases", "internal_itching", "toxic_look_(typhos)", "depression", "irritability", "muscle_pain", "altered_sensorium", "red_spots_over_body", "belly_pain", "abnormal_menstruation", "dischromic _patches", "watering_from_eyes", "increased_appetite", "polyuria", "family_history", "mucoid_sputum", "rusty_sputum", "lack_of_concentration", "visual_disturbances", "receiving_blood_transfusion", "receiving_unsterile_injections", "coma", "stomach_bleeding", "distention_of_abdomen", "history_of_alcohol_consumption", "fluid_overload", "blood_in_sputum", "prominent_veins_on_calf", "palpitations", "painful_walking", "pus_filled_pimples", "blackheads", "scurring", "skin_peeling", "silver_like_dusting", "small_dents_in_nails", "inflammatory_nails", "blister", "red_sore_around_nose", "yellow_crust_ooze"]

    for s in symptom_list:
        sy = Symptom(name= s)
        sy.save()

    # Used for disease ko symptom entry:
    b = {"(vertigo) Paroymsal  Positional Vertigo":['vomiting', 'nausea', 'headache', 'loss_of_balance', 'spinning_movements', 'unsteadiness'],"AIDS":['muscle_wasting', 'patches_in_throat', 'high_fever', 'extra_marital_contacts'],"Acne":['skin_rash', 'pus_filled_pimples', 'blackheads', 'scurring'],"Alcoholic hepatitis":['vomiting', 'yellowish_skin', 'abdominal_pain', 'swelling_of_stomach', 'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload'],"Allergy":['continuous_sneezing', 'shivering', 'chills', 'watering_from_eyes'],"Arthritis":['stiff_neck', 'muscle_weakness', 'swelling_joints', 'painful_walking', 'movement_stiffness'],"Bronchial Asthma":['cough', 'high_fever', 'fatigue', 'breathlessness', 'family_history', 'mucoid_sputum'],"Cervical spondylosis":['dizziness', 'loss_of_balance', 'back_pain', 'weakness_in_limbs', 'neck_pain'],"Chicken pox":['itching', 'skin_rash', 'loss_of_appetite', 'high_fever', 'fatigue', 'lethargy', 'headache', 'mild_fever', 'swelled_lymph_nodes', 'malaise', 'red_spots_over_body'],"Chronic cholestasis":['itching', 'vomiting', 'yellowish_skin', 'nausea', 'loss_of_appetite', 'abdominal_pain', 'yellowing_of_eyes'],"Common Cold":['continuous_sneezing', 'chills', 'cough', 'chest_pain', 'high_fever', 'fatigue', 'headache', 'muscle_pain', 'swelled_lymph_nodes', 'malaise', 'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'loss_of_smell'],"Dengue":['skin_rash', 'chills', 'vomiting', 'nausea', 'loss_of_appetite', 'high_fever', 'fatigue', 'headache', 'back_pain', 'muscle_pain', 'red_spots_over_body', 'joint_pain', 'pain_behind_the_eyes'],"Diabetes":['fatigue', 'weight_loss', 'restlessness', 'lethargy', 'irregular_sugar_level', 'blurred_and_distorted_vision', 'obesity', 'excessive_hunger', 'increased_appetite', 'polyuria'],"Dimorphic hemorrhoids(piles)":['constipation', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus'],"Drug Reaction":['itching', 'skin_rash', 'stomach_pain', 'burning_micturition', 'spotting_ urination'],"Fungal infection":['itching', 'skin_rash', 'nodal_skin_eruptions', 'dischromic _patches'],"GERD":['stomach_pain', 'acidity', 'ulcers_on_tongue', 'vomiting', 'cough', 'chest_pain'],"Gastroenteritis":['vomiting', 'sunken_eyes', 'dehydration', 'diarrhoea'],"Heart attack":['vomiting', 'chest_pain', 'breathlessness', 'sweating'],"Hepatitis B":['itching', 'yellowish_skin', 'loss_of_appetite', 'abdominal_pain', 'yellowing_of_eyes', 'fatigue', 'lethargy', 'dark_urine', 'malaise', 'yellow_urine', 'receiving_blood_transfusion', 'receiving_unsterile_injections'],"Hepatitis C":['yellowish_skin', 'nausea', 'loss_of_appetite', 'fatigue', 'family_history'],"Hepatitis D":['vomiting', 'yellowish_skin', 'nausea', 'loss_of_appetite', 'abdominal_pain', 'yellowing_of_eyes', 'fatigue', 'dark_urine', 'joint_pain'],"Hepatitis E":['vomiting', 'yellowish_skin', 'nausea', 'loss_of_appetite', 'abdominal_pain', 'yellowing_of_eyes', 'high_fever', 'fatigue', 'dark_urine', 'joint_pain', 'coma', 'stomach_bleeding'],"Hypertension":['chest_pain', 'headache', 'dizziness', 'loss_of_balance', 'lack_of_concentration'],"Hyperthyroidism":['fatigue', 'weight_loss', 'restlessness', 'excessive_hunger', 'diarrhoea', 'irritability', 'sweating', 'fast_heart_rate', 'mood_swings', 'abnormal_menstruation', 'muscle_weakness'],"Hypoglycemia":['vomiting', 'nausea', 'fatigue', 'blurred_and_distorted_vision', 'excessive_hunger', 'headache', 'irritability', 'sweating', 'anxiety', 'slurred_speech', 'palpitations'],"Hypothyroidism":['fatigue', 'lethargy', 'dizziness', 'depression', 'irritability', 'weight_gain', 'cold_hands_and_feets', 'mood_swings', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 'abnormal_menstruation'],"Impetigo":['skin_rash', 'high_fever', 'blister', 'red_sore_around_nose', 'yellow_crust_ooze'],"Jaundice":['itching', 'vomiting', 'yellowish_skin', 'abdominal_pain', 'high_fever', 'fatigue', 'weight_loss', 'dark_urine'],"Malaria":['chills', 'vomiting', 'nausea', 'high_fever', 'headache', 'sweating', 'muscle_pain'],"Migraine":['acidity', 'indigestion', 'blurred_and_distorted_vision', 'excessive_hunger', 'headache', 'stiff_neck', 'depression', 'irritability', 'visual_disturbances'],"Osteoarthristis":['neck_pain', 'joint_pain', 'knee_pain', 'hip_joint_pain', 'swelling_joints', 'painful_walking'],"Paralysis (brain hemorrhage)":['vomiting', 'headache', 'weakness_of_one_body_side', 'altered_sensorium'],"Peptic ulcer diseae":['vomiting', 'loss_of_appetite', 'abdominal_pain', 'passage_of_gases', 'internal_itching'],"Pneumonia":['chills', 'cough', 'chest_pain', 'high_fever', 'fatigue', 'breathlessness', 'sweating', 'malaise', 'fast_heart_rate', 'rusty_sputum'],"Psoriasis":['skin_rash', 'joint_pain', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails'],"Tuberculosis":['chills', 'vomiting', 'cough', 'chest_pain', 'loss_of_appetite', 'yellowing_of_eyes', 'high_fever', 'fatigue', 'weight_loss', 'breathlessness', 'sweating', 'mild_fever', 'swelled_lymph_nodes', 'malaise', 'phlegm', 'blood_in_sputum'],"Typhoid":['chills', 'vomiting', 'nausea', 'abdominal_pain', 'high_fever', 'fatigue', 'diarrhoea', 'constipation', 'toxic_look_(typhos)', 'belly_pain'],"Urinary tract infection":['burning_micturition', 'bladder_discomfort', 'foul_smell_of urine', 'continuous_feel_of_urine'],"Varicose veins":['fatigue', 'obesity', 'cramps', 'bruising', 'swollen_legs', 'swollen_blood_vessels', 'prominent_veins_on_calf'],"hepatitis A":['vomiting', 'yellowish_skin', 'nausea', 'loss_of_appetite', 'abdominal_pain', 'yellowing_of_eyes', 'diarrhoea', 'dark_urine', 'muscle_pain', 'mild_fever', 'joint_pain']}

    for disease, symptom_list in b.items():
        disease = Disease.objects.get(name=disease)
        obj_list = []
        for symptom in symptom_list:  
            try:
                s_obj = Symptom.objects.get(name__iexact=symptom.strip())
                # obj_list.append(s_obj)
                disease.disease_symptom.add(s_obj)
            except:
                print(symptom)
        # disease.disease_symtpom.add(obj_list)
 """
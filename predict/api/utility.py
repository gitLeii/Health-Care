import pandas as pd
import random  
import pickle

from predict.models import Symptom, Disease

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
    # print(predicted_disease_dict)
    for name,feats in predicted_disease_dict.items():
        similar_count = 0
        for symptom in test_input_features:
            if symptom in feats:
                similar_count+=1 
        predicted_disease_precent_dict[name] = round(similar_count*100/len(feats), 4)  
    return sorted(predicted_disease_precent_dict.items(), key=lambda x: x[1], reverse=True) 
 """

def make_prediction(user_symptoms):
    symptom_list =  ["itching","skin_rash","nodal_skin_eruptions","dischromic _patches","continuous_sneezing","shivering","chills","watering_from_eyes","stomach_pain","acidity","ulcers_on_tongue","vomiting","cough","chest_pain","yellowish_skin","nausea","loss_of_appetite","abdominal_pain","yellowing_of_eyes","burning_micturition","spotting_ urination","passage_of_gases","internal_itching","indigestion","muscle_wasting","patches_in_throat","high_fever","extra_marital_contacts","fatigue","weight_loss","restlessness","lethargy","irregular_sugar_level","blurred_and_distorted_vision","obesity","excessive_hunger","increased_appetite","polyuria","sunken_eyes","dehydration","diarrhoea","breathlessness","family_history","mucoid_sputum","headache","dizziness","loss_of_balance","lack_of_concentration","stiff_neck","depression","irritability","visual_disturbances","back_pain","weakness_in_limbs","neck_pain","weakness_of_one_body_side","altered_sensorium","dark_urine","sweating","muscle_pain","mild_fever","swelled_lymph_nodes","malaise","red_spots_over_body","joint_pain","pain_behind_the_eyes","constipation","toxic_look_(typhos)","belly_pain","yellow_urine","receiving_blood_transfusion","receiving_unsterile_injections","coma","stomach_bleeding","acute_liver_failure","swelling_of_stomach","distention_of_abdomen","history_of_alcohol_consumption","fluid_overload","phlegm","blood_in_sputum","throat_irritation","redness_of_eyes","sinus_pressure","runny_nose","congestion","loss_of_smell","fast_heart_rate","rusty_sputum","pain_during_bowel_movements","pain_in_anal_region","bloody_stool","irritation_in_anus","cramps","bruising","swollen_legs","swollen_blood_vessels","prominent_veins_on_calf","weight_gain","cold_hands_and_feets","mood_swings","puffy_face_and_eyes","enlarged_thyroid","brittle_nails","swollen_extremeties","abnormal_menstruation","muscle_weakness","anxiety","slurred_speech","palpitations","drying_and_tingling_lips","knee_pain","hip_joint_pain","swelling_joints","painful_walking","movement_stiffness","spinning_movements","unsteadiness","pus_filled_pimples","blackheads","scurring","bladder_discomfort","foul_smell_of urine","continuous_feel_of_urine","skin_peeling","silver_like_dusting","small_dents_in_nails","inflammatory_nails","blister","red_sore_around_nose","yellow_crust_ooze"]
    
    input_data = []
    for symptom in symptom_list:
        if symptom in user_symptoms:
            input_data.append(1)
        else:
            input_data.append(0) 

    with open('ml_model/final1_model.sav', 'rb') as f:
        model = pickle.load(f)
    prediction1 = model.predict([input_data]) 
    print("--------Predicted1: ", prediction1)
    return prediction1
    # return automate_predicted_checking(prediction1, user_symptoms)  
     

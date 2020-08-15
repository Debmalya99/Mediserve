import numpy as np
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import smtplib

def transform_string(s):
    ret_string = str()
    for idx in range(len(s)):
        if(s[idx] == '_'):
            ret_string += ' '
        else:
            ret_string += s[idx]
    return ret_string

def inverse_transform_string(s):
    ret_string = str()
    for idx in range(len(s)):
        if(s[idx] == ' '):
            ret_string += '_'
        else:
            ret_string += s[idx]
    return ret_string

def encode_data(symptom_input,encoder_list):
    # symptom_input is a list
    # returns an np.ndarray
    i = 0
    symptom_array = list()
    for col_name,enc in encoder_list[1:][:]:
        symptom_array.append(int(enc.transform([symptom_input[i]])))
        i += 1
    return np.array(symptom_array).reshape(1,-1)

def decode_output(result,encoder_list):
    return encoder_list[0][1].inverse_transform(result)[0]


def get_description(out_data,desc_dataset):
    for index,row in desc_dataset.iterrows():
        if(row['Disease'] == out_data['text']):
            out_data['desc'] = row['Description']

def get_precautions(out_data,prec_dataset):
    out_data['prec'] = list()
    for index,row in prec_dataset.iterrows():
        if(row['Disease'] == out_data['text']):
            for i in range(1,5):
                if(row['Precaution_'+str(i)] != 'not_needed'):
                    out_data['prec'].append(row['Precaution_'+str(i)])

def form_get_response(mail_data,req,out_data):
    mail_data['Severity'] = out_data['severity']
    mail_data['Predicted Disease'] = out_data['text']
    mail_data['First Name'] = req.args.get('firstname')
    mail_data['Last Name'] = req.args.get('lastname')
    mail_data['Gender'] = req.args.get('gender')
    mail_data['Date of Birth'] = req.args.get('birthday')
    mail_data['Height(cm)'] = req.args.get('hh')
    mail_data['Weight(kg)'] = req.args.get('ww')
    mail_data['Contact Number'] = req.args.get('cno')
    mail_data['User Email-ID'] = req.args.get('emailid')
    mail_data['Selected Hospital'] = req.args.get('hospital')
    mail_data['to_mail_id'] = 'ankurme999@gmail.com'

def send_mail(mail_data,server):
    send_data = str()
    for key in mail_data:
        send_data += key
        send_data += ' : '
        send_data += mail_data[key]
        send_data += '\n'
    server.login("ankurme999@gmail.com", "Ankur@1997")
    server.sendmail("ankurme999@gmail.com", "tisleceb1721@gmail.com",send_data)

def get_severity(sevr_dict,sym_list):
    sev = 0
    for m in sym_list:
        sev += sevr_dict[m]
    if sev in range(0,25):
        return 'Low'
    elif sev in range(25,50):
        return 'Medium'
    elif sev in range(50,75):
        return 'High'
    else:
        return 'Very High'

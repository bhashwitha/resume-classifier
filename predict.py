import os
import tensorflow
import nltk
from nltk.corpus import stopwords
import string
import re
import joblib
import pandas as pd
import warnings
warnings.filterwarnings('ignore') 
nltk.data.path.append('./nltk_data/')
from keras.models import load_model

def c_text(d):
   d = re.sub('http\S+\s*',' ',d) # remove urls
   d = re.sub('RT|cc',' ',d) # RT and cc
   d = re.sub('#\S+|@\S+',' ',d) # hashtags and mentions
   d = re.sub(r'[^\x00-\x7f]',' ',d) 
   d = re.sub('\s+',' ',d) # remove extra spaces
    
   tk = nltk.word_tokenize(d)
   sword =  list(set(stopwords.words('english'))) 
   sword.extend(list(string.punctuation))
   cl_token = [token.lower() for token in tk if token not in sword]
   return ' '.join(cl_token)


def pd_class(text):
    cl_text =c_text(text)
    path = os.path.dirname(__file__)
    my_file = path+'/word_vec_encoder.pkl'
    print("my file path location is", my_file)
    word_encode = joblib.load(path + '/models/decison_tree/word_vec_encoder.pkl')
    text_vec = word_encode.transform([cl_text])
    load_classi = joblib.load(path + '/models/decison_tree/dt.pkl')
    #load_classi.add(tf.keras.layers.Dense(256, input_shape=(x_train.shape[1],), activation='sigmoid'))
    pred = load_classi.predict(text_vec)
    label_encoder = joblib.load(path + '/models/decison_tree/output_label_encoder.pkl')
    result = label_encoder.inverse_transform(pred)
    apred = load_classi.predict_proba(text_vec)[0]
    ans_list = []
    for idx,val in enumerate(apred):
        l=label_encoder.inverse_transform([idx])
        ans_list.append([val,l[0]])
    apred_df = pd.DataFrame(ans_list,columns=['val','label'])
    return result,apred_df
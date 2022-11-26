import tweepy
import pandas as pd import re
import jsonpickle
import string
CONSUMER_KEY = 'ZSDj9mNN79hLmiflJvz213g1K'
CONSUMER_SECRET = '5UHcS1S3bLdOOWRS0uNUQufiOlbrXxuan8b93iU3gJCHtF
dKsE'
ACCESS_TOKEN = '3355371525- wJcqAJVOqbBup6Gz9nXM6Ckx69Uc1xjpUsQpix1'
ACCESS_SECRET = 'B1KBI9ytPN8WBCKtNb7eTO0EToXXPqM3EiRXauX36dLpP'


def connect_to_twitter_OAuth():
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)


api = tweepy.API(auth)
return api


api = connect_to_twitter_OAuth()
query = 'يليابوم'


ax_tweets = 300 lang= 'ar'



tweet_list = []


tweets_collected = tweepy.Cursor(api.search,q=query,lang=lang).it ems(max_tweets)

for tweet in tweets_collected:



tweettosave = jsonpickle.encode(tweet._json, unpicklable=Fals e).encode('utf-8')
tweet_list.append(tweettosave)


def tweets_to_df(tweets):


text = []
reply = []
retweet = [] user = [] screen_name = [] source = []
in_reply_to_screen_name = []


for t in tweets:
t = jsonpickle.decode(t)


text.append(t['text'])
if t['in_reply_to_status_id'] == None:
reply.append(0)
else:
reply.append(1)



retweet.append(t['retweet_count'])






user.append(t['user']['name'])


screen_name.append(t['user']['screen_name'])
 



'])
 
source.append(t['source'])
in_reply_to_screen_name.append(t['in_reply_to_screen_name 

d = {'text': text,
'is_reply': reply,
'retweet_count': retweet,
'user': user,
'screen_name' : screen_name,
'source' : source,
'in_reply_to_screen_name' :in_reply_to_screen_name,
}


return pd.DataFrame(data = d)



tweets = tweets_to_df(tweet_list)
tweets['text'] = tweets['text'].apply(lambda x: re.sub('[!@#$:).;,?؟&%]', ' ', x.lower()))
tweets['text'] = tweets['text'].apply(lambda x: re.sub('[a-zA- Z]', ' ', x.lower()))
tweets['text'] = tweets['text'].apply(lambda x: re.sub(' ', ' ', x))
tweets['text'][1]
tweets = tweets[tweets['source'].str.contains('android')|tweets[' source'].str.contains('iphone')|
tweets['source'].str.contains('iPad')|tweets['source'].str.
contains('Mac')|
tweets['source'].str.contains('Web App')]
arabic_punctuations = '''`÷×؛<>_()*&^%][؛ـ–“…”!|+¦~}{',.؟":/،ـ"-
…،'''
english_punctuations = string.punctuation
punctuations_list = arabic_punctuations + english_punctuations


arabic_diacritics = re.compile("""
ّ| # Tashdid
ّ| # Fatha
ّ| # Tanwin Fath
ّ| # Damma
ّ| # Tanwin Damm
ّ| # Kasra
ّ| # Tanwin Kasr
ّ| # Sukun
ـ# Tatwil/Kashida
""", re.VERBOSE)


def normalize_arabic(text):
text = re.sub("[اآأإ]", "ا", text)
text = re.sub("ى", "ي", text) text = re.sub("ؤ", "ء", text) text = re.sub("ئ", "ء", text) text = re.sub("ة", "ه", text) text = re.sub("گ", "ك", text) return text

def remove_diacritics(text):
text = re.sub(arabic_diacritics, '', text)
return text


def remove_punctuations(text):
translator = re.compile('[%s]' % re.escape(punctuations_list))
translator .sub(' ', text)
text = re.sub(' +',' ', text).strip()
return text
def remove_repeating_char(text):
return re.sub(r'(.)\1+', r'\1\1', text)
tweets['text'] = tweets['text'].apply(lambda x: normalize_arabic(
x))
tweets['text'] = tweets['text'].apply(lambda x: remove_diacritics
(x))
tweets['text'] = tweets['text'].apply(lambda x: remove_punctuatio ns(x))
tweets['text'] = tweets['text'].apply(lambda x: remove_repeating_
char(x))
tweets['text'].replace(r'…',' ',inplace=True, regex=True) tweets['text'].replace(r'_',' ',inplace=True, regex=True) tweets['text'].replace(r'\\\)',' ',inplace=True, regex=True) tweets['text'].replace(r'،',' ',inplace=True, regex=True) tweets['text'].replace(r'"',' ',inplace=True, regex=True) tweets['text'].replace(r'-',' ',inplace=True, regex=True) tweets['text'].replace(r'؛',' ',inplace=True, regex=True) tweets['text'].replace(r'/',' ',inplace=True, regex=True) tweets['text'] = tweets['text'].str.replace('\d+', ' ') tweets['text'] = tweets['text'].str.replace(' +',' ') tweets['text'] = tweets['text'].str.replace('\n',' ') tweets['text']
tweets_list  =list(tweets['text']) tweets_list = list(set(tweets_list)) tweets_list
!pip install googletrans
from googletrans import Translator translator = Translator() english_tweet = []
arabictweet_2 = []
for arabictweet in tweets_list:
try:
translations = translator.translate(arabictweet, dest='en')
except Exception as e:
continue arabictweet_2.append(translations.origin) english_tweet.append(translations.text) print(translations.origin, ' -> ', translations.text)
!pip install vaderSentiment import vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnaly zer

# --- examples ------- sentences = english_tweet neg_score =[]
neu_score =[] pos_score =[] compound_score =[] sentment_class = []

analyzer = SentimentIntensityAnalyzer()
for sentence in sentences:
vs = analyzer.polarity_scores(sentence) neg_score.append(vs.get('neg')) neu_score.append(vs.get('neu')) pos_score.append(vs.get('pos')) compound_score.append(vs.get('compound')) if vs.get('compound') <= -0.05:
sentment_class.append(-1)
elif vs.get('compound') >= 0.05:
sentment_class.append(1)
else:
sentment_class.append(0)


print(vs.get('compound'))
print("{:-<65} {}".format(sentence, str(vs)))
to_dataframe = {'arabic_tweet': arabictweet_2,
'translated_tweet': english_tweet,
'neg': neg_score,
'neu': neu_score,
'pos' : pos_score,
'compound' :compound_score,
'class' :sentment_class
}


final_data = pd.DataFrame(data = to_dataframe) final_data.head(50) final_data.to_csv('final_data.csv',encoding='utf-8-sig')

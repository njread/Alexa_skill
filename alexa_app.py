from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode

app = Flask(__name__)
ask = Ask(app, "/reddit_reader")

def get_headlines():
	user_pass_dict = {'user': 'njread_',
						'passwd': '7pjq6v55x',
						'api_type': 'json'}
	sess = requests.Session()
	sess.headers.update({'User-Agent': 'Test'})
	sess.post('https://www.reddit.com/api/login', data= user_pass_dict)
	time.sleep(1)
	url = 'https://reddit.com/r/worldnews/.json?limit=10'
	html = sess.get(url)
	data = json.loads(html.content.decode('utf-8'))
	titles = [unidecode.unidecode(listing['data']['title'])for listing in data['data']['children']]
	titles = '...'.join([i for i in titles])
	return titles

titles = get_headlines()
print(titles)

@app.route('/')
def homepage():
	return "hello world Nicholas Read productions."
@ask.launch
def start_skill():
	welcome_message = 'hello would you like the news?'
	return question(welcome_message)

@ask.intent("YesIntent")
def share_headlines():
	headlines = get_headlines()
	headlines_msg = 'The current world news headlines are {}'.format(headlines)
	return statement(headlines_msg)
@ask.intent("NoIntent")
def no_intent():
	bye_text = 'im not sure why you asked me then'
	return statement(bye_text)





if __name__ == '__main__':
	app.run(debug=True)
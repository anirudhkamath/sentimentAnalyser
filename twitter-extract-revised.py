import tweepy
import csv 
from textblob import TextBlob
import operator
import copy

def checkminimum(test):
	#test has the intracluster distances for your data point,refer to kmeans function, first for loop
	min_dist = test[0]
	c=0
	p=0	
	for i in test:
		if min_dist>i:
			min_dist = i
			p=c #c is the position of the minimum intracluster distance element
		c=c+1			
	return p


def kmeans(reviews):
	medians=[]
	clusters={}
	clusters2={}
	test=[]
	k = 3 #3 clusters, good, neutral, bad
	count=0
	for i in reviews:
		if count<k:
			medians.append(i)
			count=count+1

	for i in range(k):
		clusters[i]=[] #empty list holds your members of each class
	count=0
	test=[]
	for i in reviews:
		for x in range(k):
			test.append(abs(i-medians[x]))
		pos = checkminimum(test)
		clusters[pos].append(i)
		test=[]	
	#print(clusters)
	while True:	
		medians=[]
		for x in clusters:
			b = sum(clusters[x])/len(clusters[x]) #centroid of the cluster
			medians.append(b)
		for i in range(k):
			clusters[i]=[] #empty list holds your members of each class
		for i in reviews:
			for x in range(k):
				test.append(abs(i-medians[x]))
			pos = checkminimum(test)
			clusters[pos].append(i)
			test=[]
		if clusters2==clusters:
			break	
		#print(clusters)
		for i in range(k):
			clusters2[i]=[] #empty list holds your members of each class
		clusters2=copy.deepcopy(clusters)
	return clusters

consumerKey='xxx'
consumerSecret='xxx'
accessToken='xxx'
accessTokenSecret='xxx' #developers.twitter.com is where you can get these keys

#read and write permissions from Twitter

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)

api = tweepy.API(auth, wait_on_rate_limit=True) #wait_on_rate_limit states whether or not automatically wait for rate limits to replenish (dynamic)

csvFile = open('tweets.csv', 'a') #a is for append
csvWriter = csv.writer(csvFile) #we use a writer because it will write a tweet on each row of the CSV file!

hashtags = ["#s10", "#samsungs10"]


for x in hashtags:
	for t in tweepy.Cursor(api.search, q=x, count=1000, lang="en", since="2019-02-28", until="2019-03-08").items():
		#as per GSMArena, the Samsung S10 was announced in Feb 2019
		#print(t.created_at, t.text)
		csvWriter.writerow([t.created_at, t.text.encode('utf-8')])

csvFile.close()
csvFile = open('tweets.csv', 'r')
csvReader = csv.reader(csvFile, delimiter = '\n', quoting = csv.QUOTE_NONE)
words={}
spam = ["lucky", "LUCKY", "Lucky", "offer", "OFFER", "Offer", "WINNER", "Winner", "winner", "win", "WIN","Win", "giveaway", "Giveaway"]

reviews_polarity=[]
reviews=[]
flag = 0
for x in csvReader:
	flag=0
	test = TextBlob(str(x))
	#print(test)
	for y in spam:
		if y in test:
			flag=1
	if flag==0:
		reviews_polarity.append(test.sentiment.polarity)
		reviews.append(str(x))
		print(x)

print(reviews_polarity)
#print(reviews)
#applying k means on reviews to cluster good and bad reviews

#result_one=kmeans(reviews)
result_two=kmeans(reviews_polarity) #gives us good, bad, and neutral clusters. data centric clusters so as to see how the distribution is.
#print(reviews)
for x in reviews:
	print(x)
	print("\n")
print(result_two)
#cluster result_two[0] holds all the positive sentiment tweet polarities, result_two[1] holds all the neutral tweets, result_two[2] holds negative tweets

print(len(result_two[0]))
print(len(result_two[1]))
print(len(result_two[2]))

rs_two=[]
for x in result_two[2]:
	if x!=0:
		rs_two.append(x)

result_two[2]=rs_two

print(len(result_two[0]))
print(len(result_two[1]))
print(len(result_two[2]))
from TwitterSearch import *
import tumblr


def get_random_tweet():
	try:
	    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
	    tso.set_keywords([tumblr.searchTerm]) # our keyword goes here
	    tso.set_language('en') # we want to see English tweets only
	    tso.set_include_entities(False) # and don't give us all those entity information
	    tso.set_count(1) #Don't want to query 100 tweets

	    # assign keys for TwitterSearch
	    ts = TwitterSearch(
	        consumer_key = 'YOURS',
	        consumer_secret = 'YOURS',
	        access_token = 'YOURS',
	        access_token_secret = 'YOURS'
	     )

	    response = ts.search_tweets(tso)
	    print response['content']['statuses'][0]['text']
	    print "HERE"
	    return response['content']['statuses'][0]['text']
	    # txt_file.close()

	     # this is where the fun actually starts :)
	    # for tweet in ts.search_tweets_iterable(tso):
	    #     tweet_str = '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] )
	    #     print tweet_str.encode('utf-8')

	except TwitterSearchException as e: # take care of all those ugly errors if there are some
	    print(e)
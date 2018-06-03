class Object:
	def __init__(self, tweet_id, tweet_text, favorite_count, retweet_count):
		self.tweet_id = tweet_id
		self.tweet_text = tweet_text
		self.favorite_count = favorite_count
		self.retweet_count = retweet_count

	def gettextt(self):
		return self.tweet_text
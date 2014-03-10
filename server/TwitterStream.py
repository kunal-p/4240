__author__ = 'axel'
import time
import pycurl
import urllib
import json
import oauth2 as oauth
from TweetHandler import TweetHandler

API_ENDPOINT_URL = 'https://stream.twitter.com/1.1/statuses/filter.json'
USER_AGENT = 'TwitterStream 1.0' # This can be anything really

# You need to replace these with your own values
OAUTH_KEYS = {'consumer_key': 'bv9uLn65Zq0etICnJCsA',
              'consumer_secret': 'peLaBMtjTzbpWlrdxVO7kFUMHQ5XHQ2RziUalR5pA4',
              'access_token_key': '21577206-UZMxAwB1SOq3j2sKqqoRIJpq7NQi2h94TrWZOFY83',
              'access_token_secret': '5S1B8h35JawVrpiRBiS4I6Wlg3nFJhzbtOg5dW4vNYMKE'}

class TwitterStream:

    post_params = {}
    tweetHandler = None

    def __init__(self, include_entities, stall_warning, teams, timeout=False):
        trackWords = ''
        for team in teams:
            trackWords = trackWords + team + ','
        trackWords = trackWords[:-1]
        print trackWords
        self.post_params = {'include_entities': include_entities,
               'stall_warning': stall_warning,
               'track': trackWords}
        self.tweetHandler = TweetHandler(teams)

        #Set authorization tokens.
        self.oauth_token = oauth.Token(key=OAUTH_KEYS['access_token_key'], secret=OAUTH_KEYS['access_token_secret'])
        self.oauth_consumer = oauth.Consumer(key=OAUTH_KEYS['consumer_key'], secret=OAUTH_KEYS['consumer_secret'])
        self.conn = None
        self.buffer = ''
        self.timeout = timeout
        self.setup_connection()

    def setup_connection(self):
        """ Create persistant HTTP connection to Streaming API endpoint using cURL."""
        if self.conn:
            self.conn.close()
            self.buffer = ''
        self.conn = pycurl.Curl()
        # Restart connection if less than 1 byte/s is received during "timeout" seconds
        if isinstance(self.timeout, int):
            self.conn.setopt(pycurl.LOW_SPEED_LIMIT, 1)
            self.conn.setopt(pycurl.LOW_SPEED_TIME, self.timeout)
        self.conn.setopt(pycurl.URL, API_ENDPOINT_URL)
        self.conn.setopt(pycurl.USERAGENT, USER_AGENT)
        # Using gzip is optional but saves us bandwidth.
        self.conn.setopt(pycurl.ENCODING, 'deflate, gzip')
        self.conn.setopt(pycurl.POST, 1)
        self.conn.setopt(pycurl.POSTFIELDS, urllib.urlencode(self.post_params))
        #Set connections details with authorization settings.
        self.conn.setopt(pycurl.HTTPHEADER, ['Host: stream.twitter.com',
                                             'Authorization: %s' % self.get_oauth_header()])
        # self.handle_tweet is the method that are called when new tweets arrive
        self.conn.setopt(pycurl.WRITEFUNCTION, self.handle_tweet)

    def get_oauth_header(self):
        """ Create and return OAuth header.
"""
        params = {'oauth_version': '1.0',
                  'oauth_nonce': oauth.generate_nonce(),
                  'oauth_timestamp': int(time.time())}
        req = oauth.Request(method='POST', parameters=params, url='%s?%s' % (API_ENDPOINT_URL,
                                                                             urllib.urlencode(self.post_params)))
        req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), self.oauth_consumer, self.oauth_token)
        return req.to_header()['Authorization'].encode('utf-8')

    def start(self):
        """ Start listening to Streaming endpoint.
Handle exceptions according to Twitter's recommendations.
"""
        backoff_network_error = 0.25
        backoff_http_error = 5
        backoff_rate_limit = 60
        while True:
            self.setup_connection()
            try:
                self.conn.perform()
            except:
                # Network error, use linear back off up to 16 seconds
                print 'Network error: %s' % self.conn.errstr()
                print 'Waiting %s seconds before trying again' % backoff_network_error
                time.sleep(backoff_network_error)
                backoff_network_error = min(backoff_network_error + 1, 16)
                continue
            # HTTP Error
            sc = self.conn.getinfo(pycurl.HTTP_CODE)
            if sc == 420:
                # Rate limit, use exponential back off starting with 1 minute and double each attempt
                print 'Rate limit, waiting %s seconds' % backoff_rate_limit
                time.sleep(backoff_rate_limit)
                backoff_rate_limit *= 2
            else:
                # HTTP error, use exponential back off up to 320 seconds
                print 'HTTP error %s, %s' % (sc, self.conn.errstr())
                print 'Waiting %s seconds' % backoff_http_error
                time.sleep(backoff_http_error)
                backoff_http_error = min(backoff_http_error * 2, 320)

    def handle_tweet(self, data):
        """ This method is called when data is received through Streaming endpoint."""
        self.buffer += data
        if data.endswith('\r\n') and self.buffer.strip():
            # complete message received
            message = json.loads(self.buffer)
            self.buffer = ''
            msg = ''
            if message.get('limit'):
                print 'Rate limiting caused us to miss %s tweets' % (message['limit'].get('track'))
            elif message.get('disconnect'):
                raise Exception('Got disconnect: %s' % message['disconnect'].get('reason'))
            elif message.get('warning'):
                print 'Got warning: %s' % message['warning'].get('message')
            else:
                #Tweet was received correctly. TweetHandler takes care of tweet string.
                self.tweetHandler.handleTweet(message.get('text'))
                #tempNeg = self.getNegatives(message.get('text'))


if __name__ == '__main__':
    teams = ['seahawks', 'saints']
    ts = TwitterStream(0, 'true', teams)
    ts.setup_connection()
    ts.start()

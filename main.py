#!/usr/bin/python
# -*- coding: utf-8 -*-

from analysis import Analysis
from logs import Logs
from trading import Trading
from twitter import Twitter

# Whether to send all logs to the cloud instead of a local file.
LOGS_TO_CLOUD = True

def twitter_callback(text, link):
    """Analyzes Trump tweets, makes stock trades, and sends tweet alerts."""

    # Initialize these here to create separate httplib2 instances per thread.
    analysis = Analysis(logs_to_cloud=LOGS_TO_CLOUD)
    trading = Trading(logs_to_cloud=LOGS_TO_CLOUD)

    companies = analysis.find_companies(text)
    logs.debug("Using companies: %s" % companies)
    if companies:
        trading.make_trades(companies)
        twitter.tweet(companies, link)

if __name__ == "__main__":
    logs = Logs(name="main", to_cloud=LOGS_TO_CLOUD)

    # Restart in a loop if there are any errors so we stay up.
    while True:
        logs.info("Starting new session.")

        twitter = Twitter(logs_to_cloud=LOGS_TO_CLOUD)
        try:
            twitter.start_streaming(twitter_callback)
        except BaseException as exception:
            logs.catch(exception)
        finally:
            logs.info("Ending session.")

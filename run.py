from campaign import Campaign
import sys
import os

if __name__ == '__main__':
    if len(sys.argv) > 1:
        campaign_location = os.path.abspath(sys.argv[1])
        campaign = Campaign(sys.argv[1])
        campaign.run()
    else:
        print('No or invalid campaign path specified.')

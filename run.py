from campaign import Campaign

if __name__ == '__main__':
    campaign = Campaign('campaign.json') #, write=lambda x: None)
    campaign.run()

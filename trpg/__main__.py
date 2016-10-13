import os
import sys
from trpg.campaign import Campaign


def main(file_location=None, write=print, debug=lambda x: None, read=input):
    """Entry point for TRPG."""
    try:
        if file_location is None:
            file_location = sys.argv[1]
    except IndexError:
        print('No file provided. Try trpg sample')
        return

    try:
        if file_location == 'sample':
            print('Running sample campaign.')
            directory = os.path.dirname(os.path.abspath(__file__))
            print(directory)
            campaign_location = os.path.join(directory, 'sample.trpg')
        else:
            campaign_location = os.path.abspath(file_location)

        campaign = Campaign(campaign_location,
                            write=write,
                            debug=debug,
                            read=read,
                            bold=('<b>', '</b>'),
                            italic=('<i>', '</i>'))
        campaign.run()
    except FileNotFoundError:
        print('File not found.')
    except KeyError:
        print('Input file was not in the correct format.')


if __name__ == '__main__':
    main(file_location='sample')

import sys
import os
import re
from langdetect import detect
from os.path import dirname, realpath, join

# This is just a way of getting the path to this script
my_path = dirname(realpath(__file__))
# This is the path to the 'data' directory, which will store the files
# in the same format as the files in the 'test' directory
data_dir = join(my_path, 'data')

def get_reviews_for_game(file_name):
    '''
    Get list of reviews in a single game file.

    :param file_name: name of file
    :type file_name: str
    :returns: list of dicts
    '''

    reviews = []
    lines = open(join(data_dir, file_name)).readlines()
    i = 0
    while i + 1 < len(lines): # We need to get every 2-line couplet
        # Extract the hours value and the review text from each 2-line
        # sequence
        try:
            h = float(lines[i].split()[1].strip())
            r = lines[i + 1].split(' ', 1)[1].strip()
        except (ValueError, IndexError) as e:
            i += 2
            continue
        # Skip reviews that don't have at least 50 characters
        if len(r) <= 50:
            i += 2
            continue
        if len(r) > 1000:
            i +=2
            continue
        # Skip reviews with more than 1000 characters (?)
        # Insert code here
        # Skip if number of hours is less than 5 or greater than 5000
        if h < 10:
            i += 2
            continue
        if h > 5000:
            i += 2
            continue
        # Skip reviews if they cannot be recognized as English
        try:
            if not detect(r) == 'en':
                i += 2
                continue
        except LangDetectError:
            i += 2
            continue
        # Contraction rules
        # these were the ones grepped in the current data files Matt obtained
        # wont ==> won't
        r = re.sub(r"\bwont\b", r"won't", r, re.IGNORECASE)
        # dont ==> don't
        r = re.sub(r"\bdont\b", r"don't", r, re.IGNORECASE)
        # wasnt ==> wasn't
        r = re.sub(r"\bwasnt\b", r"wasn't", r, re.IGNORECASE)
        # werent ==> weren't
        r = re.sub(r"\bwerent\b", r"weren't", r, re.IGNORECASE)
        #aint ==> am not
        r = re.sub(r"\baint\b", r"am not", r, re.IGNORECASE)
        #arent ==> are not
        r = re.sub(r"\barent\b", r"are not", r, re.IGNORECASE)
        #cant ==> can not
        r = re.sub(r"\bcant\b", r"can not", r, re.IGNORECASE)
        #didnt ==> does not
        r = re.sub(r"\bdidnt\b", r"did not", r, re.IGNORECASE)
        #havent ==> have not
        r = re.sub(r"\bhavent\b", r"have not", r, re.IGNORECASE)
        #ive ==> I have
        r = re.sub(r"\bive\b", r"I have", r, re.IGNORECASE)
        #isnt ==> is not
        r = re.sub(r"\bisnt\b", r"is not", r, re.IGNORECASE)
        #theyll ==> they will
        r = re.sub(r"\btheyll\b", r"they will", r, re.IGNORECASE)
        #thats ==> that's
        r = re.sub(r"\bthatsl\b", r"that's", r, re.IGNORECASE)
        #whats ==> what's
        r = re.sub(r"\bwhats\b", r"what's", r, re.IGNORECASE)
        #wouldnt ==> would not
        r = re.sub(r"\bwouldnt\b", r"would not", r, re.IGNORECASE)
        #im ==> I am
        r = re.sub(r"\bim\b", r"I am", r, re.IGNORECASE)
        #youre ==> you are
        r = re.sub(r"\byoure\b", r"you are", r, re.IGNORECASE)
        #youve ==> you have
        r = re.sub(r"\byouve\b", r"you have", r, re.IGNORECASE)
        
        #cases which I'm not sure we should change - ill, it, and  lets
        
        # Get the hang of it now?
        # Insert more contraction code here
        # Now we append the 2-key dict to the end of reviews
        reviews.append(dict(hours=h,
                            review=r))
        i += 2 # Increment i by 2 since we need to go to the next
            # 2-line couplet
    return reviews

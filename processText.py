import os
import codecs

data_directory = os.path.join('.', 'data',
                              'yelp_dataset_challenge_academic_dataset')

businesses_filepath = os.path.join(data_directory,
                                   'yelp_academic_dataset_business.json')

with codecs.open(businesses_filepath, encoding='utf_8') as f:
    first_business_record = f.readline() 

review_json_filepath = os.path.join(data_directory,
                                    'yelp_academic_dataset_review.json')

with codecs.open(review_json_filepath, encoding='utf_8') as f:
    first_review_record = f.readline()
    
    
import json

restaurant_ids = set()

# open the businesses file
with codecs.open(businesses_filepath, encoding='utf_8') as f:
    
    # iterate through each line (json record) in the file
    for business_json in f:
        
        # convert the json record to a Python dict
        business = json.loads(business_json)
        
        # if this business is not a restaurant, skip to the next one
        if (business[u'categories'] == None) or (u'Restaurants' not in business[u'categories']):
            continue
            
        # add the restaurant business id to our restaurant_ids set
        restaurant_ids.add(business[u'business_id'])

# turn restaurant_ids into a frozenset, as we don't need to change it anymore
restaurant_ids = frozenset(restaurant_ids)

# print the number of unique restaurant ids in the dataset
print '{:,}'.format(len(restaurant_ids)), u'restaurants in the dataset.'


intermediate_directory = os.path.join('.', 'intermediate')

review_txt_filepath = os.path.join(intermediate_directory,
                                   'review_text_all.txt')

# this is a bit time consuming - make the if statement True
# if you want to execute data prep yourself.
if 1 == 1:
    
    review_count = 0

    # create & open a new file in write mode
    with codecs.open(review_txt_filepath, 'w', encoding='utf_8') as review_txt_file:

        # open the existing review json file
        with codecs.open(review_json_filepath, encoding='utf_8') as review_json_file:

            # loop through all reviews in the existing file and convert to dict
            for review_json in review_json_file:
                review = json.loads(review_json)

                # if this review is not about a restaurant, skip to the next one
                if review[u'business_id'] not in restaurant_ids:
                    continue

                # write the restaurant review as a line in the new file
                # escape newline characters in the original review text
                review_txt_file.write(review[u'text'].replace('\n', '\\n') + '\n')
                review_count += 1

    print u'''Text from {:,} restaurant reviews
              written to the new txt file.'''.format(review_count)
    
else:
    
    with codecs.open(review_txt_filepath, encoding='utf_8') as review_txt_file:
        for review_count, line in enumerate(review_txt_file):
            pass
        
    print u'Text from {:,} restaurant reviews in the txt file.'.format(review_count + 1)
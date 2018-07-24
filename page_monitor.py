#monitors BHW main page, texts me  new threads

import time
from bs4 import BeautifulSoup
import requests
import smtplib

base_url = 'https://blackhatworld.com/'
headers = {'user-agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
email_content = '\n'

# Search terms
search_terms = ['instagram', 'youtube', 'google', 'vpn', 'pbn', 'proxy', 'pva',
                'proxies', 'account', 'views', 'followers', 'seo', 'a', 'i']

# Text notifications or not
text_notification = False

# Scrapes the initial threads(posts), doesn't search these for search_terms
r = requests.get('https://www.blackhatworld.com', headers=headers)
html = r.text
soup = BeautifulSoup(html.encode('utf-8'), 'html.parser')

li = soup.find_all('li', {'class': 'discussionListItem'})
last_post = li[0].h3.a.text
thread_url = base_url + li[0].h3.a['href']

# Print title, page url
print 'Last post: ', last_post
print '\t', thread_url
print

# Continue to scrape the threads in a timed loop
while True:

    r = requests.get('https://www.blackhatworld.com', headers=headers)
    html = r.text
    soup = BeautifulSoup(html.encode('utf-8'), 'html.parser')

    li = soup.find_all('li', {'class': 'discussionListItem'})
    count =1

    # On first loop it creates a list to hold new threads, on subsequent loops it empties the list
    # so it's ready for new entries
    new_threads = []

    for thread in li:
        #author = thread.attrs['data-author']
        #author_url = base_url + thread.a['href']
        thread_url = base_url + thread.h3.a['href']
        thread_title = thread.h3.a.text

        # Ensuring we aren't going back over threads we've already done
        if thread_title != last_post:

            # Searching thread title for each search term
            for term in search_terms:
                if term in thread_title.lower():

                    # if search terms found,add it to the list
                    new_threads.append([thread_title, thread_url])

                    # and add it to email notification if notifications turned on
                    email_content += thread_title + '\n' + thread_url + '\n'
                    print '\n**********\nNew thread with at least 1 search term: ', term + '\n'

                    #If any search term is found we break, not needing to go thru the rest of the terms
                    break
                else:
                    print 'New thread found but search term ' + '"' + term + '"' + ' not found'
                    pass
        else:
            break

    # If we have new threads in the list, set the last one as the last post
    if new_threads:
        last_post = new_threads[0][0]
        ntp = '%s new threads posted' %(len(new_threads))
        print ntp
        thread_counter = 1

        # Print new threads
        for thread in new_threads:
            print str(thread_counter) + ': ' + thread[0]
            print '\t', thread[1]
            print '**********'
            thread_counter += 1


        if text_notification:
            #######################
            # MAIL SETUP AND SEND #
            #######################
            
            """Sends an email to phone_number@phones_service_provider. The phones service provider
            then sends it as a text to the phone. eg 1234567890@txt.att.net"""
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login('gmail_acct_ur_sending_from@gmail.com', 'GmailAcctPassword')
            server.sendmail('gmail_acct_ur_sending_from@gmail.com', 'phone_number_to_send_to@txt.att.net', email_content.encode('utf-8'))
            server.close()
            email_content = ''

    else:
        # Showing time so we know script is still working
        print 'No new threads. Time is', time.time()
    print
    time.sleep(15)




"""Profile monitor"""
profile_monitor_page = 'https://www.blackhatworld.com/members/profile_goes_here/'
msg = soup.find('dl', {'class':'pairsInline lastActivity'}).text.strip().split(':')[0] #u'Member_Name was last seen'
msg_date = soup.find('abbr', {'class':'DateTime muted'}) #u'Jan 16, 2018'
msg_hour = msg_date.attrs['data-timestring'] #u'5:38 AM'

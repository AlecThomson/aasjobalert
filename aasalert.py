#!/usr/bin/env python3

import bs4
import requests
import datetime

currentDT = datetime.datetime.now()
this_year = currentDT.strftime("%Y-%m-%d")
last_year = str(currentDT.year - 1) + currentDT.strftime("-%m-%d")


def get_jobs(keyword):
    url = 'https://jobregister.aas.org/jobs/query?publish_date_start='+ last_year +'&publish_date_end='+ this_year +'&title=&body='+keyword+'&job_category=PostDocFellow&institution_classification=Other%2CFrgn%2CGovA%2CInds%2CLA%2CPl%2CRL%2CSM&location_country=unknown&salary_min=0&salary_max=0&hourly_rate_min=0&hourly_rate_max=0&stipdend_min=0&stipdend_max=0'

    #Download page
    getPage = requests.get(url)
    getPage.raise_for_status() #if error it will stop the program

    #Parse text
    alltext = bs4.BeautifulSoup(getPage.text, 'html.parser')
    maintext = str(alltext.select('#block-system-main > div'))

    bad_time = 'No results' # Look for no results output
    search = maintext.find(bad_time)

    available = search == -1


    if available:
        print("Post-doc positions with the keyword '"+ keyword +"' are available!")
        print('\n')
        i = 1
        jobname = 'jobs'
        while jobname != '':
            jobname =  str(alltext.select('#block-system-main > div > table > tbody > tr:nth-child('+str(i)+')'))
            start = jobname.find('/ad/', 0, len(jobname))
            jobname = jobname[start+14:]
            end = jobname.find('<', 0, len(jobname))
            if jobname != '':
                jobname = jobname[:end]
                print('•'+jobname)
                print('\n')

            i += 1
        print('Follow this link for details: ' + url)

        # TO-DO (maybe) - implement email notification
        # ------------------- E-mail list ------------------------
        #toAddress = ['example1@email.com','example2@email.com']
        # --------------------------------------------------------
        #conn = smtplib.SMTP('smtp.gmail.com', 587) # smtp address and port
        #conn.ehlo() # call this to start the connection
        #conn.starttls() # starts tls encryption. When we send our password it will be encrypted.
        #conn.login('youremail@gmail.com, 'appkey')
        #conn.sendmail('youremail@gmail.com', toAddress, 'Subject: Borzaska Alert!\n\nAttention!\n\nYour favourite food is available today!\n\nBon apetite!:\nFood Notifier V1.0')
        #conn.quit()
        #print('Sent notificaton e-mails for the following recipients:\n')
        #for i in range(len(toAddress)):
        #    print(toAddress[i])
        #print('')
    else:
        print("No post-doc positions with the keyword '"+ keyword +"' were found...")

if __name__ == "__main__":
    import argparse

    # Help string to be shown using the -h option
    descStr = """
    Search the AAS job register for post-doc positions in the last year.
    Some code stolen from https://www.codementor.io/gergelykovcs/how-and-why-i-built-a-simple-web-scrapig-script-to-notify-us-about-our-favourite-food-fcrhuhn45#the-process-of-building-the-web-scrapig-script
    """

    # Parse the command line options
    parser = argparse.ArgumentParser(description=descStr,
                                 formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("keyword", metavar="keyword", nargs=1,
                        help="Keyword to search the AAS job register for.", type=str)

    args = parser.parse_args()

    get_jobs(args.keyword[0])
from malparser import MAL
from pprint import pprint
import json
import re 
import time
import datetime
from bs4 import BeautifulSoup
import requests
import sys
import linecache
import urllib2

#Welcome to the creator of life 


# define('DB_NAME', 'db607452881');

# /** MySQL database username */
# define('DB_USER', 'dbo607452881');

# /** MySQL database password */
# define('DB_PASSWORD', 'jokhil123');

# /** MySQL hostname */
# define('DB_HOST', 'db607452881.db.1and1.com');


#
#it must simply add new anime shows to the database
#and backup the database
#
#go through the MAL api one by one
#for each of the MAL Anime entries, get the title and use that to search AU
#with the AU Result you get a bunch of links
#with those links scrape the anime title, and episodes
#if it is not already in the DB, add the category
#if it is not already in the DB, add the episodes to the database, after each entry, wait 30 seconds
#
#after adding all existing episodes:
#check if anime is unfinished or completed
#the unfinished anime LINKS to a file for updates - see the un-finished plan below
#at the end of the MAL Search, 



#unfinished anime
#they are added to a json list dynamically
#a seperate script loops through the list, does not write to it
#the seperate script creates a temp(working) copy of the json file at the start of each loop
#with each entry, which is a link, open it and get episode numbers
#checks if the post exists in the DB, if not add it and wait 30seconds
#end of list, it deletes the working copy file and starts again (because the file will have been updated by now)
def PrintException():
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)

print("     _            _                     ____        _         _     ")
print("    / \    _ __  (_) _ __ ___    ___   / ___| __ _ | |_  ___ | |__  ")
print("   / _ \  | '_ \ | || '_ ` _ \  / _ \ | |    / _` || __|/ __|| '_ \ ")
print("  / ___ \ | | | || || | | | | ||  __/ | |___| (_| || |_| (__ | | | |")
print(" /_/   \_\|_| |_||_||_| |_| |_| \___|  \____|\__,_| \__|\___||_| |_|")
print("Automated Content Creator")
print(" ")
print("Version: 0.2.1    By: Taheer Jokhia")
print(" ")
print("This tool will add a Anime Shows to the Database constantly")
print(" ")
print(" ")

mal = MAL()
go = True 

while(go == True):
    for x in range(100, 99999):
            try:
                    print("Getting A New Search Query")
                    anime = mal.get_anime(x)
                    anime.fetch()
                    entry = anime.__dict__
                    string = str(entry['alternative_titles']['English'])
                    searchquery = string.replace("[", "").replace("]", "").replace("'", "")
                    print("Search query created: " + str(searchquery))
                    links = []
                    try:
                        print('Getting Links from Query')
                        stitle = searchquery
                        stitle = stitle.replace(" ", "+")
                        r = requests.get('http://www.animeultima.io/search.html?searchquery=' + stitle).text
                        soup = BeautifulSoup(r, 'html.parser')
                        searchResult = soup.findAll("ol", {"id": "searchresult"})
                        for l in searchResult:
                            link = l.findAll("a")
                            for q in range(0, len(link)):
                                links.append(str(link[q]["href"]))
                        print("Links Successfully Scraped")
                        links = list(set(links))

                        for u in range(0, len(links)):
                            try:
                                print("Working on link number: " + str(u))

                                html = requests.get(links[u]).text
                                soup = BeautifulSoup(html, 'html.parser')
                                desc = soup.find("div", {"class": "anime-desc"})
                                #title
                                titleFull = desc.find("h2").get_text()
                                title = titleFull.replace(" Synopsis", "")
                                title = title.replace("'s","")
                                slug = re.sub(r'\W+', '-', title)

                                ########## IMAGE FROM MAL
                                try:
                                    malurl = 'http://taheerj:j1o2k3h4i5l6@myanimelist.net/api/anime/search.xml?q=' + re.sub(r'\W+', '+', title);
                                    malresponse = requests.get(malurl).text
                                    malsoup = BeautifulSoup(malresponse, 'html.parser')
                                    malimage = malsoup.find("image").get_text()
                                except Exception,e:
                                    malimage = "http://www.animecatch.co.uk/wp-content/uploads/2015/12/animecatch-logo1.png"
                                    pass

                                if(malimage == ""):
                                    malimage = "http://www.animecatch.co.uk/wp-content/uploads/2015/12/animecatch-logo1.png"    
                                ##############
                                # slug = slug.replace(" ","-")
                                #number of episodes & status
                                table = desc.find("table")
                                rows = table.findAll("tr")
                                for row in rows:
                                    columns = row.findAll("td")
                                    if(columns[0].get_text() == "Episodes"):
                                        episodescount = columns[1].get_text()
                                    if(columns[0].get_text() == "Status"):
                                        status = columns[1].get_text()
                                #summary
                                ps = desc.findAll("p")
                                summary = ps[0].get_text()
                                summary = summary.replace("'","")
                                summary = summary.replace('"',"")

                                #######################################
                                #      MUST CREATE CATEGORY HERE 
                                #######################################
                                
                            
                                # Connect to the database




                                #create an array for this anime's posts
                                postsarray = {}
                                postids = []
                                # Connect to the database




                                postdata = {}
                                postdata['iscat'] = 'yes'
                                postdata['title'] = title
                                postdata['summary'] = summary
                                postdata['subbed'] = ''
                                postdata['number'] = ''
                                postdata['embed'] = ''
                                pdata = json.dumps(postdata)
                                req = urllib2.Request('http://www.animecatch.com/catchertunnel.php')
                                req.add_header('Content-Type', 'application/json')

                                response = urllib2.urlopen(req, pdata)
                                print('Sent to server... SERVER SAYS:')
                                print(response.read())

                                print("Server break time 3 seconds")
                                time.sleep(3)

                                #Actual episodes
                                #episodes:
                                #   subbed
                                #       1
                                #           embed
                                #           title
                                #   dubbed
                                animetable = soup.find("table", {"id": "animetable"})
                                eprows = animetable.findAll("tr")
                                eprows.remove(eprows[0])

                                if(len(eprows) < 1):
                                    print("No episodes found for: " + str(title))

                                for e in range(0, len(eprows)):
                                    episodenumber = e + 1
                                    
                                    # SUBBED
                                    embedcodefs = ""
                                    if(eprows[e].find("td", {"class": "td-lang-subbed"})):
                                        altlinkss = []
                                        link = eprows[e].find("td", {"class": "td-lang-subbed"}).find("a")["href"]
                                        ephtml = requests.get(link).text
                                        epsoup = BeautifulSoup(ephtml, 'html.parser')
                                        embedcode = epsoup.find("div", {"class": "player-embed"}).find("iframe")
                                        #HAS TO CHECK IF EMBED IS EMPTY, IF IT IS, TRY ANOTHER LINK, KEEP TRYING OTHER LINKS
                                        if(str(embedcode) == "None"):
                                            #this link was killed in action
                                            validfound = 0
                                            relatedvideoss = epsoup.findAll("div", {"class": "generic-video-item"})
                                            for div in relatedvideoss:
                                                subbedspan = div.find("span", {"class": "video-subbed"})
                                                if(str(subbedspan) != "None"):
                                                    #this div is a subbed video
                                                    thumbs = div.find("div", {"class": "thumb"})
                                                    tagass = div.findAll("a")
                                                    for tagas in tagass:
                                                        liens = tagas['href']
                                                        if "users" not in liens:                 
                                                            altlinkss.append("http://www.animeultima.io" + liens)
                                                            for altlinks in altlinkss:            
                                                                ephtmls = requests.get(altlinks).text
                                                                epsoups = BeautifulSoup(ephtmls, 'html.parser')
                                                                embedcodes = epsoups.find("div", {"class": "player-embed"}).find("iframe")
                                                                if(str(embedcodes) != "None"):
                                                                    validfound = 1
                                                                    embedcodefs = embedcodes
                                                                    break
                                                                if(validfound != 1):
                                                                    embedcodefs = "None"
                                        else:
                                            embedcodefs = embedcode

                                        embedcodefs = str(embedcodefs).replace("'", '"')
                                        embedcodefinal = embedcodefs


                                        #######################################
                                        #      MUST CREATE SUBBED POST HERE 
                                        #######################################
                                        

                                        #create post
                                        posttitle = str(title)+" - Episode "+str(episodenumber) +" - English Subbed"
                                        postslug = re.sub(r'\W+', '-', posttitle)
                                        #postslug = postslug.replace(" ","-")
                                        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                                        ts = str(st)

                                        if(embedcodefinal != ""):

                                            postdata = {}
                                            postdata['iscat'] = 'no'
                                            postdata['title'] = title
                                            postdata['summary'] = summary
                                            postdata['subbed'] = 'yes'
                                            postdata['number'] = episodenumber
                                            postdata['embed'] = embedcodefinal
                                            postdata['image'] = malimage
                                            pdata = json.dumps(postdata)
                                            req = urllib2.Request('http://www.animecatch.com/catchertunnel.php')
                                            req.add_header('Content-Type', 'application/json')

                                            response = urllib2.urlopen(req, pdata)
                                            print('Sent to server... SERVER SAYS:')
                                            print(response.read())

                                            print("Pausing to give the server a break - for 3 seconds")
                                            time.sleep(3)


                                        #add image


                                        # DUBBED
                                        embedcodedf = ""
                                        if(eprows[e].find("td", {"class": "td-lang-dubbed"})):
                                            altlinks = []
                                            linkd = eprows[e].find("td", {"class": "td-lang-dubbed"}).find("a")["href"]
                                            ephtmld = requests.get(linkd).text
                                            epsoupd = BeautifulSoup(ephtmld, 'html.parser')
                                            embedcoded = epsoupd.find("div", {"class": "player-embed"}).find("iframe")
                                            if(str(embedcoded) == "None"):
                                                #this link was killed in action
                                                validfound = 0
                                                relatedvideos = epsoupd.findAll("div", {"class": "generic-video-item"})
                                                for div in relatedvideos:
                                                    dubbedspan = div.find("span", {"class": "video-dubbed"})
                                                    if(str(dubbedspan) != "None"):
                                                        #this div is a dubbed video
                                                        thumb = div.find("div", {"class": "thumb"})
                                                        tagas = div.findAll("a")
                                                        for taga in tagas:

                                                            lien = taga['href']
                                                            if "users" not in lien: 
                                                                altlinks.append("http://www.animeultima.io" + lien)
                                                                                   
                                                                #altlinks.append()
                                                                for altlink in altlinks:
                                                                        
                                                                    ephtmlda = requests.get(altlink).text
                                                                    epsoupda = BeautifulSoup(ephtmlda, 'html.parser')
                                                                    embedcodeda = epsoupda.find("div", {"class": "player-embed"}).find("iframe")
                                                                    if(str(embedcodeda) != "None"):
                                                                        validfound = 1
                                                                        embedcodedf = embedcodeda
                                                                        break
                                                                    if(validfound != 1):
                                                                        embedcodedf = "None"
                                    
                                            else:
                                                embedcodedf = embedcoded
                                                                            
                                                               
                                        embedcodedf = str(embedcodedf).replace("'", '"')
                                        embedcodefinal = embedcodedf

                                        #######################################
                                        #      MUST CREATE POST HERE 
                                        #######################################      

                                        #create post
                                        posttitle = str(title)+" - Episode "+str(episodenumber) +" - English Dubbed"
                                        postslug = re.sub(r'\W+', '-', posttitle)
                                        #postslug = postslug.replace(" ","-")
                                        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                                        ts = str(st)

                                        if(embedcodefinal != ""):

                                            postdata = {}
                                            postdata['iscat'] = 'no'
                                            postdata['title'] = title
                                            postdata['summary'] = summary
                                            postdata['subbed'] = 'no'
                                            postdata['number'] = episodenumber
                                            postdata['embed'] = embedcodefinal
                                            postdata['image'] = malimage
                                            pdata = json.dumps(postdata)
                                            req = urllib2.Request('http://www.animecatch.com/catchertunnel.php')
                                            req.add_header('Content-Type', 'application/json')

                                            response = urllib2.urlopen(req, pdata)
                                            print('Sent to server... SERVER SAYS:')
                                            print(response.read())

                                            print("Sleeping for 3 seconds...zzzzz")
                                            time.sleep(1)
                                            print("zzzzzzzzzz")
                                            time.sleep(2)  

                                time.sleep(10)          

                            except Exception, e:
                                print("something in the AU Scraper failed... see below:")
                                PrintException()
                                pass

                    except Exception, e:
                        print("Error getting links for this search query")
                        print(str(e))
                        pass


            except Exception,e:
                    print str(x) + " id is not in MAL database. Error Message:"
                    print str(e)
                    pass 

    print "FINISHED!"
    print("Cooling down after 10,000 runs")
    print("whew that was tough")
    time.sleep(30)
    print("wait a sec, I'm going to restart the loop soon...")
    time.sleep(5)
    print("*snores*")
    print("ZZZZZZZZ")
    time.sleep(5)
    print("Okay, restarting in")
    print("5")
    time.sleep(1)
    print("4")
    time.sleep(1)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    print("Restarting Loop...")

Enter file contents here

import requests
from bs4 import BeautifulSoup
import sqlite3
from lxml import etree
import csv
import time
import re
from tkinter import messagebox

messagebox.showinfo("Start", "The program has started, please wait until finished")

conn=sqlite3.connect("Scrapped-Data.db")
cur=conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS html_websites(ComapnysName TEXT, GooglesResult TEXT, AlexasResult TEXT)")

#For scrapping
headers = {'user-agent': 'my-app/0.0.1'}

#We are getting the path inputed for connections.csv
frontend=open("input.txt",'r')
path=frontend.readline()
path=path.replace("\n","")

#We are Reading the connection.csv file
oofile= open(path,'r',encoding='utf-8',errors='ignore')
reader=  csv.reader(oofile)

#We are opening the first level of segmentation
path=frontend.readline()
path=path.replace("\n","")

fseg=open(path,'r',encoding='utf-8',errors='ignore')
fseg_reader=csv.reader(fseg)

#We are creating out data mined filed
openFile=open('ScrappedData.csv',"wt",encoding='utf8')
writer = csv.writer(openFile)
colums=[" Company Name "," Company Site "," Alexa Site "," Global Rank "," Improvment of rank "," Bounce Rate "," Improvment of bounce rate "," Daily page views "," Improvmeent of daily page views "," Daily time on site "," Imporvment of time on site "," comp 1 "," comp 2 "," comp 3 "," comp 4 "," comp 5 "," status "," Rank "]
writer.writerow(colums)

#This dic will be of every company and a list of it's data mined
dic={}


#The index is for testing purposes
index=0;

rank=0

for row in reader:
    #delay wanted
    #time.sleep(0.2)

    #here so you can read the log on where you are
    print(row[3])
    index=index+1
    print(index)
    
    #unnesscary row has to be skipped
    if index==1:
        continue
    
    
    #Change the testing range here
    if index==5:
        break
    
    #Start of the scrapper
    try:
        research_later = row[3]
        
        try:
            x=dic[research_later]
            continue
        except:
            pass
        
        goog=research_later.replace(" ","+")
        goog=goog.replace(".","")
        goog=goog.replace("?","")
        goog=goog.replace("!","")
        goog=goog.replace(",","")
        goog=goog.replace("\"","")
        goog=goog.replace("\\","")
        goog=goog.replace("\'","")
        goog=goog.replace("/","")

        goog_search = "https://www.google.jo/search?q=" +goog+"&oq=&gs_l=psy-ab.1.0.35i39k1l6.5528.9337.0.16247.24.14.6.0.0.0.246.1561.0j9j1.11.0.dummy_maps_web_fallback...0...1.1.64.psy-ab..8.16.1595.6..0j0i131k1.154.3qsaiUDOSnA"

        r = requests.get(goog_search,headers)
        soup1 = BeautifulSoup(r.text, "html.parser")

        link=soup1.find("cite").text
        alexa_search="https://www.alexa.com/siteinfo/"+link

        #is this site our target or not
        descrb=soup1.findAll("span",{"class":"st"})
        
        for i in range(3):
            x=re.search("banking|bank|ecommerce|travel|agency|online shopping|shopping|exchange rate|currency|finance|safe payment|Business|loan|booking|hotels|reservation|Electronic Commerce|commerce|E-commerce|mobile businesses|enterprises|market|for consumers|marketing|conversion rates|stock",descrb[i].text,re.IGNORECASE)
            if x==None:
                continue
            else:
                rank=100
                break
        
        
        r=requests.get(alexa_search)
        soup2=BeautifulSoup(r.text,"html.parser")
        
        try:
            cur.execute("INSERT INTO html_websites(ComapnysName,GooglesResult,AlexasResult)  VALUES(?,?,?)",(research_later,str (soup1),str (soup2)))
        except:
            pass
            
        conn.commit()

        #First DB's job has ended
        
        #Now we are minning the data

        main_div=soup2.find("div",{"class":"rank-row"})

        total_data=[]
        global_rank= main_div.find("strong",{"class":"metrics-data align-vmiddle"})

        try:
            improvment=main_div.findAll("span")[4]
        except:
            improvment= None
            
        total_data.append(research_later)
        #
        total_data.append(link)
        total_data.append(alexa_search)
        total_data.append(global_rank)
        total_data.append(improvment["title"])
        #
            
        second_div=soup2.find("table",{"cellpadding":"0"})
        second_divcountry=second_div.findAll("a")
        second_divprec=second_div.findAll("td")

        #country- prec- number

        third_div=soup2.find("section",{"id":"engage-panel"})
        main_3rd=third_div.findAll("div")

        try:
            for i in range (8,11):
                total_data.append(main_3rd[i].strong)
                total_data.append(main_3rd[i].span["title"]) #title attrib here
        except:
            for i in range (8,11):
                total_data.append(None)
                total_data.append(None)

        sites=soup2.find("table",{"id":"audience_overlap_table"})
        sites2=sites.tbody.findAll("td")

        for si in sites2:
            total_data.append(si)
            
        for i in range(len(sites2),5):
            total_data.append(None)

        ok =False
        second_data=[]
        for data in total_data:
            var=""
            if data== None:
                var=" Null " 
                ok=True
            try:
                var=" "+data.text+" "
            except:
                var=" "+data+" "
            second_data.append(var.replace('\n',""))
            
        for i in range(len(second_data),16):
            ok=True
            second_data.append(" Null ")
            
        if ok:
            second_data.append(" Must Check ")
        else:
            second_data.append(" Checked ")
        
        second_data.append(rank)
        dic[research_later]=second_data
        writer.writerow(second_data)
    except:
        print("error")
        s_data=[]
        try:
            s_data.append(row[3])
        except:
            s_data.append("Unknown")
        for i in range(15):
            s_data.append(" Null ")
            
        s_data.append(" Not Checked ")
        s_data.append(rank)
        writer.writerow(s_data)
        
#Out of the loop

final_seg=open("Result.csv","wt",encoding='utf8')
writer=csv.writer(final_seg)

index =0
for row in fseg_reader:
    if index==5:
        break
    index=index+1
    print(row[4])
    try:
        li1=dic[row[4]]
    except:
        li1=["error","error"]*9
        print("problem")

    li2=row[:-1]
    print(row[4])
    print(li1[17])
    try:
        li1[17]=li1[17]+int (row[7])
    except:
        li1[17]=int (row[7])
    li3=li2+li1
    writer.writerow(li3)
    
messagebox.showinfo("Congradz", "The program has finished,if you encountered any bug, please report it")

final_seg.close()
openFile.close()
oofile.close()
                  

        



    
                                 



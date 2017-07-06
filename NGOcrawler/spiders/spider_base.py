import os
import sys
#import feedparser
#from bs4 import BeautifulStoneSoup
from bs4 import BeautifulSoup
#from nltk import clean_html
import urllib
import re
import json

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.item import Item, Field
from NGOcrawler.items import NgocrawlerItem


class NGOSpider(scrapy.Spider):
    name = "ngo"
    #allowed_domains = ['achildshopefoundation.org']
    #start_urls = ['https://achildshopefoundation.org']

    #allowed_domains = ['afcfoundation.org']
    start_urls = ['http://www.afcfoundation.org']


    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'ngo-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        print('_______________________________________________________________')
        print('SCRAPED DATA:')
        print('_______________________________________________________________')
        print('_______________________________________________________________')

        title = response.xpath('//title/text()').extract_first()
        print title

        contact = response.css("div.contact")
        print contact

        parsedHTML = []
        i = 0
        for x in NGOSpider.start_urls:
            parsedHTML.append(self.getHTMLtext(x))
            i += 1

        phoneNumber = []
        email =[]
        streetAddress = []

        for x in parsedHTML:
            phoneNumber.append(self.getPhoneNumber(x))
            email.append(self.getEmail(x))
            streetAddress.append(self.getAddress(x))

        projectProp = 'PROJECTPROPOSAL'
        print(self.formatJSON(title,phoneNumber,email,streetAddress,projectProp))


        print('_______________________________________________________________')
        print('_______________________________________________________________')



    #getting all text on a page
    def getHTMLtext (self, url):
        page = urllib.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        HTMLtext = soup.get_text()
        return HTMLtext

    #get the phone number on webpage with regex
    def getPhoneNumber (self, webText):
        phoneNumber = ""

        phoneNumberCombinations = r'\(?\d?-?\d{,3}?\)?\s?\.?-?/?\(?\d{3}\)??\s?\.?-?/?\d{3}\s?\.?-?\d{4}'

        #catch index out of range error
        phoneNumber = re.findall(phoneNumberCombinations, webText)

        #print(re.findall(r'\(?\d{3}\)? \d{3}-\d{4}',webText))
        #basic case
        """
        phoneNumberCombos = [r'\(?\d{3}\)? \d{3}-\d{4}', r'\(?\d{3}\)?.?\d{3}.?\d{4}']
        for numbers in phoneNumberCombos:
            phoneNumber = re.findall(numbers, webText)
            print(phoneNumber)
        """
        print(phoneNumber)
        return phoneNumber


    #get email
    def getEmail (self, webText):
        email = ""
        #basic case
        emailCombinations = r'[-\w\d+.]+@[-\w\d.]+'

        #catch index out of range error
        email = re.findall(emailCombinations, webText)[0]
        print(email)
        return email


    #using alg
    def getAddress(self, webText):

        streetNumber = r'\d+'
        state = r'(AL|AK|AS|AZ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT \
                |NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY \
                Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|Florida|Georgia|Hawaii| \
                Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|\
                Minnesota|Mississippi|Missouri|Montana|Nebraska|Nevada|New[ ]Hampshire|New[ ]Jersey|New[ ]Mexico|\
                New[ ]York|North[ ]Carolina|North[ ]Dakota|Ohio|Oklahoma|Oregon|Pennsylvania|Rhode[ ]Island|\
                South[ ]Carolina|South[ ]Dakota|Tennessee|Texas|Utah|Vermont|Virginia|Washington|West[ ]Virginia|Wisconsin|Wyoming)'
        zipCode = r'[ ]+(\b\d{5}(?:-\d{4})?\b)'


        addressAnchor = state + zipCode

        #find address
        address = re.findall(addressAnchor, webText)
        #print address

        stringReform = ''
        index = 0
        addressList = []
        #append string
        for (a,b) in address:
            stringReform = a + ' ' + b
            addressList.append(re.sub("^u'(.*)'$",r'\1',stringReform))
            index += 1

        #print addresses
        #print addressList

        addressFinal = []
        #find position of zipcode
        for x in addressList:
            numberEndLoc = webText.find(x) + len(x) + 1
            #print (webText.find(streetNum))

            #assign starting point for looking for street number
            startSearch = numberEndLoc - 45
            neededText = webText[startSearch:numberEndLoc]

            street_match = re.search(streetNumber,neededText)

            if street_match:
                addressStart = street_match.start()
            else:
                print neededText
                return neededText
            #print addressStart
            #print neededText[addressStart:-1]

            addressFinal.append(neededText[addressStart:])

        print addressFinal
        return addressFinal



    def formatJSON (self,title,phoneNumber,emailAddress,streetAddress,projectProposal):

        data = {
            'Organization Title' : '',
            'Phone Number' : '',
            'Email' : '',
            'Street Address' : [],
            'Project Proposal': ''
        }

        data['Organization Title'] = title
        data['Phone Number'] = phoneNumber
        data['Email'] = emailAddress
        data['Street Address'] = streetAddress
        data['Project Proposal'] = projectProposal

        json_data = json.dumps(data)
        return json_data
        print json_data

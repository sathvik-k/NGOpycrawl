import os
import sys
import feedparser
from bs4 import BeautifulStoneSoup
from bs4 import BeautifulSoup
from nltk import clean_html
import urllib
import re

import scrapy


class NGOSpider(scrapy.Spider):
    name = "ngo"
    start_urls = ['https://achildshopefoundation.org']

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'ngo-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)


        title = response.xpath('//title/text()').extract_first()
        print title

        contact = response.css("div.contact")
        print contact

        parsedHTML = ['']
        i = 0
        for x in NGOSpider.start_urls:
            parsedHTML[i].append(self.getHTMLtext(x))
            i += 1

        phoneNumber = self.getPhoneNumber(parsedHTML[0])
        email =

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
        phoneNumber = re.findall(phoneNumberCombinations, webText)[0]

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


    def formatJSON (self,title,phoneNumber,emailAddress,streetAddress,projectProposal):
        data = {
            'Organization Title' : '',
            'Phone Number' : '',
            'Email' : '',
            'Street Address' : '',
            'Project Proposal': ''
        }

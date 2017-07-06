# NGOpycrawl

Get source code at:
git clone https://github.com/koneman/NGOpycrawl.git


Package dependencies:
Scrapy - read documentation at
pip install scrapy

Beatiful Soup - read docs at
pip install bs4

cd NGOpycrawl/NGOcrawler/spiders

then run:
python callService.py <NGO url>

This will relevant JSON web data:

e.g. -
JSON DATA: {"Organization Title": ["Alliance for Children Foundation", "Sponsor a Child", "Taiwan", "Russia", "USA", "Donate", "Vietnam", "Contact Us", "Who We Are", "Our Staff", "Media"], "Phone Number": [[" (781) 444-7148"], [" (781) 444-7148"]], "Email": [["Bonnie@allforchildren.org"], ["bonnie@allforchildren.org."], ["zlee@afcfoundation.org"], ["info@allforchildren.org."]], "Street Address": [["02494\n"], ["17 Oak Street\r\n        Needham, MA 02492 "]]}

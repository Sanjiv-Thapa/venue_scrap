# weddingspot site scraper
This is a scrapy and selenium based web scraper to extract the wedding venue details. It extracts the venue name,phone,highlights,capacity and address from venue detail page.
---
## what it scrapes 
for each venue, it collects
- URL of the venue page
- venue name
- phone number (digits only)
- venue highlights(comma-seperated format)
- guest capacity(only number)
- full address

---
## how to set up
1.**clone the repo**
```
git clone https://github.com/yourusername/weddingspot_scraper.git
cd wedding_venues
```
2.**install dependencies**

```
pip install -r requirements.txt
```
3.**how to run the spider**
```
scrapy crawl venue
```


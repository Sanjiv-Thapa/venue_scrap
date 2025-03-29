# weddingspot site scraper
This is a scrapy and selenium based web scraper to extract the wedding venue details.The site is[link](https://www.wedding-spot.com/wedding-venues/?pr=new%20jersey&r=new%20jersey%3anorth%20jersey&r=new%20jersey%3aatlantic%20city&r=new%20jersey%3ajersey%20shore&r=new%20jersey%3asouth%20jersey&r=new%20jersey%3acentral%20jersey&r=new%20york%3along%20island&r=new%20york%3amanhattan&r=new%20york%3abrooklyn&r=pennsylvania%3aphiladelphia&sr=1)
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


import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
import time
import re

class VenueSpider(scrapy.Spider):
    name = 'venue'

    start_urls = [
        'https://www.wedding-spot.com/wedding-venues/?pr=new%20jersey&r=new%20jersey%3anorth%20jersey&r=new%20jersey%3aatlantic%20city&r=new%20jersey%3ajersey%20shore&r=new%20jersey%3asouth%20jersey&r=new%20jersey%3acentral%20jersey&r=new%20york%3along%20island&r=new%20york%3amanhattan&r=new%20york%3abrooklyn&r=pennsylvania%3aphiladelphia&sr=1'
    ]

    custom_settings = {
        'FEED_URI': 'venues.csv',
        'FEED_FORMAT': 'csv',
        'DOWNLOAD_DELAY': 1,
        'LOG_LEVEL': 'INFO'
    }

    def __init__(self):
        options = Options()
        options.add_argument("--headless")  # Headless mode
        options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=options)

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(3)

        scraped_links = set()

        while True:
            current_url = self.driver.current_url
            self.logger.info(f"Scraping page: {current_url}")

            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.venueCard--wrapper a'))
                )
            except:
                self.logger.warning("Venue cards did not load.")
                break

            page_source = self.driver.page_source
            selenium_response = HtmlResponse(url=current_url, body=page_source, encoding='utf-8')

            venue_links = selenium_response.css('div.venueCard--wrapper > a::attr(href)').getall()
            new_links = [link for link in venue_links if link not in scraped_links]

            if not new_links:
                self.logger.info("No new venues found. Stopping.")
                break

            for link in new_links:
                full_url = response.urljoin(link)
                scraped_links.add(link)
                yield scrapy.Request(url=full_url, callback=self.parse_venue)

            try:
                next_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Next Page"]'))
                )
                if not next_button.is_enabled():
                    self.logger.info("Next button is disabled. Ending pagination.")
                    break
                self.driver.execute_script("arguments[0].click();", next_button)
                time.sleep(3)
            except:
                self.logger.info("No more pages or failed to click next.")
                break

    def parse_venue(self, response):
        self.driver.get(response.url)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "SecondaryCTA--venueName"))
            )
        except:
            self.logger.warning(f"Timed out waiting for venue content at: {response.url}")

        venue_html = self.driver.page_source
        venue_response = HtmlResponse(url=response.url, body=venue_html, encoding='utf-8')

        name = venue_response.xpath('//div[@class="SecondaryCTA--venueName"]/text()').get(default="").strip()

        raw_phone = venue_response.xpath('//a[@id="call-venue"]//span[contains(@class, "SecondaryCTA--hidden")]/text()').get(default="").strip()
        phone = re.sub(r'\D', '', raw_phone)

        highlights = venue_response.xpath('//h3[contains(text(), "Venue highlights")]/following-sibling::div//div[contains(@class, "VenueHighlights--label")]/text()').getall()
        highlights = ', '.join([h.strip() for h in highlights])

        raw_capacity = venue_response.xpath('//h3[contains(text(), "Guest capacity")]/following-sibling::p/text()').get(default="").strip()
        capacity_match = re.search(r'\d+', raw_capacity)
        capacity = capacity_match.group() if capacity_match else ''

        address_lines = venue_response.xpath('//h3[contains(text(), "Location")]/following-sibling::p//text()').getall()
        address = ' '.join([line.strip() for line in address_lines if line.strip()])

        yield {
            'url': response.url,
            'name': name,
            'phone': phone,
            'highlights': highlights,
            'capacity': capacity,
            'address': address
        }

    def closed(self, reason):
        self.driver.quit()

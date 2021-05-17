from tkinter import *
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
import threading

root = Tk()
root.title("Amazon Filter")
root.resizable(False, False)

def getURL(product, page):
    product = product.replace(' ', '+')
    return f'https://www.amazon.com/s?k={product}&ref=nb_sb_noss_1&page={page}'

def extractItemInfo(searchItem, maxPages, minPrice, maxPrice, minRating, minNumReviews):
    csv_file = open('amazon_filter_scrape.csv', 'w', encoding="utf-8")
    html_file = open('amazon.html', 'w', encoding="utf-8")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['description', 'rating', 'number of reviews', 'price', 'link'])
    html_file.write("""<html><head></head><body>""")

    driver = webdriver.Chrome('C:\\Users\Kyle Ruiz\\Documents\Selenium Driver\\chromedriver.exe')

    for page in range(1, maxPages):
        url = getURL(searchItem, page)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        items = soup.find_all('div', {'data-component-type': 's-search-result'})
        for item in items:
            description = item.h2.a.text.strip()
            url = 'https://www.amazon.com' + item.h2.a.get('href')
            try:
                price = item.find('span', 'a-price').find('span', 'a-offscreen').text[1:6]
                rating = item.i.text[0:4]
                numReviews = item.find('span', {'class': 'a-size-base'}).text.replace(',', '')
            except AttributeError:
                price = 0
                rating = 0
                numReviews = 0
            try:
                price = float(price)
                rating = float(rating)
                numReviews = float(numReviews)
            except ValueError:
                price = 0
                rating = 0
                numReviews = 0
            if (minPrice <= price <= maxPrice) and (rating >= minRating) and (numReviews >= minNumReviews):
                csv_writer.writerow([description, rating, numReviews, price, url])
                html_file.write(f"""
                    <a href={url}><p>{rating} / {numReviews} <br> {description} {price}</p></a> <br> <hr>
                    """)

    csv_file.close()
    html_file.write("""</body></html>""")
    html_file.close()
    driver.close()

def buttonClicked():
    searchItem = productTextField.get()
    maxPages = pageTextField.get()
    minPrice = minPriceTextField.get()
    maxPrice = maxPriceTextField.get()
    minRating = reviewChoice.get()
    minNumReviews = minReviewTextField.get()

    if minRating == "★★★★ & up":
        minRating = 4.0
    elif minRating == "★★★ & up":
        minRating = 3.0
    elif minRating == "★★ & up":
        minRating = 2.0
    elif minRating == "★ & up":
        minRating = 1.0

    maxPages = int(maxPages)
    minPrice = float(minPrice)
    maxPrice = float(maxPrice)
    minNumReviews = int(minNumReviews)

    t1 = threading.Thread(target=extractItemInfo, args=[searchItem, maxPages, minPrice, maxPrice, minRating, minNumReviews])
    t1.start()


# GUI code
dealsChoice = StringVar()
reviewChoice = StringVar(root)
options = ["★★★★ & up", "★★★ & up", "★★ & up", "★ & up"]
ratingOptionMenu = OptionMenu(root, reviewChoice, *options)
reviewChoice.set(options[0])

productLabel = Label(root, text="Enter an Amazon Item: ", font=("Arial", 12))
ratingLabel = Label(root, text="Customer Review: ", font=("Arial", 12))
minPriceLabel = Label(root, text="Minimum Price: ", font=("Arial", 12))
maxPriceLabel = Label(root, text="Maximum Price: ", font=("Arial", 12))
minReviewsLabel = Label(root, text="Minimum Reviews: ", font=("Arial", 12))
productTextField = Entry(root, width=32, font=("Arial", 12))
minReviewTextField = Entry(root, width=13, font=("Arial", 12))
minPriceTextField = Entry(root, width=13, font=("Arial", 12))
maxPriceTextField = Entry(root, width=13, font=("Arial", 12))
pagesLabel = Label(root, text="Pages Scraped: ", font=("Arial", 12))
pageTextField = Entry(root, width=13, font=("Arial", 12))
csvButton = Button(root, text="Generate CSV File", padx=5, pady=5, command=buttonClicked)

productLabel.grid(row=0, column=0, sticky="E")
ratingLabel.grid(row=1, column=0, sticky="E")
minReviewsLabel.grid(row=2, column=0, sticky="E")
minPriceLabel.grid(row=3, column=0, sticky="E")
maxPriceLabel.grid(row=4, column=0, sticky="E")
pagesLabel.grid(row=5, column=0, sticky="E")

productTextField.grid(row=0, column=1, sticky="W")
ratingOptionMenu.grid(row=1, column=1, sticky="W")
minReviewTextField.grid(row=2, column=1, sticky="W")
minPriceTextField.grid(row=3, column=1, sticky="W")
maxPriceTextField.grid(row=4, column=1, sticky="W")
pageTextField.grid(row=5, column=1, sticky="W")

csvButton.grid(row=6, column=1, sticky="E")

root.geometry("475x190")
root.mainloop()

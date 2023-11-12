from bs4 import BeautifulSoup
import click
import datetime


@click.command()
@click.option('--file', prompt='HTML note', help='The path to the Play Books-generated HTML file to be parsed.')
def main(file):
    
    with open(file, "r") as html_file:
        html = html_file.read()
        
        soup = BeautifulSoup(html, 'html.parser')

        book_title_h1 = soup.find("h1")
        book_title = book_title_h1.find("span").text.strip()

        print(book_title)
        
        author_p = soup.findAll("p")[2]
        author = author_p.find("span").text.strip()
        
        publisher_p = soup.findAll("p")[3]
        publisher = publisher_p.find("span").text.strip()
        
        print(author + ", " + publisher)
        
        last_synced_string = soup.find("span", string=lambda text: text and "Last synced" in text).text.strip()
        last_synced_string = last_synced_string.replace('– Last synced ', '')
        last_synced = datetime.datetime.strptime(last_synced_string, "%B %d, %Y")
        
        print(last_synced)
        
        
    
    
if __name__ == '__main__':
    main()
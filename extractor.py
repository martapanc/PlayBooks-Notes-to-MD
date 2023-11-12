from bs4 import BeautifulSoup
import click
import datetime
import re


def rename_file(file):
    file_name = file.replace(".html", "").replace("Notesfrom", "").replace("Noterelativeallibro", "")
    split = re.findall('[A-Z][^A-Z]*', file_name)
    
    return "output/Notes - {0}.md".format(" ".join(split))
    
    
@click.command()
@click.option('--file', prompt='HTML note', help='The path to the Play Books-generated HTML file to be parsed.')
def main(file):
    
    with open(file, "r") as html_file:
        html = html_file.read()
        
    html = html.replace("Data ultima sincronizzazione", "Last synced")
    html = html.replace("Tutte le tue annotazioni", "All your annotations")
        
    soup = BeautifulSoup(html, 'html.parser')
    
    output_file_name = rename_file(file)
    output_md = open(output_file_name, "w")

    book_title_h1 = soup.find("h1")
    book_title = book_title_h1.find("span").text.strip()

    output_md.write("# {0}\n\n".format(book_title))
    
    author_p = soup.findAll("p")[2]
    author = author_p.find("span").text.strip()
    
    output_md.write("### by {0}".format(author))
    
    publisher_p = soup.findAll("p")[3]
    publisher = publisher_p.find("span").text.strip()
    
    if publisher:
        output_md.write(", published by {0}".format(publisher))
        
    output_md.write("\n---\n")
    
    last_synced_string = soup.find("span", string=lambda text: text and "Last synced" in text).text.strip()
    last_synced_string = last_synced_string.replace('– Last synced ', '')
        
    notes_start_h1 = soup.find('h1', string='All your annotations')
    if notes_start_h1:
        note_tables = notes_start_h1.findAllNext('table')
        
        # Process every 2nd table, as each note is a nested table, and each 2nd is the child of each 1st
        for i in range(1, len(note_tables), 2):
            note_table = note_tables[i]
            
            note_span_list = note_table.findAll("span")
            
            note_content = note_span_list[1].text.strip()
            date = note_span_list[3].text.strip()
            page = note_span_list[4].text.strip()
            
            output_md.write("> {0}\n".format(note_content))
            output_md.write("(Page {0})\n\n".format(page))

            # print("{0} (page {1}) - {2}".format(note_content, page, date))
    
    output_md.write("\n---\nNotes last updated on {0}".format(last_synced_string))
    output_md.close()            
            

if __name__ == '__main__':
    main()
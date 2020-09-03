from bs4 import BeautifulSoup

def number_from_string(string):
    string = string.split(' ')
    num = None
    for word in string:
        try:
            num = int(word)
        except ValueError:
            pass
    return num

def parse_html(html_str):
    soup = BeautifulSoup(html_str, 'html.parser')
    dashboard_numbers_section = soup.find_all('section')[4] 
    headings = dashboard_numbers_section.find_all('h1')
    cumulative_cases = headings[0].get_text()
    percent_space_used = headings[1].get_text()
    total_beds_str = dashboard_numbers_section.find_all('small')[1].get_text()
    total_beds = number_from_string(total_beds_str)
    results_dict = {
        'cumulative_cases': cumulative_cases, 'total_beds':total_beds, 'perecent_space_used':percent_space_used
    }
    return results_dict


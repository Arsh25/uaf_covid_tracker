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
    sections = soup.find_all('section')
    dashboard_numbers_section = sections[4]
    cumulative_cases_section =  sections[6]
    headings = cumulative_cases_section.find_all('h1')
    cumulative_cases_div = headings[0].find_all('div')[0]
    cumulative_cases = cumulative_cases_div.get_text()
    percent_space_used = dashboard_numbers_section.find_all('h1')[1].find_all('div')[0].get_text()
    total_beds_str = dashboard_numbers_section.find_all('small')[1].get_text()
    total_beds = number_from_string(total_beds_str)
    results_dict = {
        'cumulative_cases': cumulative_cases, 'total_beds':total_beds, 'percent_space_used':percent_space_used
    }
    return results_dict


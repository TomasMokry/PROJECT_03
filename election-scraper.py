"""
treti projekt do Engeto Online Python Akademie
author: Tomáš Mokrý
email: tomas.mokry@gmail.com
discord: Tomas M#0922

"""
import sys
import requests
import csv
import copy
from bs4 import BeautifulSoup

argument_1 = sys.argv[1]
argument_2 = sys.argv[2]

def main():
    soup = get_soup(argument_1)
    relative_links = find_all_a_href(soup)
    full_addresses_main_page = compile_full_address(relative_links)
    soups_mp = soup_generator_complex(full_addresses_main_page)
    relative_links_list = find_all_sub_a_href(soups_mp,relative_links)
    full_addresses_list = compile_full_address(relative_links_list)
    soups_all = soup_generator_complex(full_addresses_list)
    all_political_parties = find_all_political_parties(soups_all)
    result_1 = find_all_code_location(soup)
    result_2 = find_all_reg_evn_val(soups_all)
    result_3 = find_all_pol_parties_results(soups_all,all_political_parties)
    final_result_dictionary = join_results(result_1, result_2, result_3)
    write_data_to_csv(final_result_dictionary, argument_2)
    print('ENDING election-scraper')

def get_soup(url: str):
    """
    Takes url and returns soup

    :return: bs4.BeautifulSoup
    """
    answer = requests.get(url)
    print(f'DOWNLOADING DATA FROM URL: {url}')
    return BeautifulSoup(answer.text, 'html.parser')

def get_atribut_code_location(tr_tag: "bs4.element.ResultSet") -> dict:
    """
    From every row (tr) takes certain cells (td)[index]
    and wrap into dict
    
    :return: dict
    """
    return {
        'code' : tr_tag[0].get_text(),
        'location' : tr_tag[1].get_text()
    }

def find_all_code_location(soup: "bs4.BeautifulSoup") -> list:
    """
    From every table takes all municipalies numbers and locations.
    Takes values from 1st and 2nd columns and creates list with dicts
    
    :return:
    [{'code':'506761', 'location':'Alojzov'},{..},{..}...]
    """
    return [
        get_atribut_code_location(tr.find_all("td"))
        for table in soup.find_all("table", {"class": "table"})
        for tr in table.find_all('tr')[2:]
        if get_atribut_code_location(tr.find_all("td"))['code'] != '-'
        or get_atribut_code_location(tr.find_all("td"))['location'] != '-'
    ]

def find_all_a_href(soup: "bs4.BeautifulSoup") ->list:
    """
    In every table finds all a hrefs 'X', store them into list.

    :return: list
    """
    return [
        i['href'] for table in soup.find_all("table", {"class": "table"}) 
        for i in table.find_all('a', href=True) if i.get_text()=='X'
        ]

def compile_full_address(relative_link_list: list) ->list:
    """
    Iterates though the list or nested list of relative links. 
    From each relative link creates complete link. 
    Works for simple list or nested list.

    :return: list or nested list    
    """
    full_addresses = []
    for i in relative_link_list:
        if type(i) is not list:
            full = f"https://www.volby.cz/pls/ps2017nss/{i}"
            full_addresses.append(full)
        elif type(i) is list:
            sub_list = []
            for j in i:
                full = f"https://www.volby.cz/pls/ps2017nss/{j}"
                sub_list.append(full)
            full_addresses.append(sub_list)
    return full_addresses

def soup_generator_complex(address_list: list) ->list:
    """
    Iterates though list or nested list of links.
    From every link creates soup.

    :return: list or nested list 
    """
    soups=[]
    for i in address_list:
        if type(i) is not list:
            answer = requests.get(i)
            soups.append(BeautifulSoup(answer.text, 'html.parser'))
        elif type(i) is list:
            sub_list_soups = []
            for j in i:
                answer = requests.get(j)
                sub_list_soups.append(BeautifulSoup(answer.text, 'html.parser'))
            soups.append(sub_list_soups)
    return soups

def find_all_sub_a_href(soups: list, relative_links: list) -> list:
    """
    Iterates though soups and checking the title of the page.
    If the soup is from the main page it appends relative link to list.
    If the soup is from the subpage it finds all a hrefs and appends
    the relative links to the nested list.
    
    :return: nested list
    ['rel. link main page',['rel. link subpage 1', 'rel. link subpage 2']]
    """
    title_main = 'Výsledky hlasování za územní celky | volby.cz'
    title_sub = 'Výsledky hlasování za územní celky – výběr okrsku | volby.cz'
    links = []
    for i,soup in enumerate(soups):
        if soup.title.get_text() == title_main:
            links.append(relative_links[i])
        elif soup.title.get_text() == title_sub:
            table = soup.find("table", {"class": "table"})
            links.append([i['href'] for i in table.find_all('a', href=True)])
    return links

def get_atribut_pol_parties(tr_tag: "bs4.element.ResultSet") -> str:
    """
    From every row (tr) takes certain cells (td)[index]
    and resturn string
    
    :return: string
    """
    return tr_tag[1].get_text()

def find_all_political_parties(soups: list) ->dict:
    """
    Iterates though the soups. Soups in list are from the main page
    soups in sublist are from subpages. Finds all political parties
    from all soups and store them into dictionary.

    :return: dict
    {'ANO' : 0, 'ODS' : 0, 'REALISTE' : 0...}
    
    """
    parties = {}
    for soup in soups:
        if type(soup) is not list:
            for table in soup.find_all("table", {"class": "table"})[1:]:
                for tr in table.find_all('tr')[2:]:
                    row_data = get_atribut_pol_parties(tr.find_all("td"))
                    if row_data not in parties and row_data != '-':
                        parties[row_data] = 0
                        parties.update(parties)
        elif type(soup) is list:
            for i in soup:
                for table in i.find_all("table", {"class": "table"})[1:]:
                    for tr in table.find_all('tr')[2:]:
                        row_data = get_atribut_pol_parties(tr.find_all("td"))
                        if row_data not in parties and row_data != '-':
                            parties[row_data] = 0
                            parties.update(parties)
    return parties

def get_atribut_reg_env_val_main(tr_tag: "bs4.element.ResultSet") -> dict:
    """
    From every row (tr) takes certain cells (td)[index]
    and wrap into dict
    
    :return: dict
    """
    return {
        'registred' : tr_tag[3].string.replace('\xa0', ''), 
        'envelopes' : tr_tag[6].get_text(strip=True), 
        'valid' : tr_tag[7].get_text(strip=True)
        }
    
def get_atribut_reg_env_val_sub(tr_tag: "bs4.element.ResultSet") -> dict:
    """
    From every row (tr) takes certain cells (td)[index]
    and wrap into dict
    
    :return: dict
    """
    return {
        'registred' : tr_tag[0].string.replace('\xa0', ''), 
        'envelopes' : tr_tag[1].get_text(strip=True), 
        'valid' : tr_tag[4].get_text(strip=True)
        }
    
def find_all_reg_evn_val(soups: list) -> list:
    """
    From soup of main page find all registred, envelopes, valid and appends
    the dictionary into list.
    From soup of subpages find all registred, envelopes, valid,
    sums values from subpages into one dictionary

    :return: list with dictionaries
    [{'registred' : 25, 'envelopes' : 12, 'valid' : 3}, {..}, {..}]
    
    """
    results = []
    for soup in soups:
        if type(soup) is not list:
            for tr in soup.find("table", {"class": "table"}).find_all('tr')[2:]:
                results.append(get_atribut_reg_env_val_main(tr.find_all("td")))
        elif type(soup) is list:
            draft_dict = {'registred':0,'envelopes':0,'valid':0}
            for i in soup:
                all_tr = i.find("table", {"class": "table"}).find_all('tr')
                row_data = get_atribut_reg_env_val_sub(all_tr[1].find_all("td"))
                draft_dict['registred'] += int(row_data['registred'])
                draft_dict['envelopes'] += int(row_data['envelopes'])
                draft_dict['valid'] += int(row_data['valid'])
            results.append(draft_dict)
    return results

def find_all_pol_parties_results(soups: list,all_parties: dict) -> list:
    """
    Iterates though the soups, finds all political party name and result,
    checking if the party is in all_parties dict. 
    If yes it updates value for each key. 
    Does the same for soup for main page - in main soups list
    and for soup for subpage - in nested soups list

    :result: list with dictionaries
    [{'ANO' : 25, 'ODS' : 12, 'REALISTE' : 3, ...}, {..}, {..}]
    """
    political_parties_results = []
    for soup in soups:
        if type(soup) is not list:
            dict_draf_1 = copy.deepcopy(all_parties)
            for table in soup.find_all("table", {"class": "table"})[1:]:
                for tr in table.find_all('tr')[2:]:
                    row_data = get_atribut_party_result(tr.find_all("td"))
                    if row_data[0] in dict_draf_1:
                        dict_draf_1[row_data[0]] = row_data[1]
            political_parties_results.append(copy.deepcopy(dict_draf_1))
        elif type(soup) is list:
            dict_draft_2 = copy.deepcopy(all_parties)
            for i in soup:
                for table in i.find_all("table", {"class": "table"})[1:]:
                    for tr in table.find_all('tr')[2:]:
                        row_data = get_atribut_party_result(tr.find_all("td"))
                        if row_data[0] in dict_draft_2:
                           dict_draft_2[row_data[0]] += int(row_data[1])
            political_parties_results.append(copy.deepcopy(dict_draft_2))
    return political_parties_results

def get_atribut_party_result(tr_tag: "bs4.element.ResultSet") -> list:
    """
    From every row (tr) takes certain cells (td)[index]
    and wrap into list
    
    :return: list
    """
    return [tr_tag[1].get_text(), tr_tag[2].get_text()]

def write_data_to_csv(data: list, file_name: str):
    """
    Takes list of dictionaries and write and save to csv file.
    """
    with open(file_name, mode='w',encoding='utf-8', newline='') as f:
        col_names = data[0].keys()
        csv_writer = csv.DictWriter(f, fieldnames=col_names)
        csv_writer.writeheader()
        csv_writer.writerows(data)
        print(f'SAVING DATA TO {file_name}')

def join_results(result_1: list, result_2: list, result_3: list) -> list:
    """
    takes 3 lists with dictionaries and join into one.

    result: list of dictionaries.
    
    """
    for i,results in enumerate(result_1):
        results.update(result_2[i])
        results.update(result_3[i])
    return result_1


if __name__ == "__main__":
    main()

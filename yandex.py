import bs4, requests, webbrowser

move_site_list = ['kinogo.by', 'baskino.me', 'seasonvar.ru']

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/73.0.3683.86 Chrome/73.0.3683.86 Safari/537.36'
}


def get_move_link(user_req, move_site):
    start_url = 'https://yandex.by/search/?text=site%3A'
    search_url = start_url + move_site + '%20' + user_req

    with requests.Session() as s:
        resp = s.get(search_url, headers=headers)

    soup = bs4.BeautifulSoup(resp.text, 'lxml')
    block = soup.find('li', class_='serp-item')
    

    move_link = block.select('h2 a')[0].get('href')
    move_title = block.find('div', class_='organic__url-text').get_text()
    try:
        move_text = block.find('span', class_='extended-text__full').get_text()[:-7]
    except AttributeError:
        move_text = block.find('div', class_='organic__content-wrapper').find('div').get_text()


    return move_title, move_text, move_link



def check_title_filter(user_req, move_title):
    if user_req in move_title or user_req.capitalize() in move_title:
        return True
    else: return False


def check_keywords_filter(user_req, move_title, move_text):
    list_of_keywords = user_req.split()
    coincidence = 0
    for keyword in list_of_keywords:
        if keyword in move_title or keyword in move_text:
            coincidence += 1
        if keyword.capitalize() in move_title or keyword.capitalize() in move_text:
            coincidence += 1
        if keyword.upper() in move_title or keyword.upper() in move_text:
            coincidence += 1

    print(coincidence)
    if coincidence > len(list_of_keywords) - 1:
        return True
    else: return False



def main():
    #user_req = 'малена'
    #user_req = 'побег из шоушенка'
    user_req = 'тротуарная империя'
    for move_site in move_site_list:
        move_title, move_text, move_link = get_move_link(user_req, move_site)
        if check_title_filter(user_req, move_title) == True:
            webbrowser.open(move_link)
            print(move_link)
            return move_link
        elif check_keywords_filter(user_req, move_title, move_text) == True:
            print(move_link)
            webbrowser.open(move_link)
            return move_link
        else: continue





if __name__ == '__main__':
    main()











import requests
from fake_headers import Headers
import bs4

def bs4_soup(link):
    '''
    Функция возвращает объект BeautifulSoup
    '''
    response = requests.get(link,
                 headers=Headers(browser='chrome', os='windows').generate())

    soup = bs4.BeautifulSoup(response.text, features='lxml')
    return soup

def params(article):
    '''
    Функция возвращает словарь с датой и временем выхода статьи,
    заголовком статьи и ссылкой на статью
    '''
    # Из тега time получается datetime    
    date = article.select_one('time')['datetime']
    # Форматируется в удобное представление
    formatted_date = f'{date[8:10]}-{date[5:7]}-{date[:4]} в {date[11:19]}'
    
    # Из класса tm-title получается текстовое представление заголовка статьи
    title = article.select_one('.tm-title').text
     
    # Для получения абсолютной ссылки на статью осуществляется конкатенация
    # адреса сайта и относительной ссылки на статью
    link = 'https://habr.com' + article.select_one('a.tm-title__link')['href']
    
    # Возвращается необходимый словарь   
    return {'date': formatted_date, 'title': title, 'url': link}

def keyword_match(article, keywords):
    '''
    Функция возвращает словарь с датой и временем выхода статьи,
    заголовком статьи и ссылкой на статью, в том случае если в названии
    или тексте указанной статьи, встречается хотя бы одно из ключевых слов
    '''
    # Текстовое представление заголовка, принятого на вход объекта статьи,
    # сравнивается с каждым словом из принятого на вход списка ключевых слов. 
    # В случае совпадения, вызывается функция params()
    if any(keyword in article.text.lower() for keyword in keywords):
            return params(article)
        
    # Иначе "собирается" абсолютная ссылка на статью
    else:
        link = 'https://habr.com' + article.select_one('a.tm-title__link')['href']
        
        # Получается объект BeautifulSoup статьи 
        article_soup = bs4_soup(link)
        
        # Текстовое представление статьи сравнивается с каждым словом из 
        # принятого на вход списка ключевых слов. 
        # В случае совпадения, вызывается функция params()
        if any(keyword in article_soup.text.lower() for keyword in keywords):
            return params(article)


if __name__ == '__main__':
    
    # Список ключевых слов:
    keywords = ['дизайн', 'фото', 'web', 'python']
    
    # Адрес сайта, с которого получаются названия статей
    url = 'https://habr.com/ru/articles'
    
    # Объект BeautifulSoup
    soup = bs4_soup(url)
    
    # Объект со статьями, указанными на странице сайта
    articles = soup.select('article.tm-articles-list__item')
    
    # Список статей, в названиях или тексте которых, 
    # встречается хотя бы одно из ключевых слов
    parsed_data = [keyword_match(article, keywords) for article in articles 
                   if keyword_match(article, keywords)]
    
    # Вывод в консоль списка названий статей в указанном формате           
    for article in parsed_data:
        print(f'{article["date"]} – {article["title"]} – {article["url"]}')

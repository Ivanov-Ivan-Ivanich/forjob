import requests

from bs4 import BeautifulSoup

import config
from model import save_db


def get_html(url):
    try:
       result = requests.get(url)
       result.raise_for_status()
        
       return result.text
    except(ValueError, TypeError, requests.RequestException):
        return False


def get_adverts(link):
    html=get_html(link)
    if html:
        soup=BeautifulSoup(html,"html.parser")
        advs=soup.find_all("tr", class_='wrap')

        
        all_advs={}
        adv=[]
        for advert in advs:

            title = advert.find('h3', class_='lheight22 margintop5').text
            
            all_advs['title']=title.strip()
           
            
            try:
                price = advert.find('p',class_='price').text
                all_advs['price']=price.strip()
                
            except AttributeError:
                price='Не указана'
                all_advs['price']=price
               
    

            try:
                img = advert.find('img')['src']
                all_advs['img']=img.strip()
            except TypeError:
                img='None'
                all_advs['img']=img

            url=advert.find('a',attrs={"data-cy":"listing-ad-title"})['href']
            all_advs['url']=url.strip()

            botom=advert.find('td', class_='bottom-cell')
            location = botom.find('span').text
            all_advs['location']=location.strip()
                
            page = advert.find('li', aria_laqbel = 'Page 3')
            all_advs['page']  = page 
            adv.append(all_advs)
            
            all_advs={}
    
    return adv
   

  
        
          
if __name__ == '__main__':
    get_adverts()
    

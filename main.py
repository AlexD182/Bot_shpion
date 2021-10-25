from bs4.formatter import XMLFormatter
import requests
from bs4 import BeautifulSoup as BS
import datetime
from DelayFunc import every
import threading




###
import bot_slave
import data_input as di

STAT = []

##    TOOLS
#-------------------------------------------------------------------- 
def GetSysytemTime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
#--------------------------------------------------------------------   
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""





def get_page_csr(url):
    _data = {}
    s = requests.Session()
    response = s.get(url=url, headers = di.headers)
    html = BS(response.content, "html.parser")
    productCard = html.find_all("div", class_="product-card__content")

    for pd in productCard:
        productName =  pd.find_all("div", class_="product-card__media")[0]        
        productInfo =  pd.find_all("span", itemprop="name")
        productSize =  pd.find_all("ul", class_="product-sizes__list")
        productPrice =  pd.find_all("span", class_="price__value")

        productName = find_between(str(productName),"href=", "><picture").replace(" ",'').replace('"',"")

        Size = str(productSize[0].text).split()

        if(False):
            print("Product name: ", productName)
            print("INFO:    ", productInfo[0].text)
            print("Size:    ", Size)
            print("Price:    ", productPrice[0].text)
            if ( len(productPrice) > 1):
                print("Price disc:    ", productPrice[1].text)
            print("===============")
        
        _data = {}
        _data["id"] = productName
        _data["Info"] = productInfo[0].text
        _data["Size"] = Size
        _data["Price"] = productPrice[0].text
        if ( len(productPrice) > 1):
            _data["PriceDiscount"] = productPrice[1].text

        if _data not in STAT:
            STAT.append(_data)   
    
    #with open("index_csr.html", "w") as file:
    #    file.write(response.text)


     

def collect_data(_url, _pagination_count):
    for page_count in range(1, _pagination_count): 
        get_page_csr(url=_url+str(page_count))    
    
    return STAT

def find_wishes(wishes, products):
    _foundList = []
    for element in wishes:
        #print ("Search: " ,element)
        for product in products:
            #print ('    Cur product: ', product)                
            if ( element['id'] in product['id']):
                for size in product['Size']:
                    if( size == element['Size']):
                        #print("Find!", product)
                        _foundList.append(product)
        
    return _foundList

def result_to_msg(result):
    _msg =[]
    if(result):                     
        for el in result:                
            info = str( el['Info'] + "\n" +
                        'Size:  ' + str(el['Size']).replace("[", "").replace("]", "").replace("'", "") +"\n" +
                        'Price:  ' + el['Price'] + "\n") 

            if ("PriceDiscount" in el):
                info += 'Price Discount:  ' + el["PriceDiscount"] + "🔥🔥🔥" + '\n'

            info += di.UP_url + el['id']
            _msg.append(info)
            #return card
            #telegram_bot_sendtext(card)        
    else:
        _msg.append("Wishes not found in products!")
    return _msg


def telegram_bot_sendtext(bot_message):
    print( GetSysytemTime(), " Send msg from bot: ", bot_message.replace('\n','') )  
    send_text = 'https://api.telegram.org/bot' + di.TOKEN + '/sendMessage?chat_id=' + di.bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()


def report():
    
    UP_data = collect_data(di.UP_url_parks, di.UP_pagination_count)
    UP_result = find_wishes(di.UP_wishes, UP_data)
    UP_massenges = result_to_msg(UP_result)

    for text in UP_massenges:  
        telegram_bot_sendtext(text)



def main():
    print( GetSysytemTime(), "  Server start")

    threading.Thread(target=lambda: every(20, report)).start()
    bot_slave.main()

       

    
if __name__ == "__main__":
    main()

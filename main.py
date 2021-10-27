from bs4.formatter import XMLFormatter
import requests
from bs4 import BeautifulSoup as BS
import datetime
from DelayFunc import every
import threading




###
import bot_slave
import data_input as di



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
    
    STAT = []
    s = requests.Session()
    response = s.get(url=url, headers = di.headers)

    if(response.ok):
        print(GetSysytemTime(), " Response ok! ::", url)
        html = BS(response.content, "html.parser")
        productCard = html.find_all("div", class_="product-card__content")

        for pd in productCard:
            productName =  pd.find_all("div", class_="product-card__media")[0]        
            productInfo =  pd.find_all("span", itemprop="name")
            productSize =  pd.find_all("ul", class_="product-sizes__list")
            productPrice =  pd.find_all("span", class_="price__value")

            productName = find_between(str(productName),"href=", "><picture").replace(" ",'').replace('"',"")

            Size = str(productSize[0].text).split()

            #logging
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
        
        print(GetSysytemTime(), " Found products:", len(STAT))
        return STAT
    
    #with open("index_csr.html", "w") as file:
    #    file.write(response.text)
    else:
        return str(GetSysytemTime()) + " : No response! : " + url + " : Error code: " + str(response.status_code)



     

def collect_data_in_page(_url, _pagination_count):
    _data_out = []
    for page_count in range(1, _pagination_count): 
        _page_data = get_page_csr(url=_url+str(page_count))
        _data_out.extend( _page_data )        
        
        if("No response!" in _page_data):
            print(_page_data)   #LOG
            return telegram_bot_sendtext(_page_data)
    print(str(GetSysytemTime()), " -- Total products: ", len(_data_out)) #LOG
    return _data_out

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
    else:
        _msg.append("Wishes not found in products!")
    return _msg


def telegram_bot_sendtext(bot_message):
    print( str(GetSysytemTime()), " Send msg from bot: ", bot_message.replace('\n','') ) #LOG 
    send_text = 'https://api.telegram.org/bot' + di.TOKEN + '/sendMessage?chat_id=' + di.bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()


def report():    
    UP_data = collect_data_in_page(di.UP_url_parks, di.UP_pagination_count)
    UP_result = find_wishes(di.UP_wishes, UP_data)

    if(UP_result):
        UP_massenges = result_to_msg(UP_result)
        for text in UP_massenges:  
            telegram_bot_sendtext(text)
    else:      
        print(str(GetSysytemTime()), " Nothing founded in products!") #LOG
        telegram_bot_sendtext("Nothing founded in UP products!\n Looking for:\n" + str(di.UP_wishes))

            



def main():
    print( GetSysytemTime(), " :: Server start ::")
    
    timeDelay = 21600 #6h
    threading.Thread(target=lambda: every(15, report)).start()

    #Start bot
    bot_slave.main()
    

       

    
if __name__ == "__main__":
    main()

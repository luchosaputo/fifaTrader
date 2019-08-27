from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, json, msvcrt, winsound, getpass

def getPlayerPrice(playerName):
  with open('players.json') as json_data:
    data = json.load(json_data)
    return data[playerName]

def changeSpecialCharacters(string):
  newString = ''
  for letter in string:
    if letter == 'ä':
      newString += 'a'
    elif letter == "é":
      newString += 'e'  
    else:
      newString += letter
  return newString

def yes_or_no(question):
    reply = str(input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
      return yes_or_no("Uhhhh... please enter ")


def search() :
  lastAction = 'Minus'
  minusButton = browser.find_element_by_xpath('/html/body/section/section/section/div[2]/div/div[2]/div/div[1]/div[2]/div[5]/div[2]/button[1]')
  plusButton = browser.find_element_by_xpath('/html/body/section/section/section/div[2]/div/div[2]/div/div[1]/div[2]/div[5]/div[2]/button[2]')
  while True: 
    if lastAction == 'Minus':
      try:
        plusButton.click()
        lastAction = 'Plus'
      except:
        pass
    else:
      try:
        minusButton.click()
        lastAction = 'Minus'
      except:
        pass
    try:
      browser.find_element_by_xpath('/html/body/section/section/section/div[2]/div/div[2]/div/div[2]/button[2]').click()
    except:
      pass  
    time.sleep(0.5)
    itemsForSale = browser.find_elements_by_class_name('listFUTItem')
    if len(itemsForSale) > 0:
      print('Found some items! \n Buying them now...')
      itemsForSale.reverse()
      for item in itemsForSale:
        if len(itemsForSale) > 0:
          try:
            if len(itemsForSale) > 1:
              time.sleep(0.5)
              item.click()
            time.sleep(0.5)  
            #buy now button
            browser.find_element_by_class_name('buyButton').click()
            time.sleep(0.1)
            #ok button
            browser.find_element_by_xpath('/html/body/div[1]/section/div/footer/button[2]').click()
            time.sleep(1)
            if sellMode:
              #click on transfer market button
              browser.find_element_by_xpath('/html/body/section/section/section/div[2]/section/div/section[2]/div/div/div[2]/div[2]/div[1]/button').click()
              time.sleep(2)
              coinsBoughtFor = browser.find_element_by_class_name('boughtPriceValue').text
              #change bid input
              browser.find_element_by_xpath('/html/body/section/section/section/div[2]/section/div/section[2]/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/input').click()          
              browser.find_element_by_xpath('/html/body/section/section/section/div[2]/section/div/section[2]/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/input').send_keys(coinsBoughtFor)
              playerName = item.find_element_by_class_name('name').text
              if not groupBuy:
                buyNowPrice = getPlayerPrice(changeSpecialCharacters(playerName))
              else:
                  buyNowPrice = sellPrice
              # change buyNowInput
              browser.find_element_by_xpath('/html/body/section/section/section/div[2]/section/div/section[2]/div/div/div[2]/div[2]/div[2]/div[3]/div[2]/div/input').click()
              browser.find_element_by_xpath('/html/body/section/section/section/div[2]/section/div/section[2]/div/div/div[2]/div[2]/div[2]/div[3]/div[2]/div/input').send_keys(buyNowPrice)
              #list item
              browser.find_element_by_xpath('/html/body/section/section/section/div[2]/section/div/section[2]/div/div/div[2]/div[2]/div[2]/button').click()
              time.sleep(2)
              if coinsBoughtFor > 0 and onlyOne:
                winsound.Beep(1500, 1000)
                return 0
            else:
              if onlyOne and browser.find_element_by_class_name('won'):
                #send to transfer list and exit
                browser.find_element_by_xpath('/html/body/section/section/section/div[2]/section/div/section[2]/div/div/div[2]/div[3]/button[7]').click()
                winsound.Beep(1500, 1000)
                return 0
              else:
                #just send it and keep going
                browser.find_element_by_xpath('/html/body/section/section/section/div[2]/section/div/section[2]/div/div/div[2]/div[3]/button[7]').click()
          except Exception as exception:
            print(exception)
      try:
        #go back
        browser.find_element_by_xpath('/html/body/section/section/section/div[1]/button[1]').click()
      except:
        pass   
      time.sleep(2)
    else:
      print('there are no players')
      time.sleep(0.5)
      try:
        #go back
        browser.find_element_by_xpath('/html/body/section/section/section/div[1]/button[1]').click()
      except:
        pass
      time.sleep(2)
    if msvcrt.kbhit():
	    if ord(msvcrt.getch()) == 27:
	      break  

#configs
sellMode = False
onlyOne = False
groupBuy = False

browser = webdriver.Firefox(executable_path=r"")
browser.get("https://www.easports.com/fifa/ultimate-team/web-app/")     
time.sleep(10)
loginButton = browser.find_element_by_xpath('/html/body/section/div/div/div/button[1]')
loginButton.click()
email = input('Email: ')
password = getpass.getpass()
emailForm = browser.find_element_by_xpath('//*[@id="email"]')
passForm = browser.find_element_by_xpath('//*[@id="password"]')
emailForm.send_keys(email)
passForm.send_keys(password)
fullLoginButton = browser.find_element_by_id('btnLogin')
fullLoginButton.click()
done = input('Please finish and select how you want to use our app \n1. Let me put the input \n2. I tell you the parameters\n')
if done == '1':
  while True:
    input('Please press enter once you`ve set up the filter \n')
    if yes_or_no('Do you want to sell the cards bought?'):
      sellMode = True
    if yes_or_no('Do you want to just buy one?'):
      onlyOne = True
    if yes_or_no('Is it a group filter?'):
      groupBuy = True
      sellPrice = input('How much should we sell for?')   
    search()
else:    
  while True:
    transfersButton = browser.find_element_by_xpath('/html/body/section/section/nav/button[3]')
    transfersButton.click()
    time.sleep(2)
    transferMarket = browser.find_element_by_xpath('/html/body/section/section/section/div[2]/div/div/div[2]/div[2]').click()
    # player insert 
    player = input('What player should we search for?')
    playerInput = browser.find_element_by_xpath('/html/body/section/section/section/div[2]/div/div[2]/div/div[1]/div[1]/div[1]/div/input').send_keys(player)
    time.sleep(2)
    playerSelection = browser.find_element_by_xpath('/html/body/section/section/section/div[2]/div/div[2]/div/div[1]/div[1]/div[1]/div/div/ul/button[1]').click()
    # price insert
    maxPrice = input('What price should we search for?')
    priceInput = browser.find_element_by_xpath('/html/body/section/section/section/div[2]/div/div[2]/div/div[1]/div[2]/div[6]/div[2]/div/input').send_keys(maxPrice)
    time.sleep(0.5)
    browser.find_element_by_xpath('/html/body/section/section/section/div[2]/div/div[2]/div/div[1]/div[2]/div[6]/div[2]/button[2]').click()
    time.sleep(0.5)
    browser.find_element_by_xpath('/html/body/section/section/section/div[2]/div/div[2]/div/div[1]/div[2]/div[6]/div[2]/button[1]').click()
    time.sleep(5)
    search()

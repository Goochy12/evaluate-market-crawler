# 1. open website
# 2. identify player
# 3. iterate through cards
# 4. extract purchases

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

url = 'https://evaluate.market/editions'
playerSelectXPath = '//*[@id="root"]/div/section/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[2]/div/div'
rowCounterXpath = '//*[@id="rc-tabs-0-panel-1"]/div/div/div/ul/li[10]/div/div[1]'
numberOfRowsXPath = '//*[@id="rc-tabs-0-panel-1"]/div/div/div/ul/li[10]/div/div[2]/div/div/div/div[2]/div/div/div/div[5]'
nextPageButtonXPathL4 = '//*[@id="rc-tabs-0-panel-1"]/div/div/div/ul/li[9]/button'
nextPageButtonXPath4 = '//*[@id="rc-tabs-0-panel-1"]/div/div/div/ul/li[10]/button'
nextPageButtonXPathG4 = '//*[@id="rc-tabs-0-panel-1"]/div/div/div/ul/li[11]/button'
tableXPath = '//*[@id="rc-tabs-0-panel-1"]/div/div/div/div/div/div/table'
dummyRowXPath = '//*[@id="rc-tabs-0-panel-1"]/div/div/div/div/div/div/table/tbody/tr[2]'
spinnerClassName = 'ant-spin-blur'
wait = None

def openSite(url):
    browser = webdriver.Chrome()
    browser.get(url)
    return browser

def getPlayerNames(mui, playerDropdownInput):
    playerDropdownInput.click()
    id = mui + "-popup"
    unorderedList = wait.until(EC.presence_of_element_located((By.ID,id)))
    players = unorderedList.find_elements_by_tag_name("li")
    playerDropdownInput.click()
    return players

def getPlayerDropdownInput(playerSelectXPath):
    # wait until present
    playerDropdown = wait.until(EC.presence_of_element_located((By.XPATH,playerSelectXPath)))
    playerDropdownInput = playerDropdown.find_element_by_tag_name('input')
    return playerDropdownInput

def getMUI(playerDropdownInput):
    playerDropdownInput.click()
    mui = playerDropdownInput.get_attribute('id')
    playerDropdownInput.click()
    return mui

def selectPlayer(playerDropdownInput,mui,option):
    playerDropdownInput.click()
    id = mui + "-option-" + str(option)
    wait.until(EC.element_to_be_clickable((By.ID,id))).click()
    return

def changeRowCount(rowCounterXpath, numberOfRowsXPath):
    wait.until(EC.element_to_be_clickable((By.XPATH,rowCounterXpath))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,numberOfRowsXPath))).click()
    return

def nextPageInTable(pageNumber):
    nextPageButtonXPath = None
    if pageNumber < 3:
        nextPageButtonXPath = nextPageButtonXPathL4
    elif pageNumber == 3:
        nextPageButtonXPath = nextPageButtonXPath4
    else:
        nextPageButtonXPath = nextPageButtonXPathG4

    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME,spinnerClassName)))
    wait.until(EC.element_to_be_clickable((By.XPATH, nextPageButtonXPath))).click()

def getTableRows(tableXPath):
    table = wait.until(EC.presence_of_element_located((By.XPATH, tableXPath)))
    time.sleep(2)
    rows = table.find_elements_by_tag_name('tr')

    return rows

def run():
    browser = openSite(url)

    wait = WebDriverWait(browser,20)

    playerDropdownInput = getPlayerDropdownInput(playerSelectXPath)
    mui = getMUI(playerDropdownInput)

    selectPlayer(playerDropdownInput,mui,0)

    changeRowCount(rowCounterXpath, numberOfRowsXPath)

    rows = getTableRows(tableXPath)
    for eachRow in rows:
        col = eachRow.find_elements_by_tag_name('td')
        for eachCol in col:
            print(eachCol.text)
    return

def saveToFile():
    return

if __name__ == '__main__':
    browser = openSite(url)
    browser.maximize_window()

    wait = WebDriverWait(browser,20)

    playerDropdownInput = getPlayerDropdownInput(playerSelectXPath)
    mui = getMUI(playerDropdownInput)

    selectPlayer(playerDropdownInput,mui,0)

    changeRowCount(rowCounterXpath, numberOfRowsXPath)

    i = 1
    for i in range(25):
        nextPageInTable(i)
        i += 1

    # rows = getTableRows(tableXPath)
    # for eachRow in rows:
    #     col = eachRow.find_elements_by_tag_name('td')
    #     for eachCol in col:
    #         print(eachCol.text)

    # nextPageInTable(nextPageButtonXPath)

    # browser.find_element_by_xpath('//*[@id="rc-tabs-0-panel-1"]/div/div/div/ul/li[10]/div/div[1]').click()
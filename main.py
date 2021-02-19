
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

url = 'https://evaluate.market/editions'
playerSelectXPath = '//*[@id="root"]/div/section/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[2]/div/div'
rowCounterXpath = '//*[@id="rc-tabs-0-panel-1"]/div/div/div/ul/li[10]/div/div[1]'
numberOfRowsXPath = '//*[@id="rc-tabs-0-panel-1"]/div/div/div/ul/li[10]/div/div[2]/div/div/div/div[2]/div/div/div/div[5]'
nextPageButtonClass = 'ant-pagination-next'
nextPageButtonDisabledClass = 'ant-pagination-disabled'
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

def nextPageInTable():
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME,spinnerClassName)))
    nextButton = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, nextPageButtonClass)))
    if(nextButton.get_attribute("aria-disabled")) == "true":
        return False
    nextButton.click()
    return True

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

    flag = True
    while flag == True:
        flag = nextPageInTable()

    # rows = getTableRows(tableXPath)
    # for eachRow in rows:
    #     col = eachRow.find_elements_by_tag_name('td')
    #     for eachCol in col:
    #         print(eachCol.text)
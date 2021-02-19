
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

url = 'https://evaluate.market/editions'
playerSelectXPath = '//*[@id="root"]/div/section/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[2]/div/div'
momentSelectXPath = '//*[@id="root"]/div/section/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[3]/div[2]/div/div'
rowCounterXpath = '//*[@id="rc-tabs-0-panel-1"]/div/div/div/ul/li[10]/div/div[1]'
numberOfRowsXPath = '//*[@id="rc-tabs-0-panel-1"]/div/div/div/ul/li[10]/div/div[2]/div/div/div/div[2]/div/div/div/div[5]'
nextPageButtonClass = 'ant-pagination-next'
nextPageButtonDisabledClass = 'ant-pagination-disabled'
tableXPath = '//*[@id="rc-tabs-0-panel-1"]/div/div/div/div/div/div/table'
dummyRowXPath = '//*[@id="rc-tabs-0-panel-1"]/div/div/div/div/div/div/table/tbody/tr[2]'
spinnerClassName = 'ant-spin-blur'
dropdownClassName = 'MuiAutocomplete-listbox'
wait = None
tableFileName = 'marketplace_data.csv'
playerFileName = 'players.csv'
playerNames = []

def openFileA(filename, format):
    return open(filename, 'a+', encoding=format)

def openFileRW(filename):
    return open(filename, 'rw+', encoding="utf-16")

def openSite(url):
    browser = webdriver.Chrome()
    browser.get(url)
    return browser

def getPlayerNamesElements(playerDropdownInput):
    global wait
    playerDropdownInput.click()
    # id = mui + "-popup"
    unorderedList = wait.until(EC.presence_of_element_located((By.CLASS_NAME, dropdownClassName)))
    players = unorderedList.find_elements_by_tag_name("li")
    return players

def getPlayerDropdownInput(playerSelectXPath):
    global wait
    playerDropdown = wait.until(EC.presence_of_element_located((By.XPATH,playerSelectXPath)))
    playerDropdownInput = playerDropdown.find_element_by_tag_name('input')
    return playerDropdownInput

def getMUI(playerDropdownInput):
    playerDropdownInput.click()
    mui = playerDropdownInput.get_attribute('id')
    playerDropdownInput.click()
    return mui

def selectPlayer(playerDropdownInput,mui,option):
    global wait
    playerDropdownInput.click()
    id = mui + "-option-" + str(option)
    wait.until(EC.element_to_be_clickable((By.ID,id))).click()
    return

def changeRowCount(rowCounterXpath, numberOfRowsXPath):
    global wait
    wait.until(EC.element_to_be_clickable((By.XPATH,rowCounterXpath))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,numberOfRowsXPath))).click()
    return

def nextPageInTable():
    global wait
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME,spinnerClassName)))
    nextButton = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, nextPageButtonClass)))
    if(nextButton.get_attribute("aria-disabled")) == "true":
        return False
    nextButton.click()
    return True

def getTableRows(tableXPath):
    global wait
    table = wait.until(EC.presence_of_element_located((By.XPATH, tableXPath)))
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME,spinnerClassName)))
    rows = table.find_elements_by_tag_name('tr')

    return rows

def getRowData(row):
    d = []
    if row[1] != '':
        for eachData in row:
            d.append(eachData.text)
        return d
    return None

def saveRow(file, rowData):
    for eachData in rowData:
        appendToFile(file,eachData)
        appendToFile(file,',')
    appendToFile(file,'\n')

def getDataElementsFromRow(row):
    rawRowElements = row.find_elements_by_tag_name('td')
    if rawRowElements == None or len(rawRowElements) == 0 or rawRowElements[0].text == None:
        return None
    return rawRowElements

def appendToFile(file,item):
    file.write(item)

def getPlayerNames(playerNameElements):
    global playerNames
    for eachPlayer in playerNameElements:
        playerNames.append(eachPlayer.text)
    return playerNames

def getPlayerMomentsInput():
    global wait
    momentDropdown = wait.until(EC.presence_of_element_located((By.XPATH, momentSelectXPath)))
    momentDropdownInput = momentDropdown.find_element_by_tag_name('input')
    return momentDropdownInput

def getPlayerMomentsElements(momentsDropDownInput):
    global wait
    momentsDropDownInput.click()
    # id = mui + "-popup"
    unorderedList = wait.until(EC.presence_of_element_located((By.CLASS_NAME, dropdownClassName)))
    momentsElements = unorderedList.find_elements_by_tag_name("li")
    return momentsElements

def savePlayerNames(playerNames):
    playerFile = openFileA(playerFileName, "utf-16")
    for eachPlayer in playerNames:
        appendToFile(playerFile,eachPlayer)
        appendToFile(playerFile,'\n')
    playerFile.close()
    return

def saveTable(playerCount, playerDropdownInput, mui):
    global playerNames
    tableFile = openFileA(tableFileName, "utf-8")
    for i in range(playerCount):
        selectPlayer(playerDropdownInput, mui, i)
        # changeRowCount(rowCounterXpath, numberOfRowsXPath)

        # iterate through table
        npFlag = True
        while npFlag == True:
            first = 0
            rows = getTableRows(tableXPath)
            for eachRow in rows:
                if first >= 2:
                    # player, dunkname, rest
                    rawRowData = getDataElementsFromRow(eachRow)
                    if rawRowData != None:
                        data = getRowData(rawRowData)
                        if data != None:
                            saveRow(tableFile, data)
                first += 1
            npFlag = nextPageInTable()

    tableFile.close()

    return

def testTableSave(playerDropdownInput, mui):
    global playerNames

    tableFile = openFileA(tableFileName, "utf-8")
    selectPlayer(playerDropdownInput, mui, 0)
    # changeRowCount(rowCounterXpath, numberOfRowsXPath)

    rows = getTableRows(tableXPath)
    first = 0
    for eachRow in rows:
        if first >= 2:
            rawRowData = getDataElementsFromRow(eachRow)
            if rawRowData != None:
                data = getRowData(rawRowData)
                print(data)
                if data != None:
                    saveRow(tableFile, data)
        first += 1
    tableFile.close()

    return

def run():
    global wait, playerNames



    browser = openSite(url)
    browser.maximize_window()

    wait = WebDriverWait(browser,20)

    playerDropdownInput = getPlayerDropdownInput(playerSelectXPath)
    mui = getMUI(playerDropdownInput)

    playerNameElements = getPlayerNamesElements(playerDropdownInput)
    playerNames = getPlayerNames(playerNameElements)
    playerDropdownInput.click()
    playerCount = len(playerNames)

    # savePlayerNames(playerNames)
    # saveTable(playerCount, playerDropdownInput, mui)
    testTableSave(playerDropdownInput,mui)
    return

def saveToFile():
    return

if __name__ == '__main__':
    run()
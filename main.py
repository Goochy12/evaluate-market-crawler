
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os

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
    unorderedList = wait.until(EC.presence_of_element_located((By.CLASS_NAME, dropdownClassName)))
    players = unorderedList.find_elements_by_tag_name("li")
    return players

def getPlayerDropdownInput(playerSelectXPath):
    global wait
    playerDropdown = wait.until(EC.presence_of_element_located((By.XPATH,playerSelectXPath)))
    playerDropdownInput = playerDropdown.find_element_by_tag_name('input')
    return playerDropdownInput

def getPlayerMUI(playerDropdownInput):
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
    for eachData in row:
        d.append(eachData.text)
    return d
    return None

def saveRow(file, rowData):
    for eachData in rowData:
        appendToFile(file,eachData)
        appendToFile(file,',')
    appendToFile(file,'\n')
    file.flush()
    os.fsync(file.fileno())

def getDataElementsFromRow(row):
    rawRowElements = row.find_elements_by_tag_name('td')
    if rawRowElements == None or len(rawRowElements) == 0 or rawRowElements[0].text == None:
        return None
    return rawRowElements

def appendToFile(file,item):
    file.write(item)

def getElementText(elements):
    text = []
    for eachText in elements:
        text.append(eachText.text)
    return text

def getPlayerNames(playerDropdownInput):
    playerDropdownInput.click()
    playerNameElements = getPlayerNamesElements(playerDropdownInput)
    playerNames = getElementText(playerNameElements)
    playerDropdownInput.click()
    return playerNames

def getMomentsNames(momentsDropdownInput):
    momentsDropdownInput.click()
    momentsElements = getPlayerMomentsElements(momentsDropdownInput)
    momentsNames = getElementText(momentsElements)
    momentsDropdownInput.click()
    return momentsNames

def getPlayerMomentsInput():
    global wait
    momentDropdown = wait.until(EC.presence_of_element_located((By.XPATH, momentSelectXPath)))
    momentDropdownInput = momentDropdown.find_element_by_tag_name('input')
    return momentDropdownInput

def getPlayerMomentsElements(momentsDropDownInput):
    global wait
    # id = mui + "-popup"
    try:
        unorderedList = wait.until(EC.presence_of_element_located((By.CLASS_NAME, dropdownClassName)))
        momentsElements = unorderedList.find_elements_by_tag_name("li")
        return momentsElements
    except:
        return []

def selectMoment(momentsDropdownInput,mui,option):
    global wait
    momentsDropdownInput.click()
    id = mui + "-option-" + str(option)
    wait.until(EC.element_to_be_clickable((By.ID,id))).click()
    return

def getMomentsMui(momentsDropdownInput):
    momentsDropdownInput.click()
    mui = momentsDropdownInput.get_attribute('id')
    momentsDropdownInput.click()
    return mui

def savePlayerNames(playerNames):
    playerFile = openFileA(playerFileName, "utf-16")
    for eachPlayer in playerNames:
        appendToFile(playerFile,eachPlayer)
        appendToFile(playerFile,'\n')
    playerFile.close()
    return

def saveTable(playerNames, playerDropdownInput, playerMui):
    tableFile = openFileA(tableFileName, "utf-8")
    for player in range(len(playerNames)):
        selectPlayer(playerDropdownInput, playerMui, player)

        momentsDropdownInput = getPlayerMomentsInput()
        momentsMui = getMomentsMui(momentsDropdownInput)
        momentsNames = getMomentsNames(momentsDropdownInput)
        # changeRowCount(rowCounterXpath, numberOfRowsXPath)

        for moment in range(len(momentsNames)):
            selectMoment(momentsDropdownInput,momentsMui,moment)
            # iterate through table
            npFlag = True
            while npFlag == True:
                rows = getTableRows(tableXPath)
                for eachRow in rows:
                    # player, dunkname, rest
                    rawRowData = getDataElementsFromRow(eachRow)
                    if rawRowData != None:
                        data = getRowData(rawRowData)
                        data.insert(0, playerNames[player])
                        data[1] = momentsNames[moment]
                        if data != None:
                            saveRow(tableFile, data)
                npFlag = nextPageInTable()

    tableFile.close()

    return

def testSaveTable(playerNames, playerDropdownInput, playerMui):
    tableFile = openFileA(tableFileName, "utf-8")
    selectPlayer(playerDropdownInput, playerMui, 1)

    momentsDropdownInput = getPlayerMomentsInput()
    momentsMui = getMomentsMui(momentsDropdownInput)
    momentsNames = getMomentsNames(momentsDropdownInput)
    # changeRowCount(rowCounterXpath, numberOfRowsXPath)
    print(momentsNames)

    for moment in range(len(momentsNames)):
        selectMoment(momentsDropdownInput, momentsMui, moment)
        # iterate through table
        npFlag = True
        while npFlag == True:
            rows = getTableRows(tableXPath)
            for eachRow in rows:
                # player, dunkname, rest
                rawRowData = getDataElementsFromRow(eachRow)
                if rawRowData != None:
                    data = getRowData(rawRowData)
                    data.insert(0, playerNames[player])
                    data[1] = momentsNames[moment]
                    if data != None:
                        saveRow(tableFile, data)
            npFlag = nextPageInTable()

    tableFile.close()

    return

def run():
    global wait, playerNames

    browser = openSite(url)
    browser.maximize_window()

    wait = WebDriverWait(browser,20)

    playerDropdownInput = getPlayerDropdownInput(playerSelectXPath)
    playerMui = getPlayerMUI(playerDropdownInput)
    playerNames = getPlayerNames(playerDropdownInput)

    # momentsNames = getMomentsNames(momentsDropdownInput)
    # print(momentsNames)

    # savePlayerNames(playerNames)
    saveTable(playerNames, playerDropdownInput, playerMui)
    # testSaveTable(playerNames, playerDropdownInput, playerMui)

    browser.quit()

    return

def saveToFile():
    return

if __name__ == '__main__':
    run()
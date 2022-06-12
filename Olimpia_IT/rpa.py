from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from config import variables
import requests
import shutil
import os
import re

class Rpa():

    def __init__(self, search,depto , number):
        self.search = search
        self.depto = depto.upper()
        self.number = number
        self.counter = 0
        self.info = dict()
        self.wait = 20

    def setConnection(self):

        status_code = requests.get("https://www.einforma.co/buscador-empresas-empresarios").status_code
        return status_code

    def driverHandling(self):

        try:
            if  self.setConnection() != 200:
                self.info =  {"message" : "Error connecting to the page"}
            else: 
                options = Options()
                #options.add_argument('--headless')
                options.add_argument('--disable-gpu')
                #driver = webdriver.Chrome(options = options, executable_path = variables["FILE"] + "/config/chromedriver.exe")
                driver = webdriver.Firefox(options = options, executable_path = variables["FILE"] + "/config/geckodriver.exe")
                driver.get("https://www.einforma.co/buscador-empresas-empresarios")
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                input =  driver.find_element(by=By.ID, value= "search2")
                input.clear()
                input.send_keys(str(self.search))
                driver.find_element(by=By.XPATH, value = "//*[@id='content']/div/div[2]/div[1]/div").click()
                if len(driver.find_elements(by=By.XPATH, value = "//div//p[contains(text(), 'Servicio No Disponible')]")) != 0:
                    self.info = {"message" : "There are problems with the page. Please try again or try again later."}
                    driver.close()
                else:
                    self.recursiveSearch(driver)
        except:
            self.info = {"message" : "There are problems with the page. Please try again or try again later."}
            try:
                driver.close()
            except:
                pass

    def recursiveSearch(self,driver):

        WebDriverWait(driver, self.wait).until(EC.presence_of_element_located((By.XPATH, "//*[@id='a_nacional']")))
        pre_score = driver.find_element(by=By.XPATH, value = "//*[@id='a_nacional']")
        results_number = re.findall("Empresas y Empresarios \(([0-9]*)\)", pre_score.text)[0]

        if int(results_number) == 0: 
            self.info = {"message": "No results"} 
            driver.close()
        else:
            self.info["score"] = int(results_number)
            self.info["results"] = list()

            self.switchSearch(driver)
            
            try:
                if self.info["message"] == "ND":
                    pass
            except:
                if self.counter == 12 or self.counter == 24:
                    driver.find_element(by=By.XPATH, value= f"//*[@id='nacional']/div[3]/div/div[2]/ul/li[{int(((self.counter)/12)+2)}]/a").click()
                    self.recursiveSearch(driver)
                    try:
                        driver.close()    
                    except:
                        pass 
                try:
                    driver.close()
                except:
                    pass        
            
    def switchSearch(self, driver):
        
        table_rows_results =  driver.find_elements(by=By.XPATH, value= "//*[@id='nacional']/tbody/tr")

        for n in range(1, len(table_rows_results)+1):

            if n == 1:
                self.driverFolderCreation()

            row = driver.find_element(by=By.XPATH, value= f"//*[@id='nacional']/tbody/tr[{n}]/td[1]")
            
            row.click()

            table_rows_resume =  driver.find_elements(by=By.XPATH, value= "//*[@id='imprimir']/table/tbody/tr")
            
            driver.find_element(by=By.XPATH, value= f"//*[@id='PROVINCIA']").click()

            try:
                driver.find_element(by=By.XPATH, value= f"//*[@id='PROVINCIA']/option[contains(text(), '{self.depto}')]").click()
            except:
                self.info = {"message": "ND"}
            else:
                info_empresa = dict()
                for m in range(2, len(table_rows_resume)+1):    
                    try:
                        driver.find_element(by=By.XPATH, value= f"/html/body/div[2]/div[2]/div/div/div[2]/div/div[1]/div[2]/table")    
                    except:
                        basic_info_row = lambda x:  driver.find_element(by=By.XPATH, value= f"/html/body/div[2]/div[2]/div/div/div[2]/div/div[1]/div[3]/table/tbody/tr[{m}]/td[{x}]")     
                    else:
                        basic_info_row = lambda x:  driver.find_element(by=By.XPATH, value= f"/html/body/div[2]/div[2]/div/div/div[2]/div/div[1]/div[2]/table/tbody/tr[{m}]/td[{x}]")
                                            
                    try:                                                           
                        info_empresa[basic_info_row(1).text[:-1]] = basic_info_row(2).text
                    except:
                        continue
            
                row_name = info_empresa["Razón Social"].replace(" ", "-")

                self.driverScreenshot(driver,row_name)

                info_empresa["Search Number"] = self.counter + 1
                info_empresa["ScreenShot"] = self.screenShotRoute(row_name) 
                self.info["results"].append(info_empresa)
                driver.back()

                self.counter += 1

                if (self.counter + 1 > self.number) or (self.counter + 1 > 30) :
                    break
                else:
                    continue

    def driverScreenshot(self, driver,name):

        move_to = driver.find_element(by=By.XPATH, value= "//*[@id='titEtiqueta']")
        move_to.location_once_scrolled_into_view
        driver.save_screenshot(f'screenshots/{self.search}/{name}.png')

    def screenShotRoute(self, name):
        return variables["FILE"] + f"/screenshots/{self.search}/{name}.png"

    def driverFolderCreation(self):

        dir_name = variables["FILE"] + f"/screenshots/{self.search}"
        try:
            if self.counter == 0: 
                os.mkdir(dir_name )
        except:
            shutil.rmtree(dir_name)
            os.mkdir(dir_name)
        
    @classmethod
    def stringInt(cls,string):
        try: 
            int(string)
            return True
        except ValueError:
            return False

        











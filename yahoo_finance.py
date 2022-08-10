from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import matplotlib.pyplot as plt
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class Localanaliz:
    def __init__(self):
        self.url = "https://finance.yahoo.com/quote/"
        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
        self.bekleme = 10
        self.carpanlar = []

    def get_veriler(self):
        rowsize = 1
        colsize = 1
        loopbreak = 0
        while loopbreak == 0:
            try:
                rovi = self.driver.find_element(By.XPATH,
                                                f"//*[@id='Col1-1-HistoricalDataTable-Proxy']/section/div[2]/table/thead/tr/th[{rowsize}]").is_enabled()
                rowsize = rowsize + 1
            except:
                rowsize = rowsize - 1
                loopbreak = 1
                break
        print("satır sayısı(rowsize) : {0}".format(rowsize))

        while loopbreak == 1:
            try:
                coli = self.driver.find_element(By.XPATH,
                                                f" //*[@id='Col1-1-HistoricalDataTable-Proxy']/section/div[2]/table/tbody/tr[{colsize}]").is_enabled()
                colsize = colsize + 1
            except:
                colsize = colsize - 1
                loopbreak = 2
                break
        print("sutun sayısı(colsize) = {0}".format(colsize))
        arr = []
        for i in range(colsize):
            col = []
            for j in range(rowsize):
                if i == 0:
                    path = "//*[@id='Col1-1-HistoricalDataTable-Proxy']/section/div[2]/table/thead/tr/th[" + str(
                        j + 1) + "]/span"
                    veri = str(self.driver.find_element(By.XPATH, path).text).strip(',.!*')
                    col.append(veri)
                elif i == 4:
                    break
                else:
                    path = "//*[@id='Col1-1-HistoricalDataTable-Proxy']/section/div[2]/table/tbody/tr[" + str(
                        i + 1) + "]/td[" + str(j + 1) + "]/span"
                    veri = str(self.driver.find_element(By.XPATH, path).text)
                    col.append(veri)
            arr.append(col)

        print(arr)

        with open("veriler.csv", "w") as dosyam:
            yaz = csv.writer(dosyam)
            for i in arr:
                if i == 0:
                    yaz.writerow(i)
                else:
                    yaz.writerow(i)
            dosyam.close()

        print("CSV dosyasına kaydedilmiş veriler : \n{0}".format(pd.read_csv("veriler.csv")))
        df = pd.read_csv('veriler.csv')

        df.set_index('Date').plot()

        plt.savefig('my_plot.png')
        plt.pause(10)
        plt.close()

    def carpanlar_baglan(self, hisse):
        self.driver.get(self.url + hisse)
        self.driver.maximize_window()
        WebDriverWait(self.driver, self.bekleme).until(
            ec.element_to_be_clickable((By.XPATH, "//*[@id='quote-nav']/ul/li[5]"))).click()
        time.sleep(7)
        WebDriverWait(self.driver, self.bekleme).until(
            ec.element_to_be_clickable((By.XPATH, "//span[@data-test='historicalFrequency-selected']"))).click()
        WebDriverWait(self.driver, self.bekleme).until(
            ec.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Monthly')]"))).click()
        WebDriverWait(self.driver, self.bekleme).until(
            ec.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Apply']"))).click()
        time.sleep(7)
        self.get_veriler()
        self.driver.quit()


if __name__ == '__main__':
    x = Localanaliz()

    garan = x.carpanlar_baglan("GARAN.IS")

    print(garan)

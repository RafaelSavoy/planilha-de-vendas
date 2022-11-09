import pandas as pd
import os

monthList = ['01.Janeiro', '02.Fevereiro', '03.Março',
             '04.Abril', '05.Maio', '06.Junho', '07.Julho', '08.Agosto', '09.Setembro', '10.Outubro', '11.Novembro', '12.Dezembro']

pathName = input('Caminho do arquivo de vendas que deseja ler: ')
pathName = input('Digite o nome da pasta em que os arquivos serão gerados: ')

class Manager:
    def __init__(self, salesFile, salesPath):
        self.currentDate = {}
        self.salesPath = salesPath
        self.sales = pd.read_excel(salesFile, index_col=0)
        self.defaultDataFrame = pd.DataFrame(
            columns=['Loja', 'Vendedor', 'Valor da Venda', 'Data'])
        self.currentDaySales = [self.defaultDataFrame]

    def getSales(self):
        return self.sales

    def toSalesPath(self):
        os.chdir(self.salesPath)

    def getDefaultDataFrame(self):
        return self.defaultDataFrame

    def setDefaultDataFrame(self, dataFrame):
        self.defaultDataFrame = dataFrame

    def resetDefaultDataFrame(self):
        self.setDefaultDataFrame(pd.DataFrame(
            columns=['Loja', 'Vendedor', 'Valor da Venda', 'Data']))

    def setCurrentDate(self, day, month, year):
        self.currentDate['year'] = year
        self.currentDate['month'] = month
        self.currentDate['day'] = day
        self.currentDate['extenseMonth'] = monthList[int(month) - 1]

    def getFullDate(self):
        date = self.getCurrentDate()
        return '{}/{}/{}'.format(date['day'], date['month'], date['year'])

    def getCurrentDate(self):
        return self.currentDate

    def resetCurrentDate(self):
        self.currentDate = {}

    def toDateFolder(self):
        currentDate = self.currentDate
        if len(currentDate) < 3:
            print("A data não foi definida!")
            return
        if not os.path.exists(currentDate['year']):
            os.mkdir(currentDate['year'])
        os.chdir(currentDate['year'])
        if not os.path.exists(currentDate['extenseMonth']):
            os.mkdir(currentDate['extenseMonth'])
        os.chdir(currentDate['extenseMonth'])
        if not os.path.exists(currentDate['day']):
                os.mkdir(currentDate['day'])
        os.chdir(currentDate['day'])
                    

    def addCurrentDaySale(self, daySale):
        self.currentDaySales.append(daySale)

    def getCurrentDaySales(self):
        return self.currentDaySales

    def resetCurrentDaySales(self):
        self.currentDaySales = [self.defaultDataFrame]

    def generateSalesFile(self, fileName):
        self.setDefaultDataFrame(pd.concat(
            self.getCurrentDaySales(), ignore_index=True))
        self.getDefaultDataFrame().to_excel(fileName)
        self.resetDefaultDataFrame()
        self.resetCurrentDaySales()
        self.resetCurrentDate()


if not os.path.exists(pathName):
    os.mkdir(pathName)

manager = Manager(
    'Vendas.xlsx', r'C:\Users\Rafael\Documents\Python\Automação\PlanilhaDeVendas/{}'.format(pathName))
manager.toSalesPath()

for index, currentSale in manager.getSales().iterrows():
    print(currentSale)
    [day, month, year] = currentSale['Data'].split("/")
    if not manager.getCurrentDate():
        manager.setCurrentDate(day, month, year)
        manager.toDateFolder()
    nextSale = None
    if (index + 1) < len(manager.getSales()):
        nextSale = manager.getSales().iloc[index + 1]
    manager.addCurrentDaySale(currentSale.to_frame().T)
    if type(nextSale) == type(None) or not nextSale['Data'] == manager.getFullDate():
        manager.generateSalesFile('Venda.xlsx')
        manager.toSalesPath()

import requests as rs


class GoogleSheetClient:

    def __init__(self, sheetId):
        self.sheetId = sheetId

    def query(self):
        url = f'https://docs.google.com/spreadsheets/d/{self.sheetId}/export?format=csv&id={self.sheetId}&gid=0'
        res = rs.get(url)

        return res.content.decode("utf-8")

    def getDictKeyVal(self,  keyHeader, valHeader):
        csvTable = self.query()
        tableStrRows = csvTable.split("\r\n")
        arrTableHeader = tableStrRows[0].split(',')
        dict = {
            valuesStr.split(",")[arrTableHeader.index(keyHeader)]:
            valuesStr.split(",")[arrTableHeader.index(valHeader)]
            for valuesStr in tableStrRows[1:]
        }
        return dict

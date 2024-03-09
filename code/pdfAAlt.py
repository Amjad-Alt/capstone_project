#%%
# %pip install pdfplumber
import pdfplumber
import os
import pandas as pd

#%%
class pdfAA:
    """
    Read special pdf files to extract info and create dataframe
    """
    
    def __init__(self, pdf_path=""):
        """
        contructor
        """
        cities = ["MAKKAH","RIYADH","TAIF","JEDDAH","BURAYDAH","MEDINA","HOFHUF","DAMMAM","TABUK","ABHA","Jazan","Hail","Baha","Njran","Arar","Skaka"] # up to page 18 on 2003.pdf. Bottom of page says page 19. Why some all caps in the pdf??
        months = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
        years = list(range(2002,2015)) # from 2002 - 2014
        multicolumns = pd.MultiIndex.from_product([cities, years, months], names=['City', 'Year', 'Month'])
        #
        rowIndices = ["General Index","Foodstuffs","Cereals and cereal products","Meat and Poultry","Fish and crustaceans","Milk and dairy products","Eggs","Cooking oil and fats","Fresh vegetables","Preserved and canned vegetables","Legumes and tubers","Fresh fruits","Preserved and canned fruits","Nuts, peanuts, seeds","Sugars and sugar preparations","Beverages","Foodstuffs, other","Tobacco","Out-of-home meals","Fabrics, clothing and footwear","Men's fabrics","Women's fabrics","Men's apparel","Women's apparel","Tailoring","Footwear","House and related items","Home repairs","Rents","Water supply expenditure","Fuel and Power","Home furniture","Furniture and carpet","Home furnishings","Small home appliances","kitchenhouse & tabletualis","Household small items","Home services","Basic home appliances","Medical care","Medical care expenses","Other medical expenses","Medicines","Transport and telecommunications","Private transport means","Operation of private transport means","Public transport fees","Telecommunications and related costs","Education and entertainment","Entertainment expenses","Education expenses","Entertainment devices","Other expenses and services","Personal hygiene and care items","Personal goods","Other expenses and services"] # taken from page 12 of 2003.pdf. Bottom of page says page 19.
        #
        self.cityIndexDf = pd.DataFrame(index=rowIndices, columns=multicolumns) # three-level column heads. Store all info here.
        self.currPdfPath = pdf_path
        self.currFileTextDf = pd.DataFrame( columns=['text']) # save each page's text into a df
        self.currFileTextDf.index.name = "page" # indexed by page number, column has the text value.
        return
    
    def importPdf(self, pdf_path="", xoffsetleft=0, xoffsetright=0, yoffsettop=0, yoffsetbottom=0, width=0, height = 0):
        """
        Import and read pdf
        Args:
            pdf_path (str, optional): _description_. Defaults to "".
            xoffset (int, optional): _description_. Defaults to 0.
            yoffset (int, optional): _description_. Defaults to 0.
        """
        if not pdf_path: pdf_path = self.currPdfPath
        if len(self.currFileTextDf): self.currFileTextDf = self.currFileTextDf.iloc[0,0] # delete everything and starts new if already existed
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                # Define the bounding box (crop box) for the first column
                # The bounding_box is in the format (x0, top, x1, bottom), with:
                # x0: the left edge of the column
                # top: the top edge of the column (usually 0 to start from the top)
                # x1: the right edge of the column
                # bottom: the bottom edge of the column (use page.height to cover until the bottom of the page)
                pagewidth = width if width > 0 else page.width/2 - xoffsetleft
                pageheight = height if height > 0 else page.height - yoffsettop - yoffsetbottom
                bounding_box = (xoffsetleft, yoffsettop, pagewidth, pageheight)
                
                # Crop the page to the bounding box to focus on the first column
                cropped_page = page.within_bbox(bounding_box)
                
                # Extract text from the cropped area
                text = cropped_page.extract_text()
                
                self.currFileTextDf.loc[i,'text'] = text 
                
                # if text:
                #     print(f"Page {i+1} First Column:\n{text}\n")
                # else:
                #     print(f"Page {i+1} First Column: No text found\n")

    def checkPageType(self, pageText):
        """
        Check if the page is about cities
        Args:
            pageText (str): the entire page of text from pdf
        """
        # return True / False, or return "city", "quarterAnnual", and different types if applicable, etc
        return True
    
    def pullCityYearMonthValues(self, pageText, city=0):
        """
        if pageType is correct, pull Year-Month values from first column somehow, along with the one-or-two city name(s)
        Args:
            pageText (str): the entire page of text from pdf
            city (int): 0 or 1, for the two different city values on a typial page. Not sure if some page might only have 1 city.
            return: [ city, year, month ] list
        """
        # checks and pull
        return [ "MAKKAH", 2003, "JAN" ] # just an example
    
    def pullRowNameAndValues(self, rowText, city=0):
        """
        For each row in pageText, see if it corresponds to an expenditure group item. If so, pull the group name, and the first column value
        Args:
            rowText (str): a row of text in pageText
            city (int): 0 or 1, for the two different city values on a typial page. Not sure if some page might only have 1 city.
            return: [ expenditureGroup, value ] list
        """
        result = None
        # result = [ "General Index", 101.60 ] # for example
        return result
    # If the two above steps are successful, can save the values into 
    # self.cityIndexDf.loc[ resultFromPullRow[0], [resultFromPullCity] ] = resultFromPullRow[1]
    
        
        
#%%
# Instantiate
# pdf_path = "/Users/amjad/OneDrive/المستندات/GWU_Cources/Spring2024/capstone_project/data/2003.pdf"
# pdf_path = "..\data\2003_sample.pdf"
pdf_path = "../data/2003_sample.pdf"
thepdf = pdfAA(pdf_path)
thepdf.importPdf()
# thepdf.importPdf(pdf_path)




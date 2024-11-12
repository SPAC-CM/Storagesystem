class I_Product:
    def __init__(self, ID, product_name):
        self.ID = ID
        self.product_name = product_name

    def ID(self):
        return self.ID

    def product_name(self):
        return self.product_name
        

class DefultProduct(I_Product):
    def __init__(self, ID, product_name):
        self.ID = ID
        self.product_name = product_name

class Clothing(I_Product):
    def __init__(self, ID, product_name, season):
        super().__init__(ID, product_name)
        self.season = season

    def Season(self):
        return self.season
        
class Food(I_Product):
    def __init__(self, ID, product_name, used_by_date):
        super().__init__(ID, product_name)
        self.used_by_date = used_by_date

    def Used_by_data(self):
        return self.used_by_date
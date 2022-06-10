import tkinter as tk

class Boutique(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.widgets()
    def widgets(self):
        self.btn_quit = tk.Button(self, text="Quitter", command=self.destroy)
        self.btn_quit.pack
        
        
        
if __name__ == "__main__":
    btk = Boutique()
    btk.title("Gestion de Boutique :)") 
    btk.mainloop()
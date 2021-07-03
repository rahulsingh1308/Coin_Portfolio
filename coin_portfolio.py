from tkinter import *
from tkinter import messagebox,Menu
import requests 
import json
import sqlite3

pycrypto=Tk()
pycrypto.geometry("300x200+10+10")
pycrypto.title("CoinCap")
pycrypto.iconbitmap('favicon.ico')

con=sqlite3.connect('coin.db')
cursorObj=con.cursor()
cursorObj.execute("create table if not exists coin (id integer primary key, symbol text , amount integer ,price real)")
con.commit()

def reset():
    for cell in pycrypto.winfo_children():
        cell.destroy()

    app_nav()
    app_header()
    my_portfolio()

def app_nav():
    def clear_all():
        cursorObj.execute("DELETE FROM coin")
        con.commit()

        messagebox.showinfo("Portfolio Notification", "Portfolio Cleared - Add New Coins")
        reset()

    def close_app():
        pycrypto.destroy()

    menu = Menu(pycrypto)
    file_item = Menu(menu)
    file_item.add_command(label='Clear Portfolio', command=clear_all)
    file_item.add_command(label='Close App', command=close_app)
    menu.add_cascade(label="File", menu=file_item)
    pycrypto.config(menu=menu)

def my_portfolio():
     api_requests=requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=edbe3e4a-2488-45c7-8ed9-5a6093c928ca")
     api=json.loads(api_requests.content)
     cursorObj.execute("select * from coin")
     coins=cursorObj.fetchall()
     
     
     def update_coin():
         cursorObj.execute("update coin set symbol=?, price=?, amount=? where id=?",(symbol_update.get(), price_update.get(), amount_update.get(), port_id_update.get()))
         con.commit()
         
         messagebox.showinfo("Portfolio Notification","Coin updated successfully !")
         reset()
      
     def delete_coin():
         cursorObj.execute("delete from coin where id=?",(port_id_delete.get(),))
         con.commit()
         
         messagebox.showinfo("Portfolio Notification","Coin deleted successfully !")
         reset()
         
     def insert_coin():
         cursorObj.execute("insert into coin (symbol,price,amount) values(?,?,?)",(symbol_txt.get(),price_txt.get(),amount_txt.get()))
         con.commit()
         
         messagebox.showinfo("Portfolio Notification","Coin inserted successfully !")
         reset()
     
     def color_indicator(amount):
       if amount>0:
          return "green"
       else:
          return "red"
     coin_row = 1
     
     for i in range(0,300):
         for coin in coins:
            if api["data"][i]["symbol"] == coin[1]:
                total_paid=coin[2] * coin[3]
                current_value= coin[2]*api["data"][i]["quote"]["USD"]["price"]
                pl_percoin=api["data"][i]["quote"]["USD"]["price"]-coin[3]
                total_pl_coin=pl_percoin * coin[2]
                
                portfolio_id=Label(pycrypto,text=coin[0],bg="light grey", fg="black", font="Arial 18 bold ",padx="5",pady="5", borderwidth="2",relief="groove") 
                portfolio_id.grid(row=coin_row,column=0,sticky=N+S+E+W)
    
                symbol=Label(pycrypto,text=api["data"][i]["symbol"],bg="light grey", fg="black")
                symbol.grid(row=coin_row,column=1,sticky=N+S+E+W)

                price=Label(pycrypto,text="${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]),bg="light grey", fg="black",font="Arial 12 bold " )
                price.grid(row=coin_row,column=2,sticky=N+S+E+W)
                
                no_coins=Label(pycrypto,text=coin[2],bg="light grey", fg="black",font="Arial 12 bold")
                no_coins.grid(row=coin_row,column=3,sticky=N+S+E+W)

                amount_paid=Label(pycrypto,text="${0:.2f}".format(total_paid),bg="light grey", fg="black",font="Arial 12 bold ")
                amount_paid.grid(row=coin_row,column=4,sticky=N+S+E+W)

                current_value=Label(pycrypto,text="${0:.2f}".format( current_value),bg="light grey", fg="black",font="Arial 12 bold ")
                current_value.grid(row=coin_row,column=5,sticky=N+S+E+W)

                pl_coin=Label(pycrypto,text="${0:.2f}".format(pl_percoin),bg="light grey", fg=color_indicator(pl_percoin), font="Arial 12 bold")
                pl_coin.grid(row=coin_row,column=6,sticky=N+S+E+W)

                total_pl=Label(pycrypto,text="${0:.2f}".format(total_pl_coin),bg="light grey", fg=color_indicator(total_pl_coin),font="Arial 12 bold")
                total_pl.grid(row=coin_row,column=7,sticky=N+S+E+W)



                coin_row +=1

     

     api=""
     
     #insert data
     
     symbol_txt=Entry(pycrypto, borderwidth="2", relief="groove")
     symbol_txt.grid(row=coin_row+1,column=1,sticky=N+S+E+W)

     price_txt=Entry(pycrypto, borderwidth="2", relief="groove")
     price_txt.grid(row=coin_row+1,column=2,sticky=N+S+E+W)

     amount_txt=Entry(pycrypto, borderwidth="2", relief="groove")
     amount_txt.grid(row=coin_row+1,column=3,sticky=N+S+E+W)
     
     add=Button(pycrypto,text="Add coin",bg="light grey", fg="black",command=insert_coin,font="Arial 18 bold",borderwidth="2", relief="groove")
     add.grid(row=coin_row+1,column=7,sticky=N+S+E+W)
     
     #update coin
     
     port_id_update=Entry(pycrypto, borderwidth="2",relief="groove") 
     port_id_update.grid(row=coin_row+2,column=0,sticky=N+S+E+W)
    
     
     symbol_update=Entry(pycrypto, borderwidth="2", relief="groove")
     symbol_update.grid(row=coin_row+2,column=1,sticky=N+S+E+W)

     price_update=Entry(pycrypto, borderwidth="2", relief="groove")
     price_update.grid(row=coin_row+2,column=2,sticky=N+S+E+W)
     
     amount_update=Entry(pycrypto, borderwidth="2", relief="groove")
     amount_update.grid(row=coin_row+2,column=3,sticky=N+S+E+W)
     
     update_coin=Button(pycrypto,text="Update coin",bg="light grey", fg="black",command=update_coin,font="Arial 18 bold",borderwidth="2", relief="groove")
     update_coin.grid(row=coin_row+2,column=7,sticky=N+S+E+W)
     
     #delete coin
     
     port_id_delete=Entry(pycrypto, borderwidth="2",relief="groove") 
     port_id_delete.grid(row=coin_row+3,column=0,sticky=N+S+E+W)
     
     delete=Button(pycrypto,text="Delete coin",bg="light grey", fg="black",command=delete_coin,font="Arial 18 bold",borderwidth="2", relief="groove")
     delete.grid(row=coin_row+3,column=7,sticky=N+S+E+W)
     
     #refresh data
    
     refresh=Button(pycrypto,text="refresh",bg="light grey", fg="black",command=my_portfolio ,font="Arial 18 bold",borderwidth="2", relief="groove")
     refresh.grid(row=coin_row,column=7,sticky=N+S+E+W)
     
     
     
    




def app_header():
    
    portfolio_id=Label(pycrypto,text="ID",bg="black", fg="white", font="Arial 18 bold ",padx="5",pady="5", borderwidth="2",relief="groove") 
    portfolio_id.grid(row=0,column=0,sticky=N+S+E+W)
           
    
    symbol=Label(pycrypto,text="symbol",bg="black", fg="white", font="Arial 18 bold ",padx="5",pady="5", borderwidth="2", relief="groove")
    symbol.grid(row=0,column=1,sticky=N+S+E+W)
    
    price=Label(pycrypto,text="Price",bg="black", fg="white", font="Arial 18 bold ",padx="5",pady="5", borderwidth="2",relief="groove") 
    price.grid(row=0,column=2,sticky=N+S+E+W)
    
    no_coins=Label(pycrypto,text="Coins Owned",bg="black", fg="white", font="Arial 18 bold ",padx="5",pady="5", borderwidth="2", relief="groove") 
    no_coins.grid(row=0,column=3,sticky=N+S+E+W)
    
    amount_paid=Label(pycrypto,text="Total amount paid",bg="black", fg="white", font="Arial 18 bold ",padx="5",pady="5", borderwidth="2",relief="groove") 
    amount_paid.grid(row=0,column=4,sticky=N+S+E+W)
    
    current_value=Label(pycrypto,text="Current Value",bg="black", fg="white", font="Arial 18 bold ",padx="5",pady="5", borderwidth="2",relief="groove") 
    current_value.grid(row=0,column=5,sticky=N+S+E+W)
    
    pl_coin=Label(pycrypto,text="P/L Per Coin",bg="black", fg="white", font="Arial 18 bold ",padx="5",pady="5", borderwidth="2",relief="groove") 
    pl_coin.grid(row=0,column=6,sticky=N+S+E+W)
    
    total_pl=Label(pycrypto,text="Total P/L",bg="black", fg="white", font="Arial 18 bold ",padx="5",pady="5", borderwidth="2",relief="groove") 
    total_pl.grid(row=0,column=7,sticky=N+S+E+W)
    

app_nav()    
app_header()
my_portfolio()
pycrypto.mainloop()
cursorObj.close()
con.close()



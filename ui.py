from tkinter import *
from tkinter import ttk
import database as db
from tkinter.messagebox import askokcancel, WARNING
import helpers

class CenterWidgetMixin:
    def center(self):
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int(ws/2 - w/2)
        y = int(hs/2 - h/2)
        self.geometry(f"{w}x{h}+{x}+{y}")
        
        
class CreateClienteWindow(Toplevel, CenterWidgetMixin):
        def __init__(self,parent):
            super().__init__(parent)
            self.title("Crear Cliente")
            self.build()
            self.center()
            self.transient(parent)
            self.grab_set()
         
        def build(self):
            frame = Frame(self)
            frame.pack(padx=20,pady=15) 
            
            Label(frame, text="DNI (2 int y 1 upper char)").grid(row=0,column=0)
            Label(frame, text="Nombre (2 -30 char)").grid(row=0,column=1)
            Label(frame, text="Apellido (2 - 30 char)").grid(row=0,column=2)
            
            #inputs
            dni = Entry(frame)
            dni.grid(row=1,column=0)
            dni.bind("<KeyRelease>",lambda event: self.validate(event,0))
            nombre = Entry(frame)
            nombre.grid(row=1,column=1)
            nombre.bind("<KeyRelease>",lambda event: self.validate(event,1))
            apellido = Entry(frame)
            apellido.grid(row=1,column=2)
            apellido.bind("<KeyRelease>",lambda event: self.validate(event,2))
            
            frame = Frame(self)
            frame.pack(pady=10)
            
            crear = Button(frame, text="Crear",command=self.create_client)
            crear.configure(state=DISABLED)
            crear.grid(row=0,column=0)
            Button(frame,text="Cancelar",command=self.close).grid(row=0,column=1)
            #PARA menejo en tiempo real
            self.validaciones = [0,0,0]
            self.crear = crear
            self.dni = dni
            self.nombre = nombre
            self.apellido = apellido
            
    
        def create_client(self):
            self.master.treeview.insert(
                parent='', index='end',iid=self.dni,values=(self.dni.get(),self.nombre.get(),self.apellido.get())
            )
            db.Clientes.crear(self.dni.get(),self.nombre.get(),self.apellido.get())
            self.close()
        
        def validate(self,event,index):
            """_summary_

            Args:
                event (_type_): evento del widget Entry
                index (_type_): 0 para dni, 1 para nombre y 2 para apellido
            """
            valor = event.widget.get()
            valido = helpers.dni_valido(valor, db.Clientes.lista) if index == 0 else (valor.isalpha() and len(valor)>= 2 and len(valor) <=30)
            event.widget.configure({"bg":"Green" if valido else "Red"})
            
            #cambiar el estado del botón
            self.validaciones[index]= valido
            self.crear.config(state=NORMAL if self.validaciones == [1,1,1] else DISABLED)
            
            
        
        def close(self):
            self.destroy()
            self.update()
    
    
class EditClientWindow(Toplevel, CenterWidgetMixin):
        def __init__(self,parent):
            super().__init__(parent)
            self.title("Actualizar Cliente")
            self.build()
            self.center()
            self.transient(parent)
            self.grab_set()
         
        def build(self):
            frame = Frame(self)
            frame.pack(padx=20,pady=15) 
            
            Label(frame, text="DNI (no editable)").grid(row=0,column=0)
            Label(frame, text="Nombre (2 -30 char)").grid(row=0,column=1)
            Label(frame, text="Apellido (2 - 30 char)").grid(row=0,column=2)
            
            #inputs
            dni = Entry(frame)
            dni.grid(row=1,column=0)
            nombre = Entry(frame)
            nombre.grid(row=1,column=1)
            nombre.bind("<KeyRelease>",lambda event: self.validate(event,0))
            apellido = Entry(frame)
            apellido.grid(row=1,column=2)
            apellido.bind("<KeyRelease>",lambda event: self.validate(event,1))
            
            cliente = self.master.treeview.focus()
            campos = self.master.treeview.item(cliente,"values")
            #deshabilitarlo despues de insertar
            dni.insert(0, campos[0])
            dni.config(state=DISABLED)
            nombre.insert(0, campos[1])
            apellido.insert(0, campos[2])
            
            frame = Frame(self)
            frame.pack(pady=10)
            
            actualizar = Button(frame, text="Actualizar",command=self.edit_client)
            actualizar.grid(row=0,column=0)
            Button(frame,text="Cancelar",command=self.close).grid(row=0,column=1)
            #PARA menejo en tiempo real
            self.validaciones = [1,1]
            self.actualizar = actualizar
            self.dni = dni
            self.nombre = nombre
            self.apellido = apellido
            
    
        def edit_client(self):
            cliente = self.master.treeview.focus()
            self.master.treeview.item(cliente , values=(self.dni.get(),self.nombre.get(),self.apellido.get()))
            db.Clientes.modificar(self.dni.get(),self.nombre.get(),self.apellido.get())
            self.close()
        
        def validate(self,event,index):
            """_summary_

            Args:
                event (_type_): evento del widget Entry
                index (_type_): 0 para nombre, 1 para apellido
            """
            valor = event.widget.get()
            valido = valor.isalpha() and len(valor)>= 2 and len(valor) <=30
            event.widget.configure({"bg":"Green" if valido else "Red"})
            
            #cambiar el estado del botón
            self.validaciones[index]= valido
            self.actualizar.config(state=NORMAL if self.validaciones == [1,1] else DISABLED)
            
            
        
        def close(self):
            self.destroy()
            self.update()
     

class MainWindow(Tk,CenterWidgetMixin):
    
    def __init__(self):
        super().__init__()
        self.title("Gestor de clientes")
        self.build()
        self.center()
        
        
    def build(self):
        frame = Frame(self)
        frame.pack()
        
        treeview = ttk.Treeview(frame)
        treeview['columns'] = ('DNI','Nombre','Apellido')
        #agrgando las columnas de la tabla
        treeview.column("#0",width=0,stretch=NO)
        treeview.column("DNI",anchor=CENTER)
        treeview.column("Nombre",anchor=CENTER)
        treeview.column("Apellido",anchor=CENTER)
        #cabecera de la tabla
        treeview.heading("DNI",text="DNI",anchor=CENTER)
        treeview.heading("Nombre",text="Nombre",anchor=CENTER)
        treeview.heading("Apellido",text="Apellido",anchor=CENTER)
        #definir scrollbar
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        #set scrollbar en el frame
        treeview['yscrollcommand'] = scrollbar.set
        
        for cliente in db.Clientes.lista:
            treeview.insert(
                parent='', index='end',iid=cliente.dni,values=(cliente.dni,cliente.nombre,cliente.apellido)
            )
        
        treeview.pack()
        
        frame =Frame(self)
        frame.pack(pady=20)
        
        Button(frame,text='Crear',command=self.create).grid(row=0,column=0)
        Button(frame,text='Borrar',command=self.delete).grid(row=0,column=1)
        Button(frame,text='Modificar',command=self.actualizar).grid(row=0,column=2)
        
        self.treeview = treeview
        
        
    def delete(self):
        cliente = self.treeview.focus()
        if cliente:
            campos = self.treeview.item(cliente,"values")
            confirmar = askokcancel(
                title="Comfirmar borrado",
                message=f"¿Borrar {campos[1]} {campos[2]}?",
                icon=WARNING
            )
            if confirmar :
                self.treeview.delete(cliente)
                db.Clientes.borrar(campos[0])
                
    def create(self):
        CreateClienteWindow(self)
        
    def actualizar(self):
        
        if self.treeview.focus():
            EditClientWindow(self)
        
        
        
        
if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
        
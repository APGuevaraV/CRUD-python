import menu
import sys
import ui


if __name__ == '__main__':
    
    if len(sys.argv) > 1 and sys.argv[1] == "-t":
        menu.iniciar()
    else:
        app = ui.MainWindow()
        app.mainloop()
    

hiddenimports = [ "Moduls.Idozito", "Moduls.Gomb", "Moduls.Kerdes", "Moduls.SimaDrot", "Moduls.KomplexKabel", "Moduls.Jelszo", "Moduls.LibaMondja"]
print("My custom hook is being loaded!")
#--hidden-import Moduls.Idozito --hidden-import Moduls.Gomb --hidden-import Moduls.Kerdes --hidden-import Moduls.SimaDrot --hidden-import Moduls.KomplexKabel --hidden-import Moduls.Jelszo --hidden-import Moduls.LibaMondja
#py -m PyInstaller main.py --onefile --windowed --icon=app.ico --additional-hooks-dir=. --debug=imports
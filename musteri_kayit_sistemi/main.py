import sys
import os

# Proje kökünü her zaman Python path'e ekle
# (VS Code play butonu bazen farklı dizinden çalıştırır)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.gui import GUI


def main():
    uygulama = GUI()
    uygulama.baslat()


if __name__ == "__main__":
    main()

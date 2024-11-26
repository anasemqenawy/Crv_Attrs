import importlib

from crv_attrs import crv_attrs_ui

importlib.reload(crv_attrs_ui)
from crv_attrs.crv_attrs_ui import SmartAttributeUI

if __name__ == "__main__":
    try:
        global main
        main.close()
        main.deleteLater()

    except:
        pass
    main = SmartAttributeUI()
    main.show()

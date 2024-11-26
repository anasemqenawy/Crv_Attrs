import maya.cmds as cmds
from maya import mel
import maya.OpenMayaUI as OMUI

try:
    from shiboken2 import wrapInstance
    from PySide2 import QtCore, QtWidgets
except ModuleNotFoundError:
    from shiboken6 import wrapInstance
    from PySide6 import QtCore, QtWidgets


# -------------------------------------------------
# ----------------- Core Functions ----------------
# -------------------------------------------------
def enable_undo(function, _name=None):
    """
    returns Decorator That Make The Process Undoable in one undo step
    """

    def undo_func(*args, **kwargs):
        # Open Chunk
        cmds.cycleCheck(e=False)
        cmds.undoInfo(openChunk=True, chunkName=_name)

        result = function(*args, **kwargs)

        # Close Chunk
        cmds.undoInfo(closeChunk=True)
        cmds.cycleCheck(e=True)

        return result

    return undo_func


# -------------------------------------------------
# ------------ PyQt Core Functions ----------------
# -------------------------------------------------
style_sheet_dict: dict = {"line_edit":
                              """
                              QLineEdit 
                              { 
                              height: 20; 
                              border-style: outset; 
                              border-width: 3px; 
                              border-radius: 4px;
                              }"""
    ,
                          "button_blue": """
                        QPushButton
                            {
                                height: 22.5;
                                width: 90;
                                background-color: rgb(20, 20, 20);
                                border-style: outset;
                                border-width: 2px;
                                border-radius: 5px;
                                font: bold; 
                            }
                            QPushButton:pressed 
                            {
                                background-color: rgb(23, 153, 231);
                                color: black; 
                            }

                            QPushButton:hover 
                            {
                                border-color: rgb(23, 153, 231);
                            }
                        """
    ,
                          "button_green": """
                       QPushButton
                           {
                               height: 22.5;
                               width: 90;
                               background-color: rgb(20, 20, 20);
                               border-style: outset;
                               border-width: 2px;
                               border-radius: 5px;
                           }
                           QPushButton:pressed 
                           {
                               background-color: rgb(37, 211, 102);
                               color: black; 
                           }

                           QPushButton:hover 
                           {
                               border-color: rgb(37, 211, 102);
                           }
                       """
    ,
                          "button_red": """
                       QPushButton
                           {
                               height: 22.5;
                               width: 90;
                               background-color: rgb(20, 20, 20);
                               border-style: outset;
                               border-width: 2px;
                               border-radius: 5px;
                           }
                           QPushButton:pressed 
                           {
                               background-color: rgb(255, 58, 58);
                                color: black; 
                           }

                           QPushButton:hover 
                           {
                               border-color: rgb(255, 58, 58);
                           }
                       """
    ,

                          "label":
                              """
                              QLabel
                              {   
                                  height: 20;
                                  width: 80;
                                  background-color: rgb(20, 20, 20);
                                  border-style: outset;
                                  border-width: 2px;
                                  border-radius: 5px;
                                  font: bold; 
                              }
                              """
    ,
                          "small_label":
                              """
                              QLabel
                              {   
                                  height: 20;
                                  width: 60;
                                  background-color: rgb(20, 20, 20);
                                  border-style: outset;
                                  border-width: 2px;
                                  border-radius: 5px;
                                  font: bold; 
                              }
                              """

    ,
                          "spin_box":
                              """
                              QDoubleSpinBox 
                              {
                                  height: 20; 
                                  border-style: outset; 
                                  border-width: 2px; 
                                  border-radius: 5px;
                              }
                              """
    ,
                          "group_box":
                              """
                              QGroupBox 
                              {
                                  font: bold 13px;
                                  border-style: outset;
                                  border-width: 2px;
                                  border-radius: 6px;
                                  border-color: black;
                                  padding: 10px;
                              }
                              """
                          }


def apply_style_sheet(widget_list: QtWidgets,
                      stylesheet):
    #
    for widget in widget_list:
        widget.setStyleSheet(stylesheet)


def beautiful_organize(qt_grp_box_name: QtWidgets,
                       parent_layout: QtWidgets,
                       organize_layout: QtWidgets):
    #
    qt_grp_box = QtWidgets.QGroupBox(qt_grp_box_name)
    qt_grp_box.setLayout(parent_layout)
    organize_layout.addWidget(qt_grp_box)
    qt_grp_box.setStyleSheet(style_sheet_dict["group_box"])


def get_maya_main_window():
    main_window_ptr = OMUI.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


def connect_widget_to_widget(drv_widget: QtWidgets,
                             driven_widget_list: [QtWidgets]):
    widget_status = drv_widget.isChecked()  # Fixed typo
    for widget in driven_widget_list:
        widget.setEnabled(widget_status)


# -------------------------------------------------
# ------------ Attrs Core Functions ---------------
# -------------------------------------------------

def convert_selected_textfield(input_str_list: str):
    """
    Cleans and processes a string representing a list, returning a sorted list of items.

    Args:
        input_str_list (str): A string containing a representation of a list.

    Returns:
        list: A sorted list of cleaned items.
    """

    # Remove unwanted characters and split into items
    cleaned_list: list = input_str_list.translate({ord(c): None for c in "[] '"}).split(",")

    # Remove leading 'u' from each item and return the sorted list
    return sorted(item.lstrip("u") for item in cleaned_list)


def get_channelbox_attr():
    """
        Retrieves the first selected attribute from the Maya Channel Box.

        This function queries the global Maya Channel Box (`$gChannelBoxName`) to
        determine the currently selected main attributes. If no attributes are
        selected or an error occurs, it returns an empty list.

        Returns:
            list: A list containing the name of the first selected attribute.
                  Returns an empty list if no attributes are selected or a
                  TypeError occurs.
        """
    try:
        channel_box_attr = mel.eval('$temp=$gChannelBoxName')
        return cmds.channelBox(channel_box_attr, query=True, sma=True)[0] or []
    except TypeError:
        pass


def create_custom_attributes(objects: list,
                             attrs_names: list,
                             chosen_separator_attr: str,
                             attribute_type: str,
                             min_val: float,
                             max_val: float):
    """
        Creates custom attributes on a list of objects in Autodesk Maya.

        This function adds custom attributes to the specified objects. It checks if the
        given separator attribute already exists on the object, and if not, creates it.
        It then either adds a set of "enum" attributes or regular attributes (e.g.,
        "float") based on the specified `attribute_type`. Optionally, for float attributes,
        the minimum and maximum values can be set.

        Args:
            objects (list): A list of object names (e.g., curve names) to which the custom
                            attributes will be added.
            attrs_names (list): A list of names for the attributes to be created.
            chosen_separator_attr (str): The name of the separator attribute used to group
                                         the custom attributes together.
            attribute_type (str): The type of the attributes to be created. Can be either
                                  "enum", "float" or "bool".
            min_val (float): The minimum value for float attributes (if `attribute_type` is "float").
            max_val (float): The maximum value for float attributes (if `attribute_type` is "float").

        Returns:
            None: This function does not return any value. It directly modifies the objects.

        Notes:
            - If the `chosen_separator_attr` does not exist on an object, it will be created as an
              "enum" attribute with the value `=======`.
            - The `attrs_names` attributes will be added or deleted based on whether they already exist
              on the object.
            - If `attribute_type` is set to "float", the function will add a float range between `min_val`
              and `max_v
    """

    if not attrs_names or not objects:
        return

    for crv in objects:
        ctrl_exist_attributes = set(cmds.listAttr(crv, ud=True) or [])

        if chosen_separator_attr not in ctrl_exist_attributes:
            cmds.addAttr(crv,
                         ln=chosen_separator_attr, nn=chosen_separator_attr, at="enum", en="=======", k=True, r=True)

        [cmds.deleteAttr(crv, attribute=attr) for attr in attrs_names if attr in ctrl_exist_attributes]

        if attribute_type == "enum":
            enum_attr = ":".join(attrs_names)
            cmds.setAttr(f"{crv}.{chosen_separator_attr}", lock=False, channelBox=True)
            cmds.addAttr(f"{crv}.{chosen_separator_attr}", e=True, en=enum_attr, k=True, r=True)
        else:
            cmds.addAttr(f"{crv}.{chosen_separator_attr}", e=True, en="=======", k=True, r=True)

            for attr in attrs_names:
                cmds.addAttr(crv, ln=attr, nn=attr, at=attribute_type, k=True, r=True)
                if attribute_type == "float":
                    cmds.addAttr(f"{crv}.{attr}", e=True, min=min_val, max=max_val)

        cmds.setAttr(f"{crv}.{chosen_separator_attr}", keyable=False, channelBox=True)


def delete_all_attrs(objects: list):
    """
        Deletes all user-defined attributes from a list of objects in Autodesk Maya.

        This function iterates over a list of objects and deletes any user-defined
        attributes (`ud`) associated with them. If an object has user-defined attributes,
        they are removed using the `deleteAttr` command.

        Args:
            objects (list): A list of object names (e.g., nodes like curves or meshes) from
                            which user-defined attributes will be deleted.

        Returns:
            None: This function does not return any value. It modifies the objects directly.

        Notes:
            - The function will only delete attributes marked as user-defined .
            - If an object has no user-defined attributes, it will be skipped without any errors.
        """

    [
        cmds.deleteAttr(crv, attribute=attr)
        for crv in objects
        for attr in cmds.listAttr(crv, ud=1) or []
    ]

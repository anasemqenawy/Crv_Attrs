import importlib
from maya import cmds

try:
    from PySide2 import QtCore, QtWidgets
except ModuleNotFoundError:
    from PySide6 import QtCore, QtWidgets

from crv_attrs import core

importlib.reload(core)


class SmartAttributeUI(QtWidgets.QDialog):
    def __init__(self, parent=core.get_maya_main_window()):
        super().__init__(parent)

        self.setWindowTitle("{RigTopia::Smart_Attribute}")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowMinimizeButtonHint)
        self.setMinimumWidth(310)
        self.setMaximumHeight(300)

        self.create_widgets()
        self.create_layout()
        self.define_widgets_style_sheet()
        self.create_connections()

    def create_widgets(self):
        # Objects Widgets
        self.get_objects_button = QtWidgets.QPushButton(":: Objects ::")
        self.objects_field = QtWidgets.QLineEdit()
        self.objects_field.setPlaceholderText("Select Scene Objects")

        # Separator Widgets
        self.get_separator_button = QtWidgets.QPushButton(":: Separator ::")
        self.separator_attr_field = QtWidgets.QLineEdit()
        self.separator_attr_field.setPlaceholderText("Enum To Separate Attrs")

        # Attributes Widgets
        self.attrs_label = QtWidgets.QLabel(":: Attributes ::")
        self.attrs_field = QtWidgets.QLineEdit()
        self.attrs_field.setPlaceholderText("Example: attr_01/attr_02/..")

        # Attribute Type Widgets
        self.attribute_type_group = QtWidgets.QButtonGroup()
        self.float_radio = QtWidgets.QRadioButton("float")
        self.bool_radio = QtWidgets.QRadioButton("bool")
        self.enum_radio = QtWidgets.QRadioButton("enum")
        self.attribute_type_group.addButton(self.float_radio)
        self.attribute_type_group.addButton(self.bool_radio)
        self.attribute_type_group.addButton(self.enum_radio)
        self.bool_radio.setChecked(True)

        # Min/Max Values
        self.min_val_label = QtWidgets.QLabel(":: Min ::")
        self.min_val_field = QtWidgets.QDoubleSpinBox()
        self.min_val_field.setRange(-10000, 10000)
        self.min_val_field.setValue(0)
        self.min_val_field.setEnabled(False)

        self.max_val_label = QtWidgets.QLabel(":: Max ::")
        self.max_val_field = QtWidgets.QDoubleSpinBox()
        self.max_val_field.setRange(-10000, 10000)
        self.max_val_field.setValue(10)
        self.max_val_field.setEnabled(False)

        # Run Widgets
        self.delete_attrs_button = QtWidgets.QPushButton(":: Delete All ::")
        self.add_attrs_button = QtWidgets.QPushButton(":: Add New ::")

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        organize_layout = QtWidgets.QVBoxLayout()

        objects_layout = QtWidgets.QHBoxLayout()
        objects_layout.addWidget(self.get_objects_button)
        objects_layout.addWidget(self.objects_field)
        core.beautiful_organize(qt_grp_box_name="Objects",
                                parent_layout=objects_layout,
                                organize_layout=organize_layout)

        separator_layout = QtWidgets.QHBoxLayout()
        separator_layout.addWidget(self.get_separator_button)
        separator_layout.addWidget(self.separator_attr_field)
        core.beautiful_organize(qt_grp_box_name="Separator",
                                parent_layout=separator_layout,
                                organize_layout=organize_layout)

        attributes_layout = QtWidgets.QHBoxLayout()
        attributes_layout.addWidget(self.attrs_label)
        attributes_layout.addWidget(self.attrs_field)
        core.beautiful_organize(qt_grp_box_name="Attributes",
                                parent_layout=attributes_layout,
                                organize_layout=organize_layout)

        attributes_type_layout = QtWidgets.QHBoxLayout()
        attributes_type_layout.addWidget(self.float_radio)
        attributes_type_layout.addWidget(self.bool_radio)
        attributes_type_layout.addWidget(self.enum_radio)
        core.beautiful_organize(qt_grp_box_name="Attributes_Type",
                                parent_layout=attributes_type_layout,
                                organize_layout=organize_layout)

        min_max_layout = QtWidgets.QHBoxLayout()
        min_max_layout.addWidget(self.min_val_label)
        min_max_layout.addWidget(self.min_val_field)
        min_max_layout.addStretch()
        min_max_layout.addWidget(self.max_val_label)
        min_max_layout.addWidget(self.max_val_field)
        core.beautiful_organize(qt_grp_box_name="Max____Min",
                                parent_layout=min_max_layout,
                                organize_layout=organize_layout)

        build_layout = QtWidgets.QHBoxLayout()
        build_layout.addWidget(self.delete_attrs_button)
        build_layout.addWidget(self.add_attrs_button)
        core.beautiful_organize(qt_grp_box_name="Build",
                                parent_layout=build_layout,
                                organize_layout=organize_layout)

        main_layout.addLayout(organize_layout)

    def define_widgets_style_sheet(self):
        core.apply_style_sheet(widget_list=[self.get_objects_button,
                                            self.get_separator_button,
                                            ],
                               stylesheet=core.style_sheet_dict["button_blue"])

        core.apply_style_sheet(widget_list=[self.add_attrs_button,
                                            ],
                               stylesheet=core.style_sheet_dict["button_green"])

        core.apply_style_sheet(widget_list=[self.delete_attrs_button,
                                            ],
                               stylesheet=core.style_sheet_dict["button_red"])

        core.apply_style_sheet(widget_list=[self.objects_field,
                                            self.separator_attr_field,
                                            self.attrs_field],
                               stylesheet=core.style_sheet_dict["line_edit"])

        core.apply_style_sheet(widget_list=[self.attrs_label,
                                            self.min_val_label,
                                            self.max_val_label],
                               stylesheet=core.style_sheet_dict["label"])

        core.apply_style_sheet(widget_list=[self.min_val_field,
                                            self.max_val_field],
                               stylesheet=core.style_sheet_dict["spin_box"])
        core.apply_style_sheet(widget_list=[self.bool_radio,
                                            self.float_radio,
                                            self.enum_radio],
                               stylesheet=core.style_sheet_dict["radio_button"])

    def create_connections(self):
        self.get_objects_button.clicked.connect(self.get_scene_objects)
        self.get_separator_button.clicked.connect(self.get_channelbox_separator)

        self.attribute_type_group.buttonClicked.connect(self.get_attrs_type)
        self.float_radio.toggled.connect(self.control_double_field)

        self.add_attrs_button.clicked.connect(self.add_attrs)
        self.delete_attrs_button.clicked.connect(self.delete_all_attributes)

    def control_double_field(self):

        core.connect_widget_to_widget(drv_widget=self.float_radio,
                                      driven_widget_list=[self.min_val_field,
                                                          self.max_val_field])

    def get_scene_objects(self):
        selected_curves = cmds.ls(sl=1, type="transform")
        self.objects_field.setText(str(selected_curves))

    def get_channelbox_separator(self):
        attr = core.get_channelbox_attr()
        self.separator_attr_field.setText(str(attr))

    def get_attrs_names(self):
        typed_attributes = self.attrs_field.text()
        return typed_attributes.split("/") if typed_attributes else []

    def get_attrs_type(self):
        for button in self.attribute_type_group.buttons():
            if button.isChecked():
                return str(button.text())

    @core.enable_undo
    def add_attrs(self):
        attrs_names = self.get_attrs_names()
        chosen_separator_attr = self.separator_attr_field.text()
        objects = core.convert_selected_textfield(self.objects_field.text())
        min_val = self.min_val_field.value()
        max_val = self.max_val_field.value()

        if objects:
            if chosen_separator_attr:
                if attrs_names:
                    core.create_custom_attributes(objects=objects,
                                                  attrs_names=attrs_names,
                                                  chosen_separator_attr=chosen_separator_attr,
                                                  attribute_type=self.get_attrs_type(),
                                                  min_val=min_val,
                                                  max_val=max_val)

    @core.enable_undo
    def delete_all_attributes(self):
        objects = core.convert_selected_textfield(self.objects_field.text())
        core.delete_all_attrs(objects=objects)

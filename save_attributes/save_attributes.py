# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SaveAttributes
                                 A QGIS plugin
 csv save
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-12-15
        git sha              : $Format:%H$
        copyright            : (C) 2020 by R.Bosman
        email                : robbert.bosman@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

# Toevoegen:
from qgis.core import QgsProject, Qgis, QgsMessageLog
from PyQt5.QtWidgets import QAction, QFileDialog
from qgis.utils import iface

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .save_attributes_dialog import SaveAttributesDialog
import os.path


class SaveAttributes:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'SaveAttributes_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Save Attributes')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('SaveAttributes', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/save_attributes/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Save Attributes as CSV'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

        # add toolbar button and menu item, werkt niet
        # self.iface.addToolBarIcon(self.action)
        # self.iface.addPluginToMenu("&Test plugins", self.action)


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Save Attributes'),
                action)
            self.iface.removeToolBarIcon(action)


    def select_output_file(self):
        filename, _filter = QFileDialog.getSaveFileName(
            self.dlg, "Select   output file ","", '*.csv')
        self.dlg.lineEdit.setText(filename)


    def run(self):
        """Run method that performs all the real work"""

        # print('run') werkt niet 

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            # self.dlg = SaveAttributesDialog()
            # self.dlg.pushButton.clicked.connect(self.select_output_file)

        # Uit demo:
        # Fetch the currently loaded layers
        layers = QgsProject.instance().layerTreeRoot().children()
        # Clear the contents of the comboBox from previous runs
        # self.dlg.comboBox.clear()
        # Populate the comboBox with names of all the loaded layers
        # self.dlg.comboBox.addItems([layer.name() for layer in layers])

        # show the dialog
        # self.dlg.show()
        # Run the dialog event loop
        # result = self.dlg.exec_()
        # See if OK was pressed
        # if result:
        #     # Do something useful here - delete the line containing pass and
        #     # substitute with your code.
        #     # pass

        #     # Uit demo:
        #     filename = self.dlg.lineEdit.text()
        #     # print('filename', filename) wert miet

        #     # QgsMessageLog.logMessage('filename', tag, level) level is default 0
        #     QgsMessageLog.logMessage('filename {0}'.format(filename), 'tets', 0)  


        #     with open(filename, 'w') as output_file:
        #         selectedLayerIndex = self.dlg.comboBox.currentIndex()
        #         selectedLayer = layers[selectedLayerIndex].layer()
        #         fieldnames = [field.name() for field in selectedLayer.fields()]
        #         # write header
        #         line = ','.join(name for name in fieldnames) + '\n'
        #         output_file.write(line)
        #         # wirte feature attributes
        #         for f in selectedLayer.getFeatures():
        #             line = ','.join(str(f[name]) for name in fieldnames) + '\n'
        #             output_file.write(line)

        #     self.iface.messageBar().pushMessage(
        #         "Success", "Output file written at " + filename,
        #         level=Qgis.Success, duration=3)


        # layer = qgis.utils.iface.activeLayer()
        # layer = QgsProject.instance.activeLayer()
        # layer = iface.activeLayer()
        # selected_features = layer.selectedFeatures()

        # layer.startEditing()
        # for i in selected_features:
        #     QgsMessageLog.logMessage('Feature {0}'.format(i['noise']), 'loggie', 0)  
        #     layer.changeAttributeValue(i.id(), 11, '{0}'.format(not i['noise']))
        #     # attrs = i.attributeMap()
        #     # for (k,attr) in attrs.iteritems():
        #     #     # print "%d: %s" % (k, attr.toString())   
        #     #     QgsMessageLog.logMessage('Attr {0} {1}'.format(k, attr), 'loggie', 0)  

      
        # layer.commitChanges()



        # Toggle noise:
        layer = iface.activeLayer()

        # Controleer of de juiste laag is geselecteerd
        field_index = layer.fields().indexFromName('noise')

        if field_index != -1:

            selected_features = layer.selectedFeatures()

            if len(selected_features) > 0:

                layer.startEditing()
                for i in selected_features:
                    QgsMessageLog.logMessage('Feature {0}'.format(i['noise']), 'loggie', 0)  
                    if i['cat'] != 3:
                        layer.changeAttributeValue(i.id(), 11, '{0}'.format(not i['noise']))      
                layer.commitChanges()

                self.iface.messageBar().pushMessage("Success", "Noise geflipt", level=Qgis.Success, duration=3)

            else:

                self.iface.messageBar().pushMessage("Niks geselecteerd", "", level=Qgis.Warning, duration=3)

        else:

            self.iface.messageBar().pushMessage("Selecteerd telling!", "", level=Qgis.Warning, duration=3)
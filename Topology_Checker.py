# -*- coding: utf-8 -*-
"""
/***************************************************************************
 TopologyChecker
                                 A QGIS plugin
 To Check the Gaps & Ovelaps
                              -------------------
        begin                : 2019-09-16
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Prabhath W.J.K.A.N. Survey Dept. of Sri Lanka
        email                : npjasinghe@gmail.com

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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon,QFileDialog
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from Topology_Checker_dialog import TopologyCheckerDialog
import os.path
from qgis.core import*
from qgis.gui import*
from PyQt4.QtGui import*
from PyQt4.QtCore import*
import processing
from qgis.utils import *
from PyQt4 import QtGui
import os, sys
import qgis
from qgis.utils import iface
import sys, time
import glob,gc


from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QFile, QFileInfo
from qgis import core, gui, utils
from qgis.core import QgsRasterLayer
from qgis.gui import QgsMapCanvasLayer
from qgis.utils import iface





class TopologyChecker:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgisInterface
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
            'TopologyChecker_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
        self.dlg = TopologyCheckerDialog()


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&3 Topology Checker')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'TopologyChecker')
        self.toolbar.setObjectName(u'TopologyChecker')

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
        return QCoreApplication.translate('TopologyChecker', message)


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

        # Create the dialog (after translation) and keep reference
        #self.dlg = TopologyCheckerDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/TopologyChecker/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Check the Topology V0.1'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&3 Topology Checker'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        
        # Get all loaded layers in the interface
        layers = self.iface.legendInterface().layers()
        # Create an empty list which we can populate
        layer_list = []
        # For every item (which we call "layer") in all loaded layers
        for layer in layers:
            # Add it to the list
            layer_list.append(layer.name())
        # Clear comboBox (useful so we don't create duplicate items in list)
        self.dlg.comboBox.clear()
        # Add all items in list to comboBox
        self.dlg.comboBox.addItems(layer_list)
        
        self.dlg.comboBox2.clear()
        # Add all items in list to comboBox
        self.dlg.comboBox2.addItems(layer_list)
        #cff = this.ComboBox.GetItemText(this.comboBox.SelectedItem);
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            window = iface.mainWindow()
            self.iface.mapCanvas().refreshAllLayers() 
            selectedLayerIndex = self.dlg.comboBox.currentIndex()
            selectedLayer = layers[selectedLayerIndex]
        
            selectedLayerIndex2 = self.dlg.comboBox2.currentIndex()
            selectedLayer2 = layers[selectedLayerIndex2]
            
            outputs_QGISDEFINECURRENTPROJECTION_1=processing.runalg('qgis:definecurrentprojection', selectedLayer2,'EPSG:5235')
            outputs_QGISDISSOLVE_1=processing.runalg('qgis:dissolve', selectedLayer2,True,'Layer',None)
            outputs_SAGASHAPESBUFFERFIXEDDISTANCE_1=processing.runalg('saga:shapesbufferfixeddistance', outputs_QGISDISSOLVE_1['OUTPUT'],2.0,1.0,5.0,True,True,None)
            outputs_SAGASHAPESBUFFERFIXEDDISTANCE_2=processing.runalg('saga:shapesbufferfixeddistance', outputs_SAGASHAPESBUFFERFIXEDDISTANCE_1['BUFFER'],30.0,1.0,5.0,True,False,None)
            outputs_QGISCLIP_1=processing.runalg('qgis:clip', outputs_QGISDISSOLVE_1['OUTPUT'],outputs_SAGASHAPESBUFFERFIXEDDISTANCE_2['BUFFER'],None)
            cLayer = iface.mapCanvas().currentLayer()
            outputs_QGISCLIP_2=processing.runalg('qgis:clip', selectedLayer,outputs_SAGASHAPESBUFFERFIXEDDISTANCE_2['BUFFER'],None)
            outputs_QGISCLIP_3=processing.runandload('qgis:clip', selectedLayer,outputs_SAGASHAPESBUFFERFIXEDDISTANCE_2['BUFFER'],None)
            
            self.iface.mapCanvas().refreshAllLayers()
            cLayer = iface.mapCanvas().currentLayer()            
            count1=cLayer.featureCount()
            cLayer = iface.mapCanvas().currentLayer()            
            QgsMapLayerRegistry.instance().removeMapLayer(cLayer) #!!!!
            self.iface.mapCanvas().refreshAllLayers()
            if count1==0:
                QMessageBox.information(window,"Info", "There is no overlap or gaps")
            else:
                outputs_QGISUNION_1=processing.runalg('qgis:union', selectedLayer2,outputs_QGISCLIP_2['OUTPUT'],None)
                outputs_QGISCLIP_3=processing.runalg('qgis:clip', outputs_QGISCLIP_1['OUTPUT'],outputs_QGISCLIP_2['OUTPUT'],None)
                outputs_QGISDISSOLVE_2=processing.runalg('qgis:dissolve', outputs_QGISUNION_1['OUTPUT'],True,None,None)
                outputs_QGISPOLYGONSTOLINES_1=processing.runalg('qgis:polygonstolines', outputs_QGISCLIP_3['OUTPUT'],None)
                outputs_QGISDELETEHOLES_1=processing.runalg('qgis:deleteholes', outputs_QGISDISSOLVE_2['OUTPUT'],None)
                outputs_QGISPOLYGONIZE_1=processing.runalg('qgis:polygonize', outputs_QGISPOLYGONSTOLINES_1['OUTPUT'],False,True,None)
                outputs_GRASS7VCLEAN_1=processing.runandload('grass7:v.clean', outputs_QGISPOLYGONIZE_1['OUTPUT'],10,0.001,('0,2000,0,2000'),-1.0,0.0001,None,'')
                cLayer = iface.mapCanvas().currentLayer()
                layer = self.iface.activeLayer()
                myfilepath= iface.activeLayer().dataProvider().dataSourceUri()                
                QgsMapLayerRegistry.instance().removeMapLayer(cLayer)
                layer = QgsVectorLayer(myfilepath, 'Overlaps', 'ogr')
                QgsMapLayerRegistry.instance().addMapLayer(layer)

                #---- ---------------iface activity--------------------------------------
                cLayer = iface.mapCanvas().currentLayer()
                outputs_QGISFIELDCALCULATOR_1=processing.runalg('qgis:fieldcalculator', cLayer,'ex',0,10.0,4.0,True,'$area',None)
                QgsMapLayerRegistry.instance().removeMapLayer(cLayer)

                layer = QgsVectorLayer(outputs_QGISFIELDCALCULATOR_1['OUTPUT_LAYER'],'Overlaps', 'ogr')		 #--"CM_Lot" is the desplay name of the CM.shp  ----
                QgsMapLayerRegistry.instance().addMapLayer(layer)
                cLayer = iface.mapCanvas().currentLayer()
                expr = QgsExpression("ex<1")
                it = cLayer.getFeatures( QgsFeatureRequest( expr ) )
                ids = [i.id() for i in it]
                cLayer.setSelectedFeatures( ids )
                cLayer.startEditing()
                for fid in ids:
                    cLayer.deleteFeature(fid)
                cLayer.commitChanges()
                
                a=r"C:\Users\Survey Department\Desktop\delete\test\d.shp"
                outputs_SAGADIFFERENCE_1=processing.runalg('saga:difference', outputs_QGISDELETEHOLES_1['OUTPUT'],outputs_QGISDISSOLVE_2['OUTPUT'],True,None)
                outputs_QGISFIELDCALCULATOR_2=processing.runalg('qgis:fieldcalculator', outputs_SAGADIFFERENCE_1['RESULT'],'ex',0,10.0,4.0,True,'$area',None)
                layer = QgsVectorLayer(outputs_QGISFIELDCALCULATOR_2['OUTPUT_LAYER'],'test', 'ogr')		 #--"CM_Lot" is the desplay name of the CM.shp  ----
                QgsMapLayerRegistry.instance().addMapLayer(layer)
                #---- ---------------iface activity--------------------------------------
                cLayer = iface.mapCanvas().currentLayer()
                expr = QgsExpression("ex<1")
                it = cLayer.getFeatures( QgsFeatureRequest( expr ) )
                ids = [i.id() for i in it]
                cLayer.setSelectedFeatures( ids )
                cLayer.startEditing()
                for fid in ids:
                    cLayer.deleteFeature(fid)
                cLayer.commitChanges()
                cLayer = iface.mapCanvas().currentLayer()
                layer = self.iface.activeLayer()
                myfilepath= iface.activeLayer().dataProvider().dataSourceUri()                
                QgsMapLayerRegistry.instance().removeMapLayer(cLayer)
                layer = QgsVectorLayer(myfilepath, 'Gaps', 'ogr')
                QgsMapLayerRegistry.instance().addMapLayer(layer)

                layer = iface.activeLayer()
                layer=None
                for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
                    if lyr.name() == "Gaps":
                        layer = lyr
                        count1=layer.featureCount()
                        if count1==0:
                            QgsMapLayerRegistry.instance().removeMapLayer( layer)
                            QMessageBox.information(window,"Info", "There is no gaps")
                            break
                for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
                    if lyr.name() == "Overlaps":
                        layer = lyr
                        count1=layer.featureCount()
                        if count1==0:
                            QgsMapLayerRegistry.instance().removeMapLayer( layer)
                            QMessageBox.information(window,"Info", "There is no overlap")
                            break
            pass

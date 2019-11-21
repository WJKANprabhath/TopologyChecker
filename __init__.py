# -*- coding: utf-8 -*-
"""
/***************************************************************************
 TopologyChecker
                                 A QGIS plugin
 To Check the Gaps & Ovelaps
                             -------------------
        begin                : 2019-09-16
        copyright            : (C) 2019 by Prabhath W.J.K.A.N. Survey Dept. of Sri Lanka
        email                : npjasinghe@gmail.com

        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load TopologyChecker class from file TopologyChecker.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .Topology_Checker import TopologyChecker
    return TopologyChecker(iface)

####################
IMT-A WiMAX scenario
####################

In this chapter, some predifined functions are introduced.

================================
Introduction of other parameters
================================

.. code-block:: python

   ...
   ...

   bsCreator = wimac.support.nodecreators.WiMAXBSCreator(stationIDs, Config)
   ueCreator = wimac.support.nodecreators.WiMAXUECreator(stationIDs, Config)

   scenario = scenarios.builders.CreatorPlacerBuilderUrbanMacro(
       bsCreator,
       ueCreator,
       sectorization = True,
       numberOfCircles = 0,
       numberOfNodes = 6)

   ...
   ...

The codes listed above are part of ``MY-OPENWNS/tests/system/WiMAC-Tests--main--1.2/configIMTA/configUMa.py``. In this test, ``wimac.support.nodecreators.WiMAXBSCreator`` is used to create base stations and ``wimac.support.nodecreators.WiMAXUECreator`` user terminals. The predefined creator placer for Urban Macro scenario is used to create a Urban Macro scenario package. This package can be found at ``MY-OPENWNS/framework/scenarios/PyConfig/scenarios/builders/creatorplacer.py``, as shown below.

.. code-block:: python

   ...
   ...
   class CreatorPlacerBuilderUrbanMacro(CreatorPlacerBuilder):

       def __init__(self, bsCreator, utCreator, sectorization, numberOfCircles = 2, numberOfNodes = 30):
         super(CreatorPlacerBuilderUrbanMacro, self).__init__(bsCreator,
                                                              scenarios.ituM2135.UrbanMacroBSPlacer(numberOfCircles),
                                                              scenarios.ituM2135.UrbanMacroAntennaCreator(sectorization),
                                                              utCreator,
                                                              scenarios.ituM2135.UrbanMacroUEPlacer(numberOfNodes, minDistance=25),
                                                              scenarios.ituM2135.UrbanMacroChannelModelCreator())

In this package, several predifened ituM2135 Urban Macro parameters are used to setup a scenario for Urban Macro enrivoment.

=================================================================
Show the positions of base stations and user terminal with pytree
=================================================================

In ITU scenario packages, user terminals are randomized placed around base station. Here we use the ``HexagonalPlacer`` as a base station placer and ``HexagonalAreaPlacer`` as a user terminal placer for Urban Micro, Urban Macro, Rural Macro and Suburban Macro scenarios; use ``LinearPlacer`` as base station placer and ``RectangularAreaPlacer`` as user terminal placer for Indoor Hotspot scenarios. All these functions are defined in ``MY-OPENWNS/framework/scenarios/PyConfig/scenarios/placer/``. All ``AreaPlacer`` are randomized placer.

.. code-block:: python
   
   scenarios.ituM2135.UrbanMacroChannelModelCreator()

``UrbanMacroChannelModelCreator`` is a child class of ``SingleChannelModelCreator``. It defines transceiver pairs and pathloss, shadowing and fastfading for all these transceiver pairs.

Many different node types are defined in OPENWNS. All these nodes are child classes of ``wns.Node``. Here we introduce two functions of WNS Node, namely, ``setProperty(propertyName, propertyValue)`` and the ``getProperty(propertyName)``. With function setProperty you can add properties to node. ``propertyName`` is a string type parameter that gives property name and ``propertyValue`` saves the corresponding value for this property. The function ``getProperty`` takes the property name as the input parameter and returns the property value according to the input property name.



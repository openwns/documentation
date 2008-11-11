###########################################
Experiment 1: Maximum Throughput Estimation
###########################################

In the first experiment, we will learn how to setup a very simple
simulation campaign, run the simulations and evaluate the results.

In the following, we will assume that ``myFirstCampaign`` is the root
directory of the simulation campaign, created as described in the
previous section, and ``myFirstCampaign/Experiment1`` is the directory
where the simulations are stored.

In the beginning, this directory contains only the following files:

   campaignConfiguration.py

   simcontrol.py

``simcontrol.py`` is used to manage the simulation, i.e. creating the
scenarios, executing the simulations (either locally or in a
distributed grid, if available) and presenting information about the
current status. ``campaignConfiguration.py`` contains the parameters
which shall be simulated.

*********
config.py
*********

To complete the campaign, a configuration file ``config.py`` is
required that configures the scenario, nodes and the evaluation. For
the first experiment, a config.py can be found in
``openWNS/tests/system/WiFiMAC-Tests--main--1.0/PyConfig/experiment1``,
this file needs to be copied into the simulations directory.

In the following, we will go step-by-step through this configuration
file and explain the different steps that are required to setup a IEEE
802.11-based wireless network scenario. To concentrate on the
simulation process, the first scenario is kept as simple as possible:
One Access Point (AP) transmits data to a Station (STA), within a
distance d, see :ref:`figure-wifimac-experiment1`

.. _figure-wifimac-experiment1:

.. figure:: images/experiment1.*
   :align: center

   Scenario of experiment 1

Import Statements
=================

The file ``config.py`` for this scenario begins, as every python file,
with import statements.

.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment1.config.imports
   :language: python

Namely, we import

* The random number generator

* The simulator core ``wns.WNS``, plus classes to define dB, dBm and an interval.

* The traffic generator ``Constanze``.

* A virtual ARP and DNS server for the IP-Layer.

* From wifimac:
  * The support package that allows the generation of nodes.
  * The pathselection package (used for mesh networking, but required in all scenarios as every AP registers itself and its associated STAs)
  * The management information base
  * The evaluation structure for the wifimac and the ip layer

* The scenario package to define the radio environment.

Simulation Parameters
=====================

The next lines bundle the simulation parameters to allow for a better
overview and an easy change of parameters.

.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment1.config.simulationParameter
   :language: python

The statement ``from SimConfig import params`` is required for the
automatic generation of scenarios in the campaign: the object
``params`` contains member variables for every parameter that will be
changed in the campaign. In this case, it is

#. the simulation time,
#. the distance between the AP and the STA,
#. the offered traffic and
#. the ratio of uplink to downlink traffic.

Besides these parameters, this section also sets the simulation's
settling time, the logger level for the logger output, the packet
size, the start delay of the uplink and downlink and the network
frequency.

WNS Core Configuration
======================

The next section creates one instance of the WNS configuration, which
is used by the core module of the openWNS:

.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment1.config.WNS
   :language: python

The output strategy ``delete`` assures that old simulation output is
deleted prior to the simulation, and the write interval of the
status-report and the probes is set.

Scenario and Pathloss
=====================

The creation of the scenario instance is done by using the rise
module; additionally the default riseConfig and ofdmaPhyConfig is
instantiated. Furthermore, a managerPool is created which may be used to
manage different orthogonal radio channels.


.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment1.config.scenario
   :language: python

The configuration of the radio channel propagation parameters contains
modules for three major effects:

* Pathloss,
* Shadowing and
* Fast fading

.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment1.config.radioChannel
   :language: python

As we can see, shadowing and fast fading are switched off, whereas the pathloss uses a simple single-slope function

   pathloss = offset + freqFactor * log_10(frequency) + distFactor * log_10(distance)

Node Creation
=============

After we have defined the scenario and the radio environment, nodes
can be created using the node creator, which is contained in the
``wifimac.support`` package or in the respective IP-packages. We
distinguish between two types of nodes:

Virtual nodes
   are nodes that do not have a position (and mobility) and
   are accessed by other nodes directly, i.e. without using data
   transmissions. Most often, virtual nodes are used to emulate
   control or management functions in a simulator to ease the
   simulation setup.

Real nodes
   that simulate entities from the real world.

Virtual Nodes
-------------

In the first step, we set up virtual nodes for the ARP, DNS,
pathselection and the management information base; additionally, the
radio access network gateway (RANG) is created.

.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment1.config.NodeCreation.Virtual
   :language: python

The RANG is represents the portal to the Internet to which all APs in
the network must be connected. Therefore, the RANG also contains a
listener for all uplink-traffic of the STAs.

The virtual path selection server requires as input the number of
transceivers in the IEEE 802.11 network.

Access Point
------------

After some preparation to generate and store the node-ids, the AP is created:

.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment1.config.NodeCreation.AP
   :language: python

The creation requires two steps:

#. Generation of a transceiver configuration and

#. Creation of the AP node and addition to ``WNS.nodes``

These two steps are required because an AP can have potentially more
than one transceiver, each with a different configuration
(e.g. frequency). In our case, there is only one transceiver, having a
configuration with mainly default values, stored in
``wifimac.support.Transceiver.Mesh``. In the configuration file, only
the values for the transmission power, the beacon start delay, the
rate adaptation strategy and the threshold for the RTS/CTS
transmission is set.

For the creation of the AP, the function ``createAP`` of the node
creator is used::

  ap = nc.createAP(idGen, managerPool, apConfig)

Then, the ap object is added to the nodes, its id and the MAC
addresses (only one in this case) is stored and the AP is made known
to the RANG.

Station
-------

The first two steps are very similar to the creation of the AP:

#. Generation of a (STA) transceiver configuration (again with some few configuration settings) and

#. Creation of the STA node.

.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment1.config.NodeCreation.STA.node
   :language: python

In contrast to an AP, a STA also has a sink for the downlink traffic
(if active), and a source for the uplink traffic (if
active). Furthermore, both the RANG and the STA's IP layer have to
know which interface to use when communicating with each other, hence,
this has to be added to the IP routing layer. Finally, A downlink
source must be added to the RANG for every STA. All this is done in
the following lines:

.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment1.config.NodeCreation.STA.Traffic
   :language: python

Finally, the configured STA node can be added to ``WNS.nodes`` and to the ``staIDs``:

.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment1.config.NodeCreation.STA.Add
   :language: python

Evaluation
==========

In the final lines, the evaluation is installed, creating probe output
for the WiFiMAC hop-to-hop and the IP end-to-end layer:

.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment1.config.Probing
   :language: python


************************
campaignConfiguration.py
************************

After the simulation configuration is completed, we can set the
simulations parameters in the file ``campaignConfiguration.py``. The
contents of this file can be deleted and replaced with the following
lines.

.. note::

   An example ``campaignConfiguration.py`` can be found in
   ``openWNS/tests/system/WiFiMAC-Tests--main--1.0/PyConfig/experiment1``

First, we import the necessary package to handle the generation of
simulation scenarios:

.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment1.campaignConfiguration.import
   :language: python


Then, we setup a class ``Set`` that contains all simulation parameters that are used in ``config.py``:

.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment1.campaignConfiguration.Set
   :language: python

Next, an instance with the same name as in the ``config.py`` is created:

.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment1.campaignConfiguration.params
   :language: python

Then, the parameters in ``params`` can be populated with different
values. Each time the ``write()`` member function (inherited from the
class ``Parameters``) is called, the current values are fixed and
represent one simulation:

.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment1.campaignConfiguration.population
   :language: python

With this setup, 10 simulations are created, differentiated by the
offered downlink traffic between 1 and 10 Mb/s. This concludes the
file ``campaignConfiguration.py``.

********************************
Creating and Running Simulations
********************************

We are now ready to create the simulations and let them run locally.
As mentioned earlier, simulation execution is controlled by the script
``simcontrol.py``. With the command

.. code-block:: bash

   ./simcontrol.py --create-database

The ``campaignConfiguration.py`` is executed and the parameter values
are written to the database. Then, the command

.. code-block:: bash

  ./simcontrol.py --create-scenarios

reads the database and creates the for every scenario a sub-directory.
This can be validated by calling

.. code-block:: bash

   ./simcontrol.py -i

which should present the ten simulations, all in state ``NotQueued``
and the different simulation parameters. Before running all
simulations, a single one can be tested (e.g. for typos in
``config.py``) by changing into one of the new created directories and
running

.. code-block:: bash

   ./wns-core-dbg

If everything works right, the logging output of the simulation is
printed (consisting of the simulation time, the module, the FU and the
output), until the simulation time reaches 5 seconds and the simulation ends with

.. code-block:: bash

   wns::simulator::Application: shutdown complete

After this test, the simulations can be run one-by-one using the ``simcontrol.py`` script:

.. code-block:: bash

   ./simcontrol --execute-locally-with-state=NotQueued

This starts the serial execution of all defined scenarios. In a
"production" environment, a grid engine would be used to queue all
simulations and run them in parallel; the script is configured to work
together with the Sun Grid Engine. The installation and configuration
of this grid is out of the scope of this tutorial.

After some time, all 10 simulations should be finished, which can be controlled again with

.. code-block:: bash

   ./simcontrol.py -i

Each simulation directory now contains a directory ``output``, where
all probe output is stored in text files. Additionally, the output is
stored in the database, which can be accessed much more user-friendly
than browsing through text files.

*****************
Using the Wrowser
*****************

The Wrowser ("WNS Browser") is the openWNS graphical user interface to
browse, i.e. plot, simulation results in a fast and convenient way. It
is stared by calling

.. code-block:: bash

   openWNS/framework/Wrowser--main--0.9/wrowser

In the menu File are the different options to read the generated
simulation data, we select ``Open Campaign Database`` and then under
the appropriate user the campaign with the chosen name.

Next, we can draw the graph of offered traffic versus throughput as
measured by the IP-Layer in the RANG. As the offered traffic is a
simulation parameter, we select Figure -> New -> Parameter. In the new
window, the simulation parameter has to be set to ``offeredTraffic``,
this will be displayed in the x-axis. For the y-axis, we select
``ip.endToEnd.window.aggregated.bitThroughput_Moments`` [#]_ and select
``Draw`` in the bottom.

In the new figure, we should see that the traffic has not yet reached
the saturation point, i.e. even at 10 Mb/s all offered traffic reached
the STA.

.. rubric:: Footnotes

.. [#] The aggregated bit throughput probe shows the aggregated traffic which
       has left the RANG and has reached its final destination.

************
Experiments
************

#. Find the saturation throughput by editing the
   ``campaignConfiguration.py`` and enlarging the offered traffic
   until a point where the traffic cannot be carried completely. It is
   not necessary to delete existing scenarios, ``simcontrol.py`` will
   automatically identify the missing simulations and create them when
   told so.

#. How does the mean end-to-end delay react on increasing the offered
   traffic? How does the 99-percentile react?

#. Now, we want to add another parameter ``packetSize`` to select a
   packet size of 1480 and 80 Bytes.

   #. Change the static setting in ``config.py`` to a variable parameter.

   #. Add the parameter ``packetSize`` to the class ``Set`` in the
      ``campaignConfiguration.py``. As existing simulations do not
      have this parameter, but have used 1480B, we add this as the default value by specifying::

         packetSize = Int(default=1480*8)

   #. Add an outer for-loop to the existing one to vary the packetSize between 1480*8 and 80*8::

      	 for params.packetSize in [1480*8, 80*8]:
	     for i in xrange(1, 21):
    	     	 params.offeredTraffic = i * 1000000
  		 params.write()

   #. Create the simulations (in the database and the scenarios) and execute them.

   #. Evaluate the impact of the frame size on the saturation point using the Wrowser.



























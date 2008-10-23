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
required that cofigures the scenario, nodes and the evaluation. For
the first experiment, a config.py can be found in
``openWNS/tests/system/WiFiMAC-Tests--main--1.0/PyConfig/experiment1``,
this file needs to be copied into the simulations directory.

In the following, we will go step-by-step through this configuration
file and explain the different steps that are required to setup a IEEE
802.11-based wireless network scenario. To concentrate on the
simulation process, the first scenario is kept as simple as possible:
One Access Point (AP) transmits data to a Station (STA), within a
distance d.

.. figure:: example1.*
   :align: center

   Scenario of example 1

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

Transceiver Configuration
=========================

The configuration of each transceiver makes heavy use of Python's
object oriented features: the support package of the WiFiMAC module
provides a general class for an AP (or mesh point, MP) transceiver and
for a STA transceiver. The major difference between them is that the
first has beaconing enabled, whereas the second does not transmit any
beacons but scans each frequency in ``scanFrequencies`` for
``scanDuration`` before the association to the strongest beacon takes
place.

By deriving from either ``wifimac.support.Transceiver.Mesh`` or
``wifimac.support.Transceiver.Station``, a new class can be generated
which inherits the default configuration; this default values can the
be changed accordingly. Additionally, the creator function
``__init__`` can be changed according to the requirements of the
scenario.

First, let us look at the specialized configuration of
``MyAPTransceiver``:

.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment1.config.nodeConfiguration.AP
   :language: python

* New ``__init__`` function requires the initial beacon start delay as
  parameter, this allows to schedule the beacon transmissions by hand
  to avoid beacon collisions.

* Upon being called (which happens every time an instance of this
  class is created), the ``__init__`` function first calls the
  ``__init__`` function of its superclass, which requires the
  transceiver frequency as a parameter.

* Then, the parameters are changed in the following way:

  #. The transmission power is set to 20 dBm

  #. The beacon delay is set to the given value

  #. The rate adaptation strategy is set to ``Opportunistic``, which
     uses a Packet Error Rate (PER) statistic to search for the
     optimal transmission rate.

  #. Finally, the threshold to precede every frame transaction with an
     RTS/CTS is set to a high value, i.e. RTS/CTS is switched off.

The configuration class of the STA transceiver looks very similar:

.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment1.config.nodeConfiguration.STA
   :language: python

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
``wifimac.support`` package or in the resepective IP-packages. We
distinguis between two types of nodes:

Virtual nodes
   are nodes that do not have a position (and mobility) and
   are accessed by other nodes directly, i.e. without using data
   transmissions. Most often, virtual nodes are used to emulate
   control or management functions in a simulator to ease the
   simulation setup.

Real nodes
   that simulate entities from the real world.

**Virtual Nodes**

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

**Access Point**

After some preparation to generate and store the node-ids, the AP is created:

.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment1.config.NodeCreation.AP
   :language: python

Mainly, five steps are required for this procedure:

#. Generate an instance of the ``Node`` class of the ``wifimac.support`` package with a given position.
   ``apConfig = wifimac.support.Node(position = wns.Position(0,0,0))``

#. Add one or more transceivers to this node; here, we use the pre-defined ``MyAPTransceiver``.
   ``apConfig.transceivers.append(MyAPTransceiver(beaconDelay = 0.001))``

#. Generate an ap object using the node creator with the node instance.
   ``ap = nc.createAP(idGen, managerPool, apConfig)``

#. Add the ap object to the nodes
   ``WNS.nodes.append(ap)``

#. Add the ap object to the RANG
   ``rang.dll.addAP(ap)``

**Station**

The following creation of the station takes more lines, mostly used to
configure the IP-Layer and the traffic generation:

.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment1.config.NodeCreation.STA
   :language: python

After the creation of the ``staConfig`` (using the parameter
``distance`` to set its position) and the ``sta`` object by the node
creator, both the downlink and the uplink must be created, using the
poisson load generator from ``Constanze``. Then, the IP routing table
is populated with a route from the STA to the RANG and from the RANG
to the STA.

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

First, we import the neccessary package to handle the automatic
generation of simulation scenarios::

	import wnsrc
	from pywns.simdb.Parameters import Parameters, Bool, Int, Float, String

Then, we setup a class ``Set`` that contains all simulation parameters that are used in ``config.py``::

	class Set(Parameters):
	      simTime = Float()
	      distance = Float()
	      ulRatio = Float()
	      offeredTraffic = Int()

Next, an instance with the same name as in the ``config.py`` is created::

      params = Set()

Then, the parameters in ``params`` can be populated with different
values. Each time the ``write()`` member function (inherited from the
class ``Parameters``) is called, the current values are fixed and
represend one simulation::

	  params.simTime = 5.0
	  params.distance = 25.0
	  params.ulRatio = 0.0

	  for i in xrange(1, 11):
	      params.offeredTraffic = i * 1000000
	      params.write()

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
the appropriate user the campaign with the choosen name.

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

*******************
Experiements Part 1
*******************

#. Find the saturation throughput by editing the
   ``campaignConfiguration.py`` and enlarging the offered traffic
   until a point where the traffic cannot be carried completely. It is
   not neccessary to delete existing scenarios, ``simcontrol.py`` will
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


*****************************************
Efficient Search for the Saturation Point
*****************************************

With the help of the database, the search for the saturation point can
be done in a much more efficient way than be selecting "random" values
for the offered traffic and simulating until the point is found. A
typicall offered traffic vs. throughput curve will allways be a
bisector in the beginning, reach the saturation point and then,
depending on the type of system under simulation, flatten out or fall
down. Therefore, this saturation point can be found efficiently using
binary search: Starting with a small offered traffic as initial value,
simulations are run sequentially, doubling the offered traffic every
time.

If the throughput is less than the offered traffic, the upper bound is
found, and the binary search continues with the mean value of the
upper- and the lower bound. This procedure continues until the upper-
and lower bound have converged.

As this search for the saturation throughput is needed frequientally,
it is directly encapsulated into the parameter generation process as
described in the previous experiment.

We now have to distinguish between two types of parameters:

Scenario parameters
   Parameters to distinguish different scenario
   aspects, e.g. distance between two nodes

Input parameter
   The input to which the saturation point of the
   function f(input) = output shall be found.

In the following, the file ``campaignConfiguration.py`` is changed to
implement the binary search. A sample implementation can be found in
the directory
``openWNS/tests/system/WiFiMAC-Tests--main--1.0/PyConfig/experiment1``

Paramter Class
==============

The parameter class recognizes the scenario parameters by a new
parameter ``parameterRange``; only one parameter (the input parameter)
must be without this parameterRange, but with the default
(i.e. starting value) instead. Hence, the parameter class from the
first experiment would look like the following:

.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment1.db.campaignConfiguration.Set
   :language: python

Database Access
===============

The next step is to define a function that returns the output value -
the throughput in our case. To be compatible, this function must have
a defined signature and return value:

.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment1.db.campaignConfiguration.GetTotalThroughput
   :language: python

This function works in the following way: As input, it gets

paramsString
  A string containing an SQL-ready enumeration of the parameters which define a specific scenario

inputName
  The name of the input variable in the database

cursor
  A cursor object to access the database

This input is used to start two queries: The first one gets a list of
3-tuples, containing the scenario-id, the value of the input name and
the mean value of the moment probe with the name
``ip.endToEnd.window.incoming.bitThroughput_Moments``. The inner
``SELECT`` - statement is only used to find the correct scenario-id,
using the ``paramsString``.

Similarly, the second query gets the same 3-tuple, but with the mean
value of the probe
``ip.endToEnd.window.aggregated.bitThroughput_Moments``. The remaining
lines go through both lists (at the same time using the ``zip``
command), compare the scenario-id and the value of the input parameter
and append another 3-tuple, consisting of the scenario-id, the input
value and the sum of the incoming and aggregated traffic - which
should be the same as the input value in our case.

Accessing the Cursor
====================

With the following lines, the cursor from the appropriate database
belonging to the simulation campaign is fetched:

.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment1.db.campaignConfiguration.Cursor
   :language: python

Starting the Binary Search
==========================

Finally, one round of the binary search (i.e. for every combination of
the scenario parameter values, given in as the ``parameterRange``),
can be started by creating an instance of the class ``Set`` and using
the new member function ``binarySearch``:

.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment1.db.campaignConfiguration.StartBinarySearch
   :language: python

To create the instance ``params``, new parameters are required, namely
the name of the input variable, the cursor, the campaign id and a
pointer to the function that retrieves the input and the output
variable from the database for a given scenario.

The binary search requires as parameters the maximum error (how much
deviation of the output from the input is allowed to still count as
match) and the exactness which must be undercut to stop the search. As
result, it returns the number of new/waiting/finished scenarios,
together with the results if any finished scenarios exist.

The last lines automatically create new scenarios and execute them, if
new scenarios have been created:

.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment1.db.campaignConfiguration.CreateNew
   :language: python

Using Simcontrol.py for the Binary Search
=========================================

When called, the current ``campaignConfiguration.py`` executes one
step of the binary search, for every combination of simulation
parameter settings. Again, the execution is done by ``simcontrol.py``
when populating the database with new scenarios:

.. code-block:: bash

   ./simcontrol.py --create-database

Without deleting the previous results of the experiment, the binary
search will use the existing scenarios and continue the binary search
at the most suitable point.

The execution of several rounds can be automated by the parameter
``--intervall=TIME``: It causes the simcontrol.py repeat the creation
of new scenarios. If the simulations are executed locally, the
parameter ``TIME`` can be set to 1 (second). In this way, the
saturation point can be evaluated automatically up to a predefined
exactness.

*******************
Experiements Part 2
*******************

#. How does the saturation point change under different distances between the AP and the STA?


























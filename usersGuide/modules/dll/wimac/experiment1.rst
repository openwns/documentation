###########################################
Experiment 1: Saturation Throughput
###########################################

In the first experiment, we will setup a very simple simulation campaign, run the
simulations and evaluate the results.

In the following, we will assume that ``myFirstCampaign`` is the root directory 
of the simulation campaign, created as described in the previous section, and 
``myFirstCampaign/experiment1`` is the directory where the simulations are stored.

In the beginning, this directory contains only the following files:

.. code-block:: bash

   $ ls
   campaignConfiguration.py   simcontrol.py

``simcontrol.py`` is used to manage the simulation, i.e. to create the
scenarios, execute the simulations (either locally or in a
distributed grid, if available) and presenting information about the
current status. ``campaignConfiguration.py`` contains the parameters
which shall be simulated.



*****************************************
Experiment 1 - Offered Traffic (part 1)
*****************************************

The first scenario is kept as simple as possible:
One Base Station (BS) and one Mobile Station (MS) transmit data in uplink and downlink,
within a distance d.

1. In this simulation, we would like to measure the saturation throughput
   in downlinnk and uplink. Accordingly, we need to create a
   set of simulations with increasing offered traffic and plot the
   carried throughput versus offered traffic.
   Each simulation campaign, independent of its complexity, follows four
   basic steps:

   a. Create the simulation configuration file, :ref:`experiment1FirstConfig` - 
      this one is the same for all simulations.

   #. Create the parameter file, :ref:`experiment1FirstCampaignConfig` - this one
      contains the parameters that differentiate the simulations from each other, i.e. the different offered traffic in our case.

   #. Run the simulations using :ref:`experiment1FirstSimcontrol`.

   #. View results using the :ref:`experiment1FirstWrowser`.


.. _experiment1FirstConfig:



Config.py
---------

To complete the campaign, a configuration file ``config.py`` is
required that configures the scenario, nodes and the evaluation. For
the first experiment, a config.py can be found in
``myOpenWNS/tests/system/WiMAC-Tests--main--1.2/PyConfig/experiment1/``, this
file needs to be copied into the simulations directory
(``myFirstCampaign/experiment1``):

.. code-block:: bash

   $ cp ../../myOpenWNS/tests/system/WiMAC-Tests--main--1.2/configTutorial/experiment1/config.py .

Take a look at the first lines of the configuration file ``config.py``
and you can see how to adjust the parameters of this scenario:

.. literalinclude:: ../../../../../.createManualsWorkingDir/wimac.tutorial.experiment1.config.simulationParameter
   :language: python

The most important statement is the first one:

.. code-block:: python

   from openwns.wrowser.simdb.SimConfig import params

Here, a parameter class ``params`` is imported. It is required for the
automatic generation of scenarios in the campaign: the object
``params`` contains member variables for every parameter that will be
changed in the campaign. In this case, it is

#. the carrier bandwidth (bandwidth).
#. the distance between the BS and the MS (distance)
#. the offered traffic (traffic)

Besides these parameters, this section also sets the packet size, the packet scheduling strategy, simulation's settling time and five other parametrs.

.. _experiment1FirstCampaignConfig:



campaignConfiguration.py
------------------------

To set different values for the parameters of the simulations, a second file besides the
``config.py`` is neccessary: the ``campaignConfiguration.py``.
For the first experiment, a prepared ``campaignConfiguration.py`` can be found in
``myOpenWNS/tests/system/WiMAC-Tests--main--1.2/configTutorial/experiment1/``, this
file needs to be copied into the simulations directory, overwriting the existing one:

.. code-block:: bash

   $ cp ../../myOpenWNS/tests/system/WiMAC-Tests--main--1.2/configTutorial/experiment1/campaignConfiguration.py .

Two sections in this files are especially interesting for the simulation: First, 
the parameter class ``Set`` is defined that contains all simulation parameters that
are used in ``config.py``:

.. literalinclude:: ../../../../../.createManualsWorkingDir/wimac.tutorial.experiment1.campaignConfiguration.Set
   :language: python

Next, an instance with the same name as in the ``config.py`` is created:

.. literalinclude:: ../../../../../.createManualsWorkingDir/wimac.tutorial.experiment1.campaignConfiguration.params
   :language: python

The class ``Set`` contains the function ``setDefaults()``. Calling this functions,
default values are defined for all parameters.

Then, the parameters in ``params`` can be populated with different values. Each 
time the ``write()`` member function (inherited from the class ``Parameters``) is
called, the current values are fixed and represent one simulation:

.. literalinclude:: ../../../../../.createManualsWorkingDir/wimac.tutorial.experiment1.campaignConfiguration.offeredTraffic
   :language: python

With this setup, 6 simulations are created, differentiated by the
offered downlink traffic between 0.1 and 12.1 Mb/s. This concludes the file 
``campaignConfiguration.py``.

.. _experiment1FirstSimcontrol:



simcontrol.py
-------------

We are now ready to create the simulations and let them run.  As mentioned earlier,
simulation execution is controlled by the script ``simcontrol.py``. With the command

.. code-block:: bash

   $ ./simcontrol.py --create-database

The ``campaignConfiguration.py`` is executed and the parameter values
are written to the database. Then, the command

.. code-block:: bash

  $ ./simcontrol.py --create-scenarios

reads the database and creates a sub-directory for every scenario.
This can be validated by calling

.. code-block:: bash

   $ ./simcontrol.py -i

      id   state        [...]     bandwidth  distance  offeredTraffic
        1  NotQueued                     5     100.0         1000.0
        2  NotQueued                     5     100.0      2501000.0
        3  NotQueued                     5     100.0      5001000.0
        4  NotQueued                     5     100.0      7501000.0
        5  NotQueued                     5     100.0     10001000.0
        6  NotQueued                     5     100.0     12001000.0

Before running all simulations, a single one can be tested (e.g. for typos in 
``config.py``) by changing into one of the new created directories and running

.. code-block:: bash

   $ ./openwns-dbg

If everything works right, the logging output of the simulation is printed 
(consisting of the simulation time, the module, the FU and the output), until the
simulation time reaches 1.1 seconds and the simulation ends with

.. code-block:: bash

   wns::simulator::Application: shutdown complete

After this test, the simulations can be run one-by-one using the ``simcontrol.py`` script:

.. code-block:: bash

   $ ./simcontrol.py --execute-locally --restrict-state=NotQueued
   Executing scenario with id: 1
   Executing scenario with id: 2
   Executing scenario with id: 3
   Executing scenario with id: 4
   Executing scenario with id: 5
   Executing scenario with id: 6


This starts the serial execution of all defined scenarios. In a "production" 
environment, a grid engine could be used to queue all simulations and run them
in parallel; the script is configured to work together with the SunGridEngine_
e.g. with the command instead:

.. code-block:: bash
   $ ./simcontrol.py --execute-scenarios --restrict-state=NotQueued

Optionally, if you use the SunGridEngine_, you can modify the ``simcontrol.py``
in order boost the priority of our simulations by editing the ``estimated cpu time``
from 100 hours to 1h in the following line:

. literalinclude:: ../../../../../.createManualsWorkingDir/wimac.tutorial.experiment1.simcontrol.cpuTime
   :language: python

The installation and configuration of this grid is out of the scope of this tutorial.

.. _SunGridEngine: http://gridengine.sunsource.net/

After some time, all 6 simulations should be finished, which can be controlled again with

.. code-block:: bash

   $ ./simcontrol.py -i

    id    state  [...]  simTime prog   sgeId host bandwidth distance  offeredTraffic  
    1   Finished         1.10s  100.00%                 5     100.0          1000.0
    2   Finished         1.10s  100.00%                 5     100.0       2501000.0 
    3   Finished         1.10s  100.00%                 5     100.0       5001000.0
    4   Finished         1.10s  100.00%                 5     100.0       7501000.0
    5   Finished         1.10s  100.00%                 5     100.0      10001000.0
    6   Finished         1.10s  100.00%                 5     100.0      12501000.0 
    
Each simulation directory now contains a directory ``output``, where all probe 
output is stored in text files. Additionally, the output is stored in the 
database, which can be accessed much more user-friendly than viewing text files.

.. _experiment1FirstWrowser:



Wrowser
-------

The Wrowser ("Wireless network simulator Result brOWSER") is the openWNS graphical
user interface to browse, i.e. plot, simulation results in a fast and convenient 
way. We assume that the Wrowser is installed according to :ref:`gettingStartedWrowser`.
Thus, the Wrowser is started by calling

.. code-block:: bash

   $ ~/wrowser/bin/wrowser

In the menu File are the different options to read the generated simulation data,
we select ``Open Campaign Database`` and then under the appropriate user the 
campaign with the chosen name, see :ref:`figure-wimac-experiment1-wrowser-selectCampaign`.

.. _figure-wimac-experiment1-wrowser-selectCampaign:

.. figure:: images/experiment1-wrowser-selectCampaign.*
   :align: center

   Campaign selection

After reading in the simulation parameters from the database, the
Wrowser will display all possible parameter combinations, see
:ref:`figure-wifimac-experiment1-wrowser-parameter`.

.. _figure-wimac-experiment1-wrowser-parameter:

.. figure:: images/experiment1-wrowser-parameter.*
   :align: center

   Parameter selection

We do not want to deselect any of the simulations, but draw the graph of the offered
traffic versus the obtained throughput measured by the top MAC-Layer. Thus, the 
Wrowser needs to get, for all six simulations, the throughput, combine it with 
the offered traffic parameter and draw this to a graph. This type of combination
plot is named "Parameter Plot" in the Wrowser. We select Figure -> New -> Parameter.
In the new window, the simulation parameter has to be set to ``offeredTraffic``,
this will be displayed in the x-axis. For the y-axis, we select ``wimac.top.window.aggregated.bitThroughput_BS_Moments``
[#]_ and select ``Draw`` in the bottom to see a figure as in :ref:`figure-wimac-experiment1-wrowser-throughput`.

.. rubric:: Footnotes

.. [#] The aggregated bit throughput probe shows the aggregated traffic which
       has left the BS and has reached its final destination.


.. _figure-wimac-experiment1-wrowser-throughput:

.. figure:: images/experiment1-wrowser-throughput.*
   :align: center

   Throughput plot

In the new figure, we should see that the traffic has reached the saturation point at 7.5 Mb/s.

Another interesting figure is the relation of offered traffic versus the packet 
delay, evaluated as a probability function. This can be done by choosing a 
``PDF/CDF/CCDF`` graph in the ``Figure`` menu and plotting the probe `` 
wimac.top.packet.incoming.delay_BS_Id1_PDF. 

The Packet Delay is only meaningful in underload, because the infinite delay of 
lost or droped packets in overload is not considered in this metric. From the 
previous figure we can derive the saturation throughput of 7.5 Mb/s. Therefore 
we deselect the last two simulations with a  ``offeredTraffic`` beyond 7.5Mb/s. 
In the ``Configure Graph`` menu which called with the botton next to ''Draw'' 
button, we select the ``Line markers`` as ``None``

:ref:`figure-wimac-experiment1-wrowser-configureGraph_b`.

.. _figure-wimac-experiment1-wrowser-configureGraph_b:

.. figure:: images/experiment1-wrowser-configureGraph_b.*
   :align: center

   configure graph


we can see that the probability for a higher delay increases as the offered traffic increases, see 


:ref:`figure-wimac-experiment1-wrowser-delay`.

.. _figure-wimac-experiment1-wrowser-uplink-delay:

.. figure:: images/experiment1-wrowser-uplink-delay.*
   :align: center

   Delay plot



*******
Details
*******

So far, we have just used the prepared ``config.py``, without the knowledge how
it generates the simulation scenario. In the following sections, we will go step
by step through the different parts of the ``config.py`` and learn what is neccessary
to setup the scenario and how the WiMAC modul can be parameterized.



Simulation Parameters
---------------------

The file ``config.py`` for this scenario begins with the simulation
parameters to allow for a better overview and an easy change of
parameters.

.. literalinclude:: ../../../../../.createManualsWorkingDir/wimac.tutorial.experiment1.config.simulationParameter
   :language: python

The statement ``from openwns.wrowser.simdb.SimConfig import params`` is required for the
automatic generation of scenarios in the campaign: the object
``params`` contains member variables for every parameter that will be
changed in the campaign. In this case, it is

#. the carrier bandwidth (bandwidth).
#. the distance between the BS and the MS (distance),
#. the offered traffic (traffic) and

Besides these parameters, this section also sets the packet size, the packet scheduling
strategy, simulation's settling time and five other parametrs.



Import Statements
-----------------

Then the Python code that generates the scenario starts. First, several modules are imported:

.. literalinclude:: ../../../../../.createManualsWorkingDir/wimac.tutorial.experiment1.config.imports
   :language: python

Namely, we import

* The random number generator

* The simulator core ``openwns``, which inlcudes e.g. classes to define dB, dBm 
  and an interval.

* The scenario package to define the radio environment.

* A virtual DHCP, ARP and DNS server for the IP-Layer.

* From wimac:

  - The support package that allows the generation of stations and transceivers 
    for the stations.
  - The pathselection package (used for IMT-Advanced scenarios, but required in 
    all scenarios as every BS registers itself and its associated MSs) (within 
    helpers.py)
  - The traffic load (within helpers.py)
  - The evaluation structure for the wimac



WNS Core Configuration
----------------------

The next section creates one instance of the openWNS:

.. literalinclude:: ../../../../../.createManualsWorkingDir/wimac.tutorial.experiment1.config.WNS
   :language: python

The output strategy ``delete`` assures that old simulation output is
deleted prior to the simulation. The write interval of the
status-report and the probes is set.



Scenario
--------

The scenario building basically consist of the following definitions

* the positions of stations
* the transceivers
* the protocol stacks of the MAC

After passing the default configuartion parametersOFDMA to the wimac module, the
creation of the scenario instance is done by using the scenario and wimac module;

.. literalinclude:: ../../../../../.createManualsWorkingDir/wimac.tutorial.experiment1.config.scenario
   :language: python

The positions of the stations can be defined busing the placers which garantue a 
specific distribution of the positions. Here, the positions of the BSs comply a 
hexagonal grid with the chosen number of rings ``numberOfCircles`` around a center
cell. All positions of the MSs are on a line according to the position list 
``positionList``. Because we only study a scenario with one BS and one MS we chose
``numberOfCircles`` and ``numberOfNodes`` equal to one. The different types of placers
can be chosen from the pytho classes in the path ``myOpenWNS/framework/scenarios/PyConfig/scenarios/placer/``

Next, the antenna type of the BS is defined with a position offset relative to the
BS positions. This is required because more than one antenna per BS is possible. 
Here we only have one antenna per BS with a hight of 5 meters.

The protocoll stack of the stations is defined by the creator. In this file,
the creator ``WiMAXBSCreator`` and ``WiMAXUECreator`` are used, which can be found
in the folder ``myOpenWNS/modules/dll/WiMAC--main--1.0/PyConfig/wimac/support/``

The scenario is build by the ``scenarios.builders.CreatorPlacerBuilder`` using the
above mentioned parameters and functions.



Radio Channel
-------------

The configuration of the radio channel propagation parameters contains modules for three major effects:

* Pathloss,
* Shadowing and
* Fast fading

.. literalinclude:: ../../../../../.createManualsWorkingDir/wimac.tutorial.experiment1.config.radioChannel
   :language: python

Line-of-Side Test (LoS_Test) radio channel is chosen. More details about how the
radio channel can be configured can be found in the file ``wimac.support.helper.py``.



Evaluation
----------

In the final lines, the evaluation is installed, creating probe output
for the WiMAC station types BSs and MSs with a certain window and settling time:

.. literalinclude:: ../../../../../.createManualsWorkingDir/wimac.tutorial.experiment1.config.Probing
   :language: python



************************************* 
Experiment 1 - Bandwidth (part 2) 
************************************* 

2. Find the impact of increased ``bandwidth`` from 5MHz to 10 and 20 MHz on the 
   saturation throughputs by editing the ``campaignConfiguration.py`` and ``config.py``.

   a. Change the static setting in ``config.py`` to a variable parameter that gets
      its value from the imported instance ``params``.

   #. Add the parameter ``bandwidth`` to the class ``Set`` in the ``campaignConfiguration.py``.
      As existing simulations do not have this parameter, but have used 5MHz, we
      add this as the default value by specifying::

        bandwidth= Int(default=5)

   #. Add an outer for-loop to the existing one to vary the bandwidth between 5 and 20 MHz::

        for rate in [0,10,15,30,35]:
           for params.bandwidth in [5,10,20]:
             params.offeredTraffic = (0.001 + rate) * 1e6
             params.write()
   
   #. It is not necessary to delete existing scenarios, ``simcontrol.py`` will
      automatically identify the missing simulations and create them when told so.
      Everytime you modify the campaign parameters, first call ``simcontrol.py --create-database``
      to add entries to the database and ``simcontrol.py --create-scenarios`` to
      create the simulation directories accordingly. Create the simulations (in 
      the database and the scenarios) and execute them.

   #. Evaluate the impact of the bandwidth on the saturation point using the Wrowser.




***********************************
Experiment 1 - Distance (part 3)
***********************************

3. Now, we want to vary another parameter ``distance'' to select a
   distance between BS and MS of 100m to 12km.

   a. Change the static setting in ``config.py`` to a variable parameter that gets its value from the imported instance ``params``.

   #. Add the parameter ``distance`` to the class ``Set`` in the
      ``campaignConfiguration.py``. As existing simulations do not
      have this parameter, but have used 100m, we add this as the default value by specifying::

         distance= Int(default=100)

   #. Add an outer for-loop to the existing one to vary the distance between 100m and 12000 m::

      	 for params.packetSize in [1480*8, 80*8]:
	     for i in xrange(1, 21):
    	     	 params.offeredTraffic = i * 1000000
  		 params.write()

   #. Create the simulations (in the database and the scenarios) and execute them.

   #. Evaluate the impact of the frame size on the saturation point using the Wrowser.



























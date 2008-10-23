#######################################################
Experiment 2: Efficient Search for the Saturation Point
#######################################################

.. note::

   Experiment 2 re-uses the campaign (and also existing simulations)
   from experiment 1; Especially, the same ``config.py`` is
   used. Therefore, we recommend to continue the experiment in the
   directory ``myFirstCampaign/Experiment1``, and not to create a new
   sub-campaign using ``./playground.py preparecampaign PATH``.

With the help of the database, the search for the saturation point can
be done in a much more efficient way than be selecting "random" values
for the offered traffic and simulating until the point is found. A
typical offered traffic vs. throughput curve will always be a
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

As this search for the saturation throughput is needed often,
it is directly encapsulated into the parameter generation process as
described in the previous experiment.

We now have to distinguish between two types of parameters:

Scenario parameters
   Parameters to distinguish different scenario
   aspects, e.g. distance between two nodes

Input parameter
   The input to which the saturation point of the
   function f(input) = output shall be found.

In the following, the existing file ``campaignConfiguration.py`` is
changed to implement the binary search. An example implementation can be
found in the directory
``openWNS/tests/system/WiFiMAC-Tests--main--1.0/PyConfig/experiment2``

Parameter Class
===============

The parameter class recognises the scenario parameters by a new
parameter ``parameterRange``; only one parameter (the input parameter)
must be without this parameterRange, but with the default
(i.e. starting value) instead. Hence, the parameter class from the
first experiment would look like the following:

.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment2.db.campaignConfiguration.Set
   :language: python

Database Access
===============

The next step is to define a function that returns the output value -
the throughput in our case. To be compatible, this function must have
a defined signature and return value:

.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment2.db.campaignConfiguration.GetTotalThroughput
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

.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment2.db.campaignConfiguration.Cursor
   :language: python

Starting the Binary Search
==========================

Finally, one round of the binary search (i.e. for every combination of
the scenario parameter values, given in as the ``parameterRange``),
can be started by creating an instance of the class ``Set`` and using
the new member function ``binarySearch``:

.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment2.db.campaignConfiguration.StartBinarySearch
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

.. literalinclude:: ../../../../../.createManualsWorkingDir/wifimac.tutorial.experiment2.db.campaignConfiguration.CreateNew
   :language: python

Using simcontrol.py for the Binary Search
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

************
Experiments
************

#. Calculate (roughly) the maximum distance for which a reception is possible using

   #. The pathloss function from the ``config.py`` in experiment 1.

   #. A background noise N = -95dBm

   #. A minimum Signal to Noise Radio (SNR) of 6 dB.

#. How does the saturation point change when varying the distances
   between the AP and the STA?

#. Validate the calculation by simulating distances near to the
   calculated maximum distance (e.g. +- 10m).


























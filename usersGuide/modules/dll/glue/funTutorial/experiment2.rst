##########################
Experiment 2: The ALOHA FU
##########################

In experiment 1 we have seen that the system suffers from significant
throughput degradation in heavy load situations. With higher load, the
system is not even able to carry the saturation throughput. The reason
for this behavior are collisions on the medium. In a case of a
collision, the compound can not be received correctly.

To solve the issue, we include a ALOHA functional unit. The ALOHA
functional unit retransmits the compound in case of a collision after
a delay that is chosen according to a given random distribution.

.. _figure-funtutorial-experiment2-fun:

.. figure:: images/experiment2.*
   :align: center

   FUN setup

The functional unit network configuration is as follows:

.. literalinclude:: ../../../../../../.createManualsWorkingDir/glue.fun.tutorial.experiment2
   :language: python

-----
Tasks
-----

 1. Copy the configuration file from the glue tutorial directory to
    your campaign simulation directory.
 2. Execute the simulations.


The result shows, that the ALOHA functional unit avoids the throughput
degradation in overload situations.

.. _figure-funtutorial-experiment2-results-throughput-clients:

.. figure:: images/experiment2_throughput_clients.*
   :align: center

   Aggregated throughput of the clients vs. load


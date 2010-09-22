##########################
Experiment 2: The ALOHA FU
##########################

.. _figure-funtutorial-experiment2-fun:

.. figure:: images/experiment2.*
   :align: center

*****
Aloha
*****

* **Module**

  * ``glue.mac.Aloha``

* **Usage** 

  * Constructor: ``Aloha(commandName)``
  * ``commandName`` : Name of the Aloha command 
  * waits a random time between zero and the configured maximum waiting time before the medium is accessed 

* **Parameter**

  * ``maximumWaitingTime`` (default ``0.01``)

    * maximum waiting time in seconds.

  * ``parentLogger`` (default ``None``)

*********
FUN setup
*********

.. literalinclude:: ../../../../../../.createManualsWorkingDir/glue.fun.tutorial.experiment2
   :language: python

.. _figure-funtutorial-experiment2-results-throughput-clients:

.. figure:: images/experiment2_throughput_clients.*
   :align: center
   :width: 480px 

   Aggregated throughput of the clients vs. load


#################################
Experiment 2 : Packet Scheduling
#################################

In this experiment we extend the previous deployment by one additional MS. In 
the single cell scenario with one BS and two MS we will study the impact of 
different scheduling strategies on the throughtput and fairness.

In Wireless Metropolitan Area Network (WMAN) systems a central scheduler allocates
resources (such as time, frequency, or transmit power) to MSs within a cell and 
forwards its scheduling decisions within a MAP-message every frame. Additionally
data packets are selected by the scheduler which are being transmitted on the 
allocated resources. 

The scheduler frame work within the openWNS allows to orthogonalize the 
scheduling of the different dimensions and thereby to independently choose
different strategies for each resource allocation (such as dynamic subchannel assignment (DSA),
adaptive modulation and coding (AMC), adaptive power control (APC)) and the packet 
scheduling. 

For more details on the scheduling process within the ``WIMAC`` and ``openWNS`` 
please refer to NewSchedulerManual_.

.. _NewSchedulerManual: http://openwns.comnets.rwth-aachen.de/Wiki/NewSchedulerManual


In this experiment we study the impact of different strategies for the 
packet scheduling on the throughtput and fairness as well as briefly examine the
effect of different strategies for DSA on the frame occupation. During the DSA 
transmission oppertunities are defined in time and frequency and are dedicated 
to MSs.



************
Preparation
************


:Add new Probe:
  In order to differentiate and to gather data rate from different links we add 
  a third Probe "aggregated.bitThroughput" to the ``TutorialEvaluation``. By 
  uncommenting the corresponding line ``wimac.top.window.aggregated.bitThroughput``
  in the in the file ``default.py`` which is in the folder 
  ``myOpenWNS/modules/dll/WiMAC--main--1.0/PyConfig/wimac/evaluation/``:

  .. literalinclude:: ../../../../../.createManualsWorkingDir/wimac.tutorial.experiment2.evaluating.tutorialEvaluation
     :language: python


:Update campaign:
  Using ``./playground.py preparecampaign PATH`` with the same ``PATH``
  as in the preparation for experiment 1 (namely ``../myWiMACCampaign`` according
  to the chapter "Preparations" ), we can update the sandbox and apply the made 
  changes to the probing. When prompted by ``./playground.py``, please select 
  ``(U)pdate the sandbox``


:Create sub-campaign:
  Using ``./playground.py preparecampaign PATH`` with the same ``PATH``, we can 
  create a sub-campaign that uses the same sandbox, but a differed directory to 
  store the simulations. When prompted by ``./playground.py``, please select 
  ``(C)reate a sub-campaign`` and choose as name e.g. ``Experiment2``.


:Configuration files:
  Rerquired configuration files ``config.py`` and ``campaignConfig.py`` can be 
  found in ``myOpenWNS/tests/system/WiMAC-Tests--main--1.2/PyConfig/experiment2/``,
  this file needs to be copied into the simulations directory 
  (``myWiMACCampaign/experiment2``), e.g,:

   .. code-block:: bash

     $ cp ../../myOpenWNS/tests/system/WiMAC-Tests--main--1.2/configTutorial/experiment2/config.py .


:Second MS:
  The second MS is also placed by the ``LinearPlacer`` by the following line in 
  the ``config.py``:

  .. literalinclude:: ../../../../../.createManualsWorkingDir/wimac.tutorial.experiment2.config.scenario
     :language: python

  creating two MS on a line at 100m and 3000m from the BS.


:Change probing type:
  As we do not need the distribution of of our metrics anymore, we secondly change
  our Probing type from ``PDF`` to ``Moments`` in the follwing line in the ``config.py`` :

   .. literalinclude:: ../../../../../.createManualsWorkingDir/wimac.tutorial.experiment2.config.probing
      :language: python


*******************************************************
Experiment 2 - packet scheduling strategies (part 1) 
*******************************************************

We will again increase the offered traffic with varying schedling types namely 
``RoundRobin``, ``Proportional Fair``, ``Exhaustive Round Robin``, and 
``Fixed Resources``.

   #. Create the simulations (in the database and the scenarios) and execute them.

   #. Evaluate the impact of the strategy on the cell throughput as well as on 
      the idividual throughput using the Wrowser.Exemplarily you can evalute the
      downlink throughputs graphs of both users for each scheduler configuration.
      
   #. Which strategy is fair? And in what terms (e.g. resources or data rate) ?



*******************************************************
Experiment 2 - packet scheduling strategies (part 2) 
*******************************************************

In the second part we like to examine the impact of the DSA strategy on the frame
occupation. The scheduling strategies ``fixed`` and ``round robin`` may yield similar 
throughput results but they use different DSA strategies, namly ``linear first`` 
and ``fixed``.
      
   #. Recording the frame occupation can be activeted by uncommending the 
      following line at the end of the ``config.py``:
       
            .. wimac.evaluation.default.installJSONScheduleEvaluation(WNS, loggingStationIDs)
                :language: python
      
   #. In order to evaluate the differences of the DSA- strategies we will study 
      the frame occupation in a middle load situtation at 3Mbps for the scheduling 
      ``round robin`` and ``fixed``. You can get the corresponding simmulation 
      ``ID`` (and folder name) by the command ``./simcontrol -i``. The WiMAC 
      simulator is configured in a manner that the frame occupation can only be 
      probed in the debug (dbg) mode. This folders have to be removed:
        
        .. code-block:: bash

            $ rm -rf  ../myWiMACCampaign/experiment2/ID
        
        and recreated in a manner that the two simualtions run in the ``dbg`` mode:
        
        .. code-block:: bash

           $ ./simcontrol --create-scenario --flavor=dbg
   
   #. Reque the two simulations
   
   #. Watch the resulting frame occupation of this two simulations by using the 
      Wroser according to the CouchDB_.
        
     .. _CouchDB: http://docs.openwns.org/UsersGuide/CouchDB.html
   
   #  How does the resource assignement differ? 


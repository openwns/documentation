#################################
Experiment 2 : Packet Scheduling
#################################

.. sectionauthor:: Benedikt Wolz <bmw@comnets.rwth-aachen.de>, Department of Communication Networks (ComNets), RWTH Aachen University

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

     $ cp ../../myOpenWNS/tests/system/WiMAC-Tests--main--1.2/PyConfig/experiment2/config.py .


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
      
*******************
Static Factory
*******************
In previous tutorials we modified values of parameters in the PyConfig but the 
protocol stack of the simulated communication systems and the c++ programm were 
left unchanged. Now we will change the protocoll stack and the c++ program by means 
of the ``StaticFactory``. 

Within a given context, a number of different strategies to accomplish a task may
exist. Depending on the situation (here configuration), one of those strategies 
should be chosen. To make strategy selection configurable, the strategies are 
encapsulated in classes. These classes share an abstract strategy interface 
accessed by the context. The strategy can then be replaced without modification 
of the context. 
An example for the use of the strategy pattern is the ``Dropping buffer``.
The ``Dropping buffer`` can be configured to use one of two dropping strategies: ``Front``
and ``Tail``. Internally, those names are used to create instances of dropping strategy
classes. Those strategy classes encapsulate the selection of candidates to drop.

All these instances are created by the ``StaticFactory`` which provides an easy to 
use interface for creating instances. Strategies register at a ``StaticFactory``
in a decentralized manner by utilizing static, namespace-level objects. Before
the main function starts execution, all strategies have already been registered 
at the ``StaticFactory``. If shared objects containing strategies are dynamically
loaded, all strategies defined within the shared object get registered during 
shared object initialization. There is no central point of strategy registration.

Every "StaticFactory" is parameterized by a creator, which itself is configured by
the strategy TYPE (the abstract strategy interface) and the concrete 
implementation KIND and enforces a strategy constructor signature. Every specific 
strategy registers at the ``StaticFactory`` using its abstract strategy interface
and the creator suiting the abstract strategy constructor signature. The 
possibilities offered by PyConfig and "StaticFactory" allow an easy configuration 
at all three levels(???) of configurability.

Let's see at the example of packet schedulinghow the ``StaticFactory`` is used.
. The packet scheduling can be configured to use one of the strategies: 
``RoundRobin``, ``Proportional Fair``, ``Exhaustive Round Robin``, and 
``Fixed Resources``. Internally, those names are used to create instances of 
the classes of packet scheduling strategy which encapsulate the type of selection 
of packets to schedule.

According to the string in the parameter ``Config.scheduler`` being set in the 
``config.py`` the function 
``wimac.support.helper.setupScheduler(WNS, Config.scheduler)`` in the file 
``myOpenWNS/modules/dll/WiMAC--main--1.0/PyConfig/wimac/support/helper.py`` 
first selects the specific type of scheduler in terms of DSA- and packet 
scheduling strategy and second instantiates them in a loop for each BS: 

    .. literalinclude:: ../../../../../.createManualsWorkingDir/wimac.tutorial.experiment2.staticFactory.substrategy.ProportionalFair.helper.py
       :language: python

For instance for a chosen string ``PropFair`` the packet scheduling strategy 
``ProportionalFair`` and a DSA strategy ``LinearFFirst`` are selected . In this 
manner working combinations of the two strategy types are suggested and can be 
easily configured. By using ``setupSchedulerDetail()`` instead of 
``setupScheduler()`` the strategy for packet scheduling and DSA can be chosen 
idependently which is used in the second part of the experiment in order to vary
the DSA strategy only.

A class is registered at the StaticFactors by a name which is used used twice 
in the code. Once in the python file and once in the c++ code. 
The ``subStrategy`` (TYPE) (or strategy for packet scheduling) of 
``ProportionalFair`` (KIND) is registered once in the python file 
``/myOpenWNS/framework/libwns--main--1.0/PyConfig/openwns/Scheduler.py`` with 
the keyword ``__plugin__``:

  .. literalinclude:: ../../../../../.createManualsWorkingDir/wimac.tutorial.experiment2.staticFactory.substrategy.ProportionalFair.openwns.Scheduler.py
     :language: python

and once at the begining of the c++ file ``/myOpenWNS/framework/libwns--main--1.0/src/scheduler/strategy/staticpriority/ProportionalFair.cpp`` 
refering to the ``SubStrategyInterface``:

  .. literalinclude:: ../../../../../.createManualsWorkingDir/wimac.tutorial.experiment2.staticFactory.substrategy.ProportionalFair.cpp
     :language: c++


*******************************************************
Experiment 2 - packet scheduling strategies (part 1) 
*******************************************************

1. We will again increase the offered traffic with varying schedling types namely 
   ``RoundRobin``, ``Proportional Fair``, ``Exhaustive Round Robin``, and 
   ``Fixed Resources``.

   a. Create the simulations (in the database and the scenarios) and execute them.

   #. Evaluate the impact of the strategy on the cell throughput as well as on 
      the idividual throughput using the Wrowser.Exemplarily you can evalute the
      downlink throughputs graphs of both users for each scheduler configuration.
      
   #. Which strategy is fair? And in what terms (e.g. resources or data rate) ?



*******************************************************
Experiment 2 - dynamic subchannel assignment (part 2) 
*******************************************************

2. In the second part we like to examine the impact of the DSA strategy on the frame
   occupation. The scheduling strategies ``fixed`` and ``round robin`` may yield similar 
   throughput results but they use different DSA strategies, namly ``linear first`` 
   and ``fixed``.
      
   a. Recording the frame occupation can be activeted by uncommending the 
      following line at the end of the ``config.py``:
       
            ``wimac.evaluation.default.installJSONScheduleEvaluation(WNS, loggingStationIDs)``
      
   #. In order to evaluate the differences of the DSA- strategies we will study 
      the frame occupation in a middle load situtation at 3.8 Mbps for the scheduling 
      ``round robin`` and ``fixed``. You can get the corresponding simmulation 
      ``SCENARIOID`` (and folder name) by the command ``./simcontrol -i``. The WiMAC 
      simulator is configured in a manner that the frame occupation can only be 
      probed in the debug (dbg) mode. This folders have to be removed:
        
        .. code-block:: bash

            $ rm -rf  ../myWiMACCampaign/experiment2/SCENARIOID
        
      and recreated in a manner that the two simualtions run in the ``dbg`` mode:
        
        .. code-block:: bash

           $ ./simcontrol --create-scenario --flavor=dbg
   
   #. Reque the two simulations (e.g.: by ``./simcontrol.py --queue-single-scenario=SCENARIOID``)
   
   #. Watch the resulting frame occupation of this two simulations by using the 
      Wroser according to the CouchDB_.
        
        .. _CouchDB: http://docs.openwns.org/UsersGuide/CouchDB.html
   
   #.  How does the resource assignement differ? 


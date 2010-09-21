#################################
Experiment 2 : Cell Spectral Efficiency Calibration
#################################

In this experiment you learn how to setup the openWNS LTE module to comply to the baseline IMT-Advanced calibration scenario as agreed by the 3GPP. The motivation behind this base line scenario is to agree on default values for LTE functionalities not fully described by the standard. This mainly applies to the many degrees of freedom in the scheduler. 

*******************************
Uplink Power Control
*******************************

The more power a station emits the more interference it will cause to other cells. At the same time more transmission power increases the received signal power in the own cell and therefore the SINR. The LTE module implements the open-loop fractional pathloss compensation power control behaviour as specified by [3GPP36.213]_
The formula used by user terminals to calculate its transmission power in uplink direction is

.. math:: P_{TX} = P_0 + \alpha PL

where both the base level :math:`P_0` and the fractional path-loss compensation factor :math:`\alpha` are broadcasted by the eNB. User terminals measure the path-loss :math:`PL` to the serving cell utilizing the downlink reference signals and a proper time-averaging function to determine the transmission power. 

The dynamic offset mechanisms as specified in [3GPP36.213]_ are not implemented.

.. [3GPP36.213] 3GPP Technical Specification 36.213, 'Evolved Universal Tertestial Radio Access (E-UTRA); Physical Layer Procedures (Release 8)', www.3gpp.org

*******************************
Downlink Subchannel Assignement
*******************************

Use ``Exhaustive Round Robin`` with any DSA strategy.

*******************************
Uplink Subchannel Assignement
*******************************

Use ``DSA Driven Round Robin`` with ``Fixed`` DSA strategy.

Use CouchDB channel trace to verify resource assignement

*******************************
Small scale fading
*******************************

Describe ``FTFading`` setup.

*******************************
Scenario Setup
*******************************

Scenario viewer should already be known. Describe ``channelModelCreator`` and random seed setup for multiple drops.

*******************************
Using the openWNS Wrowser API
*******************************

.. figure:: images/getCampaign.*
   :align: center

.. code-block:: python

   bash # python
   Python 2.6.5 (r265:79063, Apr 16 2010, 13:09:56) 
   [GCC 4.4.3] on linux2
   Type "help", "copyright", "credits" or "license" for more information.
   >>> import openwns.wrowser.simdb.api as api
   >>> c = api.getCampaignByTitle("lteR8RC1Calib")
   >>> c
   <openwns.wrowser.simdb.api.campaigns.Campaign instance at 0xb759344c>
   >>> dir(c)
   ['__doc__', '__init__', '__module__', 'authorized', 'campaignID', 'dbSize', 'description', 'title']
   >>> c.dbSize
   '8336 kB'

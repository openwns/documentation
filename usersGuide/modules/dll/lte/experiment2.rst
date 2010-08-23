#################################
Experiment 2 : Cell Spectral Efficiency Calibration
#################################

In this experiment you learn how to setup the openWNS LTE module to comply to the baseline IMT-Advanced calibration scenario as agreed by the 3GPP. The motivation behind this base line scenario is to agree on default values for LTE functionalities not fully described by the standard. This mainly applies to the many degrees of freedom in the scheduler. 

*******************************
Uplink Power Control
*******************************

The more power a base station (BS) emits the more interference it will cause to other cells. At the same time more transmission power increases the received signal power in the own cell and therefore the SINR. The formula used to calculate the transmitted power of a user terminal (UT) in uplink is

.. math:: P_{TX} = P_0 + \alpha PL

where :math:`P_0` and :math:`\alpha`

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
#######################################
Experiment 3 : Cell Spectral Efficiency
#######################################


Cellular scenario.

Gezeigt wird der Einfluss verschiedener DSA-strategien auf die Varianz
der Interferenz, die Rahmenbelegung und die „Cell Spectral
Efficiency“.  Auswirkung der Cluster Order und Sectorisierung auf das
SINR und die „cell spectral efficiency“.  Prozess der
Interferenzschätzung soll erläutert werden. Scenario Viewer und
Interferenz Cache (kks) werden vorgestellt.



Interference Cache
==================

The Scheduler of the sending station must have a rough estimation of
the interference level at the receiver to choose the appropriate
modulation and coding scheme. The measured SINR at the receiver
indicated by the PHY are stored in the *Interference Cache*
which are averaged by:

.. math::
  \hat{\mu}_{\gamma}[k] = \left\{ \begin{array}{c@{\quad}l}
      \gamma[0] & k=0 \\
      (1-\alpha_{avg})\hat{\mu}_{\gamma}[k-1]+\alpha_{avg}\gamma[k] & k>1
    \end{array} \right.

The measured values for SINR are directly stored at the
Interference Cache of the sender. The transmission of the measured
values to the sender is not simulated.

.. code-block:: cpp

  void storeCarrier( wns::node::Node* node, 
      const wns::Power& carrier, ValueOrigin origin);

  void storeInterference( wns::node::Node* node, 
      const wns::Power& interference, ValueOrigin origin);
  
  wns::Power 
  getAveragedCarrier( wns::node::Node* node ) const;
  
  wns::Power 
  getAveragedInterference( wns::node::Node* node ) const;
  
  wns::Power 
  getCarrierDeviation( wns::node::Node* node ) const;
  
  wns::Power 
  getInterferenceDeviation( wns::node::Node* node ) const;


The interference cache offers the interface shown in above. The
methods ``storeCarrier(...)`` and ``storeInterference(...)`` provide
write access to the interference cache while the other methods provide
read access. When adding measured values to the interference cache, it
is necessary to provide an origin indicator that indicates if the
access to the interference cache comes from a remote station or from a
local measurement. This gives the opportunity to average measured
values with different :math:`\alpha` values.
 


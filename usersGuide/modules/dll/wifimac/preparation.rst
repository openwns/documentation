===========
Preparation
===========

In the following, it is assumed that the openWNS source code is
situated in the directory ``myOpenWNS``.

Make sure that the following points are met within your openWNS
installation:

* Running ``./playground.py`` from ``myOpenWNS`` should give no error or
  warning message, but the standard help output.

* The installation of both the debug as well as the opt version of
  openWNS, from the source code to the ``myOpenWNS/sandbox`` directory,
  works without problems. Installation is started with the commands

  .. code-block:: bash

     $ ./playground.py install
     $ ./playground.py install  --flavour=opt

* All system and unit tests should run without errors. Tests are
  started with the command

  .. code-block:: bash

     $ ./playground.py runtests

* The plugin to create simulation campaigns, ``preparecampaign``, is
  available when running ``./playground.py``.

If all these steps succeed, you can create a new simulation campaign
which is then used for all the following experiments. A simulation
campaign consists of

#. a sub-directory ``sandbox`` that contains all necessary libraries
   and the openwns executable. After creation of the campaign, the
   directory will be changed to read-only mode in order to avoid
   changes to its content.

#. one or more directories to store the simulation configuration(s)
   and the results in. When the simulation campaign is initially
   created, this directory is named ``simulations``.

To create the simulation campaign, use the ``preparecampaign``-plugin
in the following way:

.. code-block:: bash

   $ ./playground.py preparecampaign ../myFirstCampaign
   Preparing simulation campaign. Please wait...

This will create the directory ``../myFirstCampaign``, including the
neccessary sub-directories. After some moments, the script requests
the following user input:

#. ``Do you want to use the database server for storing simulation
   campaign related data?`` Currently, the database storage of
   simulation results is in alpha stage only and not
   recommended. Also, it is not needed for this tutorial. Hence, you
   can reply with ``n``.

Then, the script will install the openWNS into the ``sandbox``
directory of the campaign and create an (initially empty)
``simulations`` directory. This directory can be used for the first
experiment.

For the other experiments, it is suggested to create sub-campaigns by
using again the ``preparecampaign`` plugin. Sub-campaigns use the same
version of the openWNS to run the simulations, but have a significant
different configuration file. When running

.. code-block:: bash

   $ ./playground.py preparecampaign ../myFirstCampaign

the script will ask (after the database-question):

.. code-block:: bash

   Found simulation campaign in directory /home/wns/myFirstCampaign.
   Shall I try to (U)pdate the sandbox or do you want to (C)reate a new sub campaign?
       Type 'e' to exit (u/c/e) [e]:

Use ``c`` to create the sub-campaign and type a useful name for the
directory, e.g. ``experiment2``.

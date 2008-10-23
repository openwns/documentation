===========
Preparation
===========

In the following, it is assumed that the openWNS source code is
situated in the directory ``openWNS``.

Make sure that the following points are met within your openWNS
installation:

* Running ``./playground.py`` from ``openWNS`` should give no error or
  warning message, but the standard help output.

* The installation of both the debug as well as the opt version the
  openWNS from the source code to the directory ``openWNS/sandbox``
  works without problems. Installation is started with the commands::

 	./playground.py install
	./playground.py install  --flavour=opt

* All system and unit tests should run without errors. Tests are
  started with the command::

  	./playground.py runtests

If all these steps succeed, you can create a new simulation campaign
which is then used for all the following experiments. A simulation
campaign consists of

#. a sub-directory ``sandbox`` that contains all necessary libraries
   and the wns-core. After the creation of the campaign the directory
   will be changed to read-only mode in order to prevent accidently
   removing the directory or altering its content.
#. a directory to store the simulations, the default is ``simulations``.

With the command ``./playground.py preparecampaign PATH``, with
``PATH`` as the root directory of the campaign, the campaign is
created. After some moments, the script requests the following user input:

#. Use the database to store simulation parameters and results? For
   fast and efficient evaluation of the generated results, it is
   recommended to use the database.
#. Name of the directory to store
   simulations; the default is fine.
#. Name of the campaign.
#. Description of the campaign.

If the directory ``PATH`` already contains a valid simulation campaign, the script offers two options:

#. To update the content of the ``sandbox`` directory with the current version of the openWNS.
#. To add a new sub-campaign in a new simulation directory.

For the different experiments, we suggest to use different
sub-campaigns, e.g. with names Experiment1, Experiment2, etc.

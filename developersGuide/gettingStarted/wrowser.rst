----------------------
Installing the Wrowser
----------------------

The Wrowser (an acronym for Wireless network simulator Result brOWSER)
supports with a graphical interface the collection of results,
extraction of measurements and creation of parameter
plots. Furthermore, the Wrowser helps to create simulation campaigns
with large parameter spaces. The Wrowser is a project separated from
the openWNS and thus has to be installed independently.

.. important::
   The following steps are only required if you want to
   use the Wrowse to view simulation results. To run a single
   simulation and to evaluate the results using the text-output files,
   the Wrowser is not needed.


Prerequisites
-------------

Similar to the openWNS the Wrowser relies third party software. Each
of the listed libraries and programs below are freely
available.

 * python-qt4_ A comprehensive set of Python bindings for the Qt cross-platform GUI/XML/SQL C++ framework from Qt Software
 * python-qt4-dev Tools Development tools for python-qt4_
 * python-matplotlib_ A python 2D plotting library which produces publication quality figures in a variety of hardcopy formats and interactive environments across platforms.
 * python-tk_ Python's de-facto standard GUI (Graphical User Interface) package.

.. _python-qt4: http://wiki.python.org/moin/PyQt
.. _python-matplotlib: http://matplotlib.sourceforge.net/
.. _python-tk: http://wiki.python.org/moin/TkInter

Installation
------------

Similar to the openWNS installation, the Wrowser can be obtained and
updated using Bazaar. The following command will checkout the current
version of the Wrowser into the directory 'wrowser'. Choose whatever
you want as name.

.. code-block:: bash

   $ bzr branch lp:openwns-wrowser wrowser
   Branched 27 revision(s).
   $ cd wrowser
   $ scons

You should now be able to start the Wrowser using

.. code-block:: bash

   $ bin/wrowser

It will open an empty window, see :ref:`figure-gettingstarted-wrowser`.

.. _figure-gettingstarted-wrowser:

.. figure:: images/wrowser.*
   :align: center

   The initial, empty Wrowser window

Adding the wrowser-plugin into playground.py
--------------------------------------------

The Wrowser comes with a plugin for the playground.py that supports
the setup of simulation campaigns, i.e., a compiled version of the
openWNS together with a configuration and a set of parameters that
shall be simulated. Each simulation campaign also provides a tool to
start, stop and query the status of the simulations.

The playground.py script of your openWNS installation gathers these
plugins in all directories specified in the file
``playground.config``, which is located in the directory ``.wns`` in
your home folder. Open this file with an editor and add the following
two lines:

.. code-block:: bash

   [AdditionalPluginPaths]
   path1 = [path to the wrowser]/wrowser/wrowser/playgroundPlugins

Of course, you must replace ``[path to the wrowser]`` with the
directory where you have installed the Wrowser in the previous step.

Then, go into your openWNS - directory created during the installation
of the openWNS and call playground.py. If everything went right, you
should see the new command ``preparecampaign``:

.. code-block:: bash

   $ ./playground.py
   [...]
   preparecampaign :  Prepare a simulation campaign.
   [...]

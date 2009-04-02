.. _gettingStartedPrerequisites:

-------------
Prerequisites
-------------

openWNS relies on a number of third party software. Each of the listed
libraries and programs below are freely available. openWNS is built
entirely around free software. Some of the software is optional.


Third party libraries
---------------------

 * CppUnit_ (>=1.10) The basic unit testing framework
 * Python_ (>=2.4) Used by almost everything starting from the build framework to configuration
 * SciPy_ Pythons open-source software for mathematics, science, and engineering
 * Boost_ Mainly used to have the TR1 implementations of the upcoming C++ standard available

.. _CppUnit: http://cppunit.sourceforge.net/
.. _Python: http://www.python.org
.. _SciPy: http://www.scipy.org/
.. _Boost: http://www.boost.org/

Build framework
---------------

 * Bazaar_ The Revision Control System
 * SCons_ (>=0.96) A make replacement
 * GCC_ (>=3.4) Compiler Suite, due to usage of special language features regarding templates the versions below 3.4 do not work

.. _Bazaar: http://bazaar-vcs.org/
.. _SCons: http://www.scons.org
.. _GCC: http://gcc.gnu.org/

Optional for build framework
----------------------------

 * Doxygen_ Documentation is generated with this tool
 * Graphviz_ Used by doxygen to create nice UML diagrams
 * Icecream_ Allows for distributed compiling

.. _Doxygen: http://www.doxygen.org/
.. _Graphviz: http://www.graphviz.org/
.. _Icecream: http://wiki.kde.org/icecream


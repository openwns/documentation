===============
Getting Started
===============

.. _gettingStartedPrerequisites:

Prerequisites
-------------

openWNS relies on a number of third party software. Each of the listed
libraries and programs below are freely available. openWNS is built
entirely around free software. Some of the software is optional.


*Third party libraries:*

 * CppUnit_ (>=1.10) The basic unit testing framework
 * Python_ (>=2.4) Used by almost everything starting from the build framework to configuration
 * Boost_ Mainly used to have the TR1 implementations of the upcoming C++ standard available

.. _CppUnit: http://cppunit.sourceforge.net/
.. _Python: http://www.python.org
.. _Boost: http://www.boost.org/

*Build framework:*

 * Bazaar_ The Revision Control System
 * SCons_ (>=0.96) A make replacement
 * GCC_ (>=3.4) Compiler Suite, due to usage of special language features regarding templates the versions below 3.4 do not work

.. _Bazaar: http://bazaar-vcs.org/
.. _SCons: http://www.scons.org
.. _GCC: http://gcc.gnu.org/

*Optional for build framework:*

 * Doxygen_ Documentation is generated with this tool
 * Graphviz_ Used by doxygen to create nice UML diagrams
 * Icecream_ Allows for distributed compiling

.. _Doxygen: http://www.doxygen.org/
.. _Graphviz: http://www.graphviz.org/
.. _Icecream: http://wiki.kde.org/icecream

Download
--------


.. important::
  Before you actually start with the download make sure
  your system has all the necessary software to install and run openWNS: see
  :ref:`gettingStartedPrerequisites`.

.. note:: 
  This download instructions are a little bit longer than
  others (e.g. where you just need to download a .tgz-file). But it pays
  off as soon as you want to retrieve your first update. In the end the
  download should not take more than 5 minutes (time for downloading not
  included).

*Short version:*

.. code-block:: bash

   bzr branch http://launchpad.net/~comnets/openwns-sdk/sdk--main--1.0 myOpenWNS
   cd myOpenWNS
   ./playground.py upgrade --noAsk


Configuring Bazaar
------------------

Like many other software projects openWNS is available via a revision
control system. The system is called Bazaar.  Thus, in order to
download openWNS you need Bazaar. For most distributions (SuSE,
Debian, Ubuntu, ...) Bazaar is available as package. In any other case
you will need to build it from the sources available here_

.. _here: http://bazaar-vcs.org/Download

To see if Bazaar is installed on your system and to check that you have
an up to date version you can try:

.. code-block:: bash

   $ bzr --version
   Bazaar (bzr) 0.92.0
   ...


If you haven't used Bazaar before you need to make yourself known to the system:

.. code-block:: bash

   $ bzr whoami "Joe Average <joe@average.com>"


Your id should be your name, followed by your email address in angle
brackets. Bazaar records your id in the log messages for your
commits. This information will @em not be used at any point when
you're just downloading openWNS (like now). For futher information on
Bazaar you can have a look at __ http://bazaar-vcs.org .

Retrieve a copy of openWNS
--------------------------

Now it's time to retrieve a copy of openWNS. The following command will
checkout the current version of openWNS to 'myOpenWNS'. Choose
whatever you want as name. A good name is 'openWNS-sdk--main--1.0' ;-).

.. code-block:: bash

   $ bzr branch http://launchpad.net/~comnets/openwns-sdk/sdk--main--1.0 myOpenWNS
   Branched 70 revision(s).
   $ cd myOpenWNS

Now you have a local copy of openWNS. Well, not really. What you have
is rather an empty house. If you inspect all the sub-directories of @c
myLocalDirectory at this moment, you would notice that they are almost
all empty. Apart from some bash and Python scripts there is not much
to see. Especially no C++ source code below the directory @c
framework.

.. code-block:: bash

   $ cd myLocalDirectory
   $ ls framework/

So let's furnish this house! openWNS is designed to be a highly
modular simulation framework. Hence, it is made up of a number of
modules. Each module again is a Bazaar project (just like the one
you've just fetched). Normally you would have to fetch each Bazaar
project (or each module) by hand (like you did with this). This is
very tedious. Fortunately, there is a program that helps you with this
task (and other task as you will learn). It is called @c
playground.py. So to fetch all modules and necessary other data simply
enter:

.. code-block:: bash

  $ ./playground.py upgrade
  Warning: According to 'config/projects.py' the following directories are missing:
    ./tests/unit (from URL: http://launchpad.net/~comnets/openwns-unittests/unittest--main--1.0)
    ./framework/buildSupport (from URL: http://launchpad.net/~comnets/openwns-buildsupport/buildsupport--main--1.0)
    ./supportlibs (from URL: http://launchpad.net/~comnets/openwns-supportlibs/supportlibs--main--1.0)
    ./documentation (from URL: http://launchpad.net/~comnets/openwns-documentation/documentation--main--1.0)
    ./framework/library (from URL: http://launchpad.net/~comnets/openwns-library/library--main--1.0)
    ./framework/application (from URL: http://launchpad.net/~comnets/openwns-application/application--main--1.0)
    ./framework/pywns (from URL: http://launchpad.net/~comnets/openwns-pywns/pywns--main--1.0)
  Try fetch the according projects? (Y/n) y

Just answer ``y`` to this question and all necessary projects will be
fetched. Depending on your link speed and the current size of openWNS this
can take several minutes.

After the download has finished you have all pieces available to
proceed with the @ref installation of openWNS. Now there should be the
framework available:

.. code-block:: bash

  $ ls framework/*
  buildSupport
  library/
  application/
  pywns/


Installation
------------

After you have successfully downloaded (see @ref download) openWNS you
are ready to install openWNS. Make sure you satisfy all @ref
prerequisites.

The installation itself is quite easy:

.. code-block:: bash

  ./playground.py install --flavour=dbg

After building has finished you can find the respective modules in
``./sandbox/dbg/``.

Under ``./sandbox/dbg/bin/`` you should find a binary which is called
``openwns``. If you want to check if everything worked change to:

.. code-block:: bash
  
  cd tests/unit/unitTests

and say

.. code-block:: bash
  
  ./openwns -t -v

``-t`` runs all available unit tests and ``-v`` puts ``openwns`` into verbose mode
(``--help`` shows all available options).

SDKLayout
---------


The SDK (Software Development Kit) keeps all other sub projects of
openWNS. The structure of the SDK as well as the location of the sub
projects is as follows (note, a directory followed by a name in square
means the directory is a sub project):

 - ``openWNS-sdk/``: master project
 - ``openWNS-sdk/bin/`` : helper scripts
 - ``openWNS-sdk/config/`` : configuration for the SDK
 - ``openWNS-sdk/config/projects.py`` : defines the projects being part of this working copy
 - ``openWNS-sdk/config/private.py`` : user defined compilation settings
 - ``openWNS-sdk/config/pushMailRecipients.py`` : list of recipients for mail on 'bzr push'
 - ``openWNS-sdk/config/valgrind.supp`` : openWNS-specific valgrind suppressions
 - ``openWNS-sdk/documentation/`` : the documentation project
 - ``openWNS-sdk/framework/`` : core part (lib, simulator application) of openWNS
 - ``openWNS-sdk/framework/application/`` : core application project
 - ``openWNS-sdk/framework/library/`` : core library project
 - ``openWNS-sdk/framework/buildSupport/`` : build system project
 - ``openWNS-sdk/framework/pywns/`` : post processing, system tests in python

 - ``openWNS-sdk/modules/`` : reserved for future use

 - ``openWNS-sdk/sandbox/`` : the build system will install libs and apps here

 - ``openWNS-sdk/tests/``
 - ``openWNS-sdk/tests/unit/`` : Python annd C++ unit tests
 - ``openWNS-sdk/tests/system/`` : reserved for future use

 - ``openWNS-sdk/wnsbase/`` : SDK builtins

Most important are probably the ``framework`` and ``tests/unit``
directory ;-).

.. note:
   When openwns-sdk is initial download the sub projects are not
   contained in the SDK. See @ref download for further instructions on how to
   fetch the missing parts.

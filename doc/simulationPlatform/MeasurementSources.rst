
.. index::
   single: measurements; measurement source
   single: measurement source

Measurement Sources
===================


Introduction
------------

openWNS decouples the generation and evaluation of
measurements. The evaluation, may that be logging, filtering, sorting
or simply storing them is described in detail in
:ref:`simulationPlatformEvaluationFramework`. 
In the following, the focus is solely on the generation of
measurements and adding context information to them, which than may be
processed by the evaluation framework.

Concept
-------

In the following we will be making use of some fundamental conecepts
regarding the implementation of measurement sources, which will be
defined now.

measurement source
    A measurement source is a logical concept that describes a
    location within the simulator where a measurement value is measured and is
    made available to the evaluation framework. A measurement value
    has a timestamp, which holds the time when the measurement value
    was generated. A  measurement value may have context information.

measurement value
    A ``double`` value representing a measurement of some phenomenon
    in your simulator

context
    A dictionary mapping an arbitrary but unique name to an ``int``
    value. The context captures the state (within a certain scope) of
    your simulator when a measurement value is measured.

Realization
-----------

Measurement sources, values and their context information is realized by
``wns::probe::bus::ProbeBus``. The ``ProbeBus`` realizes the
connection of measurement sources to the evaluation
framework. ``wns::probe::bus::Context`` realizes the context
information.

Commonly, the entries in the context information of each measurement
source do not change during the whole simulation (of course the value
of each entry changes over time, but not the name). In such cases the
``wns::probe::bus::ContextCollector`` should be used to
automatically generate the context information and the timestamp when
a measurement souce generates a measurement value and passes it on to
the evaluation framework. The
``wns::probe::bus::ContextProviderCollection`` and
``wns::probe::bus::ContextProvider`` are used to define which context
information is to be gathered by the ``wns::probe::bus::ContextCollector``.

Implementing a Measurement Source
------------------------------------

To add a measurement source to some class of your simulator you need
to add

.. literalinclude:: ../../../.createManualsWorkingDir/wns.probe.bus.tests.DevelopersGuideTest.include.example

to the header file of that class. Suppose you have implemented a
simple queueing model with a ``Job`` class that has some priority and
that records the time when processing started. It may look like this:

.. literalinclude:: ../../../.createManualsWorkingDir/wns.probe.bus.tests.DevelopersGuideTest.job.example

Furthermore, let us say that you have a class ``Processor`` that will
process a ``Job`` and then generate a measurement of the processing
time. The context of this measurement will be the ``Job``'s priority
class. The ``Processor`` class may look like this:

.. literalinclude:: ../../../.createManualsWorkingDir/wns.probe.bus.tests.DevelopersGuideTest.processor.example
 
The class has two methods ``startJob()`` and ``onJobEnded``. It has 
a distribution member variable to draw randomly distributed processing
delays. To generate measurements we need a pointer to a
``wns::probe::bus::ProbeBus``. This is your connection poit to the
evaluation framework. Let's have a look at the constructor of
``Processor``.

.. literalinclude:: ../../../.createManualsWorkingDir/wns.probe.bus.tests.DevelopersGuideTest.constructor.example

To initialize our ``ProbeBus`` we ask the
``wns::probe::bus::ProbeBusRegistry`` to create one for us and
register it with a unique name. Since we want to measure processing
delay we choose the name ``processor.processingDelay``. You should
always prefix your measurement source name with the namespace of your
class to make it unique. You will see in
:ref:`simulationPlatformEvaluationFramework` that this name is used
to connect your evaluation to the measurement source.

Let's see what happens if someone request the processor to start a
job. Here is ``startJob``:

.. literalinclude:: ../../../.createManualsWorkingDir/wns.probe.bus.tests.DevelopersGuideTest.startJob.example

We get the event scheduler and record the current time in the
``job.startedAt_``. Then we draw a random processing time form the distribution
and schedule a delayed call to our the ``onJobEnded`` method. If you
do not understand how the scheduling works please read
:ref:`simulationPlatformEventScheduler` first.

So let's see how to generate the processing delay measurements. This
is done int ``onJobEnded``.

.. literalinclude:: ../../../.createManualsWorkingDir/wns.probe.bus.tests.DevelopersGuideTest.stopJob.example

Since we want to provide context information for our measurement value
we first create an empty ``wns::probe::bus::Context`` and populate it
with the job's priority which we read from the ``Job`` itself. Then we
get the current time from the scheduler and calculate the measurement
value, which is simply the current time minus the job's start time,
i.e. the processing delay.

Everything is prepared now. We have the *measurement value*, the
*timestamp* and the *context*. To pass it on to the evaluation
framework, we first assure that ``probeBus_`` is not ``NULL`` and then
call ``forwardMeasurement`` of our ``probeBus_``.

Making use of the Context Collector
-----------------------------------

to be written.

Publication of Measurements
---------------------------

Assuming you have obtained a measurement, you would like to publish it so
it can be handled in any way you desire. When publishing the measurement,
it is not necessary to know in which way and by whom it is being processed.
However, the entities that do process the measurement may require certain
additional information about the circumstances under which the measurement
was taken, e.g. which Node has taken the measurement, at which point in the
scenario it was taken, what kind of node took it, which Traffic Category
the measured packet belongs to, where the packet originated from, etc. etc.

We refer to this kind of information as the so called
@link wns::probe::bus:::IContext Context @endlink of the measurement. Hence,
the process of publishing the measurement involves gathering and compiling
this Context and then forwarding everything to the appropriate processing
entities. All this is handled by the
@link wns::probe::bus::ContextCollector ContextCollector@endlink.
The only information the
@link wns::probe::bus::ContextCollector ContextCollector@endlink needs to have
about the processing of the measurements is a configurable name of the
ProbeBusID into which to forward the measurement and the context info.

Entry points to the existing ProbeBusses are governed by a global Registry
called the @link wns::probe::bus::ProbeBusRegistry ProbeBusRegistry@endlink.
They may be accessed via the aforementioned name.

<b>NOTE</b> that the @link wns::probe::bus::ProbeBus ProbeBusses @endlink
are <b>centralized</b>, while the publication of measurements is
<b>distributed</b>. This means that all entities that take and publish
measurements of the same type have a
@link wns::probe::bus::ContextCollector ContextCollector@endlink
of their own, but all these @link wns::probe::bus::ContextCollector
ContextCollectors @endlink forward their measurements and context into
the same @link wns::probe::bus::ProbeBus ProbeBus@endlink.

See @ref wns_probe_bus_contextcollector for more information on the
@link wns::probe::bus::ContextCollector ContextCollector@endlink

Processing of Measurements
--------------------------

Processing of measurements is accomplished by the
@link wns::probe::bus::ProbeBus ProbeBus@endlink.
The @link wns::probe::bus::ProbeBus ProbeBus@endlink is an object that
supports hierarchical chaining to form trees of
@link wns::probe::bus::ProbeBus ProbeBusses@endlink.
The measurement and the @link wns::probe::bus::IContext context@endlink are
inserted at the root of the tree and each
@link wns::probe::bus::ProbeBus ProbeBus@endlink may
store and forward the received measurement, depending on the outcome of an
internal decision unit that determines whether or not the current node
@link wns::probe::bus::ProbeBus::accepts() accepts@endlink the measurement.
By appropriate combination and parameterization, the said tree can then be
used to filter and thus sort the measurements based on the available
@link wns::probe::bus::IContext context@endlink information. openWNS
provides a @ref probebusses "toolbox" of different
@linkwns::probe::bus::ProbeBus ProbeBus@endlink implementations
that can be flexibly combined to accomplish all kinds of measurement
processing tasks. In addition, the simple
@link wns::probe::bus::ProbeBus ProbeBus@endlink interface and the very
generic @link wns::probe::bus::IContext context@endlink information concept
allow for the quick prototyping of tailor-made solutions.

Measurement Publication by using the ContextCollector
-----------------------------------------------------

The ContextCollector serves the task of gathering context information. To do
so, it creates an empty Context object and asks the ContextProviderCollection
to add information into that object. After that, it forwards the measured
value and the Context to the (root of a) ProbeBus hierarchy.
When being constructed, the ContextCollector relies on two mandatory parameters:

-# A ContextProviderCollection, of which the ContextCollector will make a
copy for its internal purposes. (The copying allows to instantiate a number
of ContextCollectors with the same instance of the local
ContextProviderCollection)
-# The unique, identifying name of the ProbeBus into which to forward the
measurements (under this name the ContextCollector will look up in the
wns::probe::bus::ProbeBusRegistry
This procedure is illustrates in the sequence diagram below
@msc
hscale="2";
MeasurementSource,
ContextCollector [label = "ContextCollector", URL="\ref wns::probe::bus::ContextCollector"],
ContextProviderCollection [label = "ContextProviderCollection", URL="\ref wns::probe::bus::ContextProviderCollection"],
ContextProvider [label = "ContextProvider", URL="\ref wns::probe::bus::IContextProvider"],
ProbeBus [label = "ProbeBus", URL="\ref wns::probe::bus::ProbeBus"];

MeasurementSource=>>ContextCollector [label = "ContextCollector(ContextProviderCollection, probeBusID)", URL="\ref wns::probe::bus::ContextCollector::ContextCollector()", ID="1"];
MeasurementSource=>>ContextCollector [label = "put(measurement)", URL="\ref wns::probe::bus::ContextCollector::put()"];
ContextCollector=>>ContextProviderCollection [label = "fillContext(context, compound)", URL="\ref wns::probe::bus::ContextProviderCollection::fillContext()", ID="2"];
--- [label = "foreach ContextProvider in ContextProviderCollection"];
ContextProviderCollection=>>ContextProvider [label = "visit(context, compound)", URL="\ref wns::probe::bus::IContextProvider::visit()", ID="3"];
ContextProviderCollection<<ContextProvider;
--- [label = "next ContextProvider"];
ContextCollector<<ContextProviderCollection;
ContextCollector=>>ProbeBus [label = "forwardMeasurement(timestamp, measurement, context)", URL="\ref wns::probe::bus::ProbeBus::forwardMeasurement()"];
--- [label = "ProbeBus forwards measurement to all its accepting children"];
ContextCollector<<ProbeBus;
MeasurementSource<<ContextCollector;
@endmsc
<OL>
<LI> In this example the MeasurementSource creates the ContextCollector. The
creation can be done by any object. The MeasurementSource only needs to know
its ContextCollector object to place the put() call.
<LI> If only the measurement is used when putting the compound is set to an
empty compound automatically. A description on gathering context from
compounds will follow
<LI> The ContextProvider may add any number of key, value pairs to the Context
</OL>



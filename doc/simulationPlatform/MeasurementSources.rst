Measurement Sources
===================


Introduction
------------

In a nutshell, openWNS now decouples the generation and publication of
measurements from their processing, may that be logging, filtering, sorting
or simply storing them. In the following, it will shortly be explained what
generation, publication and processing are about.

Generation of Measurements
--------------------------

Generating measurement values is up to you, the Implementer of a certain,
class, module, node, whatever that might be. Measurements may currently be
everything that can be represented by a double value, like SINR,
Interference, Power values, delay times, packet sizes, throughput figures ...

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



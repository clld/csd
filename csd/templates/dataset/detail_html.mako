<%inherit file="../home_comp.mako"/>
<%namespace name="util" file="../util.mako"/>

<%def name="sidebar()">
    <%util:well title="Cite">
        ${h.newline2br(h.text_citation(request, ctx))|n}
        ${h.cite_button(request, ctx)}
    </%util:well>
</%def>

<h2>Comparative Siouan Dictionary</h2>

<p class="lead">
    Compiled by:
    Richard T. Carter, Willem de Reuse, Randolph Graczyk, A. Wesley Jones,
    John E. Koontz. Robert L. Rankin, David S. Rood, Patricia A. Shaw, and Paul Voorhis,
    at the Siouan Workshop held in the
    Summer of 1984 at the University of Colorado.
</p>
<p>
    The dictionary project was
    sponsored by NEH
    (RT-21062-89; RT-21238-91). The 1984 Comparative Siouan Workshop was
    held at the University
    of Colorado under sponsorship of NSF (BNS 8406236) and NEH (RD
    20477-84). Additional data
    were provided by Jimm Good Tracks, Kenneth Miner, Carolyn Quintero and
    Kathleen Shea.
</p>
<p>
    Senior editors:
    Richard T. Carter, A. Wesley Jones, Robert L. Rankin
    with John E. Koontz and David S. Rood
</p>
<p>
    Project and workshop Principal Investigator:
    David S. Rood
</p>
<p>
    This dictionary is a work in progress. It will probably always be a
    work in progress. However, it represents a vast amount of time and
    effort by a large number of people, and all of us agree that it should
    be made available to other interested people now.  We hope there will be
    provisions for you to make changes and additions, but right now we only
    offer you the chance to mine it for information which should be double
    checked before it's utilized.
</p>
<p>
    The project which culminates in this work dates to a workshop at the
    University of Colorado in 1984.  A fairly thorough history, including
    comments on the continuously evolving technological tools, can be found
    in Rood and Koontz (2002).  The primary compiler/analysts were Robert L.
    Rankin, Richard T. Carter, A. Wesley Jones, John E. Koontz and David S.
    Rood.  Since 2009, Iren Hartmann and the computer staff at the Max
    Planck Institute for Evolutionary Anthropology in Leipzig, Germany, have
    been working to create this web-based version.  Financial support [check
    the users manual for the archive and the Missouri paper]
</p>
<p>
Because this has been a team effort, there are many inconsistencies.
Because it has been developing for so many years, there are features
that we no longer understand and abbreviations we no longer remember.
We have made as many corrections and reconciled as many discrepancies as
we could, while hoping not to lose information in the process.  Below is
a list of things to watch out for:
</p>
<ol>
    <li>Part of speech designations refer to the reconstructed word, but
often with some uncertainty.  We have elected not to use the term
"postposition", substituting "ADV" for that.  Some of us think that
these words are probably relational nouns, but that is a topic for
further investigation.</li>
    <li>Verbs have not been subdivided into transitive, intransitive,
stative, impersonal, etc. because these categories sometimes vary among
the daughter languages.</li>
    <li>At one point the editors attempted to assign "semantic category"
terms like "plant", "action verb", or "color term" to the
reconstructions, but it proved to be difficult to agree on many of
these.  We have not eliminated those that were assigned, however;
perhaps someone would like to propose ways to be consistent about
supplying this information.  Some of these categories may be revealing
for morphological reconstruction, e.g. many body part terms may have had
an initial *i- possessive prefix which has been lost, but not without
traces, in some of the daughter languages.</li>
    <li>At one point the editors hoped to be able to present all the data
from all the languages in a single, consistent orthography. Toward that
end, many citations will be in two forms: the original as written in the
source notes or publications, and a second form preceded by a daggar ().
We have tried to automate the conversion from the source spellings to
the daggered spellings, but unsuccessfully.  So some entries will have
daggered alternatives and some will not.</li>
    <li>Not all the sources could be recovered, and not all of those cited
can be confirmed.  Someone has added information without proper
acknowledgement, and we have not been able to correct for that.</li>
    <li>Dashes (-) in the middles of words represent morpheme boundaries.</li>
    <li>Frequently a form in a daughter language will appear without a
gloss.  In those cases, the gloss assigned to the reconstruction is the
same as that in the daughter.  Again, there has been an attempt to
insert the missing glosses automatically, but there may be gaps.</li>
    </ol>
##<p>
##Please submit any comments or questions (or corrections) to
##</p>
<p>
Reference:
</p>
<blockquote>
Rood, David S. and John E. Koontz.  2002. "The Comparative Siouan
Dictionary Project".  In Frawley, William, Kenneth C. Hill and Pamela
Monroe, eds.  Making Dictionaries: Preserving Indigenous Languages of
the Americas, 259-281. Berkeley: Univ. of Calif. Press.
</blockquote>
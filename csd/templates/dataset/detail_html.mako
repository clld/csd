<%inherit file="../home_comp.mako"/>
<%namespace name="util" file="../util.mako"/>

<%def name="sidebar()">
    <%util:well title="Cite">
        ${h.newline2br(h.text_citation(request, ctx))|n}
        ${h.cite_button(request, ctx)}
    </%util:well>
    ${util.feed('Latest Comments', request.blog.feed_url('comments/feed/', request), eid='comments')}
</%def>

<h2>Comparative Siouan Dictionary</h2>

<p style="font-size: medium;">
    Compiled by:
    Richard T. Carter, Willem de Reuse, Randolph Graczyk, A. Wesley Jones,
    John E. Koontz. Robert L. Rankin, David S. Rood, Patricia A. Shaw, and Paul Voorhis,
    at the Siouan Workshop held in the Summer of 1984 at the University of Colorado.
</p>
##<p>
##    The dictionary project was
##    sponsored by NEH
##    (RT-21062-89; RT-21238-91). The 1984 Comparative Siouan Workshop was
##    held at the University
##    of Colorado under sponsorship of NSF (BNS 8406236) and NEH (RD
##    20477-84). Additional data
##    were provided by Jimm Good Tracks, Kenneth Miner, Carolyn Quintero and
##    Kathleen Shea.
##</p>
##<p>
##    Senior editors:
##    Richard T. Carter, A. Wesley Jones, Robert L. Rankin
##    with John E. Koontz and David S. Rood
##</p>
##<p>
##    Project and workshop Principal Investigator:
##    David S. Rood
##</p>
<div style="text-align: center;">
    <h3>Introduction</h3>
    <h5>
        David S. Rood, Principal Investigator<br/>
        University of Colorado<br/>
        May 2015
    </h5>
</div>
<p>
    This dictionary is a work in progress. It will probably always be a work in progress.
    However, it represents a vast amount of time and effort by a large number of people, and
    all of us agree that it should be made available to other interested people now.  While
    the original data set will be preserved in its most recent stage and cannot be changed,
    there is a way  for you to make additions by leaving comments and your thoughts via our
    commenting feature.  Of course we also  encourage you to mine it for information which
    should be double checked before it is utilized.  The attached paper
    (<a href="#rankin-1998">Rankin et al. 1998</a>)
    summarizes many of the conclusions about proto-Siouan to which the work on the dictionary
    has led us.
</p>
<p>
    The project which culminates in this work dates to a workshop at the University of
    Colorado in 1984. A fairly thorough history, including comments on the continuously
    evolving technological tools, can be found in
    <a href="#rood-2002">Rood and Koontz (2002)</a>.
    The primary compiler/analysts were Robert L. Rankin, Richard T. Carter,
    A. Wesley Jones, John E. Koontz and David S. Rood.
    Additional data were provided by Jimm Good Tracks, Kenneth Miner, Carolyn Quintero and Kathleen Shea.
    Since 2011, Iren Hartmann and
    the computer staff at the Max Planck Institute for Evolutionary Anthropology in Leipzig,
    Germany, have been working to create this web-based version. The main programmers on the
    project were Robert Forkel  and Hans-Jörg Bibiko. Financial support for the 1984 workshop
    came from NSF (BNS 8406236) and NEH (RD 20477-84). Financial support for the dictionary
    came from NEH (RT-21062-84; RT-21238-91). The second NEH grant included an offer to match
    funds we raised elsewhere, and such funds were received from the American Philosophical
    Society and the University of Colorado.
</p>
<p>
    Because this has been a team effort, there are many inconsistencies. Because it has been
    developing for so many years, there are features that we no longer understand and
    abbreviations we no longer remember.  Iren Hartmann and her colleagues at the
    Max Planck Institute for Evolutionary Anthropology in Leipzig have devoted many hours and
    considerable effort to cleaning out the inconsistencies and typing up loose ends, as well
    as to the design and functioning of the web site itself.  The entire Siouanist community
    and the other linguists on the project owe Iren a huge debt of gratitude.  Even so, there
    will be plenty of things for readers and users to comment on.
</p>
<p>
    Below is a list of things to watch out for:
</p>
<ol>
    <li>
        Part of speech designations refer to the reconstructed word, but
        often with some uncertainty.  We have elected not to use the term
        "postposition", substituting "ADV" for that.  Some of us think that
        these words are probably relational nouns, but that is a topic for
        further investigation.
    </li>
    <li>
        Verbs have not been subdivided into transitive, intransitive,
        stative, impersonal, etc. because these categories sometimes vary among
        the daughter languages and the part of speech is meant to refer to the
        reconstructed proto-form.
    </li>
    <li>
        At one point the editors attempted to assign “semantic category”
        terms like “plant”, “action verb”, or “color term” to the reconstructions, but it
        proved to be difficult to agree on many of these, so not very many entries had
        been assigned such a category In this web version, however, we have included the
        set of semantic domains as used in the Hoocąk dictionary database with some few
        additions. We hope that it may prove useful in sorting and filtering the data.
        All entries, except function words/grammatical markers, have been assigned a
        semantic category.  Some of these categories may be revealing for morphological
        reconstruction, e.g. many body part terms may have had an initial *i- possessive
        prefix which has been lost, but not without traces, in some of the daughter
        languages.
    </li>
    <li>
        At one point the editors hoped to be able to present all the data
        from all the languages in a single, consistent orthography.  Toward that
        end, many citations will be in two forms: the original as written in the
        source notes or publications (listed in the column “cognate”), and a second
        form preceded by a dagger (†) (listed in the column “phonetic Siouan”).  We
        have tried to automate the conversion from the source spellings to the daggered
        spellings, but unsuccessfully. So some entries will have daggered alternatives
        and some will not. All other forms are listed in the orthography as used in the
        cited resource, though over the years some changes may have been made in certain
        cases as well.
    </li>
    <li>
        Not all the sources could be recovered, and not all of those cited can be
        confirmed.  Someone has added information without proper acknowledgement, and
        we have not been able to correct for that.
    </li>
    <li>
        Dashes (-) in the middles of words represent morpheme boundaries.
    </li>
    <li>
        Frequently a form in a daughter language will appear without a gloss.
        In those cases, the gloss assigned to the reconstruction is the same as that
        in the daughter.  Again, there has been an attempt to insert the missing glosses
        automatically (listed in square brackets in the column “Meaning”), but there may
        be gaps.
    </li>
</ol>
<p>
    Please submit any
    <a href="${request.route_url('contact')}">comments, questions or bug reports (or corrections)</a>
    to iren.hartmann@gmail.com and david.rood@Colorado.EDU
</p>
<h4>Acknowledgements</h4>
<dl>
    <dt>At CU:</dt>
    <dd>
        hours and hours of data entry:  Jule Gomez de Garcia
    </dd>
    <dt>At MPI-EVAN:</dt>
    <dd>
        <ul>
            <li>
                Robert Forkel for including the CSD in his wonderful
                ${h.external_link('http://clld.org', label='CLLD framework')},
                for all his technical support and for programming the web site
            </li>
            <li>
                Soung-U Kim for his great mind and initiative and the many months spent on
                splitting fields and cleaning up inconsistencies
            </li>
            <li>
                Hans-Jörg Bibiko for his many clever scripts that helped us immensely in
                the initial conversion of the CSD from a word processor file (back) into
                a database
            </li>
            <li>
                Doreen Schrimpf for cleaning up many inconsistencies and for helping with
                the restructuring of the database file
            </li>
        </ul>
    </dd>
</dl>

<h4>UNCONVENTIONAL SYMBOLS IN THE RECONSTRUCTIONS</h4>

<dl>
    <dt>*E</dt>
    <dd>marks a vowel which is sometimes /a/, sometimes /e/, and in a few languages also sometimes
    /iN/ or /aN/ depending on the following grammatical context.  This is traditionally called
    “the ablaut vowel”.
    </dd>
    <dt>*R, *W</dt>
    <dd>These symbols represent reconstructed sounds which are like *r or *w but have a
    different set of reflexes.  Think of them as another kind of *r or *w.  The editors refer
    to them as “funny *r” and “funny *w”.  See Rankin, Carter and Jones (1998) for details.
    </dd>
    <dt>*S</dt>
    <dd>
        Stems with fricatives sometimes in some languages show a kind of positional sound
        symbolism, in that front (alveolar or dental) articulation marks a kind of diminutive
        sense, alveopalatal position represents a normal sense, and velar position represents
        an augmented sense. Some examples from Lakhota:
    <dl class="dl-horizontal">
	    <dt>zí</dt><dd>‘yellow’</dd>
        <dt>ží</dt><dd>‘tawny’</dd>
        <dt>ǧí</dt><dd>‘brown’</dd>
	    <dt>sóta</dt><dd>‘murky’</dd>
        <dt>šóta</dt><dd>‘muddy’</dd>
        <dt>ȟóta</dt><dd>‘grey’</dd>
    </dl>
    </dd>
</dl>
<p>
    This system is no longer productive in any of the languages, but sometimes only one of
    these grades survives, and it may not be the same grade across the languages.  The symbol
    *S therefore represents one of these sound-symbolic roots where we cannot be sure of the
    exact grade to reconstruct.
</p>


<h4>THE SIOUAN FAMILY TREE</h4>
<p>
    Family tree for languages used in this database; poorly attested languages (e.g. Woccon)
    are occasionally mentioned but not listed here:
</p>
<ul style="list-style-type: none;">
    <li>
        Siouan-Catawban
        <ul style="list-style-type: none;">
            <li>Catawba</li>
            <li>
                Siouan
                <ul style="list-style-type: none;">
                    <li>
                        Missouri Valley
                        <ul style="list-style-type: none;">
                            <li>Crow</li>
                            <li>Hidatsa</li>
                        </ul>
                    </li>
                    <li>Central Siouan
                        <ul style="list-style-type: none;">
                            <li>Mandan</li>
                            <li>
                                Mississippi Valley
                                <ul style="list-style-type: none;">
                                    <li>Dakotan (Lakota, Dakota (Santee-Sisseton, Yankton-Yanktonais), Assiniboine, Stoney)</li>
                                    <li>Chiwere-Winnebago (Chiwere (Iowa-Otoe), Hoocąk)</li>
                                    <li>Dhegiha (Kansa, Osage, Omaha-Ponca, Quapaw)</li>
                                </ul>
                            </li>

                        </ul>
                    </li>

                </ul>
            </li>
            <li>Ohio Valley
                <ul style="list-style-type: none;">
                    <li>Tutelo</li>
                    <li>Ofo-Biloxi</li>
                </ul>
            </li>
        </ul>

    </li>
</ul>
<p>
    The criteria for including a cognate set in the dictionary were that the set must be
    attested in two of the three major branches (Missouri Valley, Central Siouan, Ohio Valley).
    If we had allowed forms that were only attested in Central Siouan, there would have been
    hundreds of additional entries.
</p>

<h4>ROOT EXTENSIONS IN PROTO-SIOUAN: A SPECULATIVE OBSERVATION</h4>
<p>
	One problem in finding data to compare across Siouan languages is that a very large
number of verbs occur with a small number (less than a dozen) of instrumental prefixes.
To find the verb root, one has to subtract the prefix – and the languages may not agree on
which prefix, if any, can be used with a given root, even if the roots are cognate.
John Koontz devised a computer program for automating the subtraction of the prefixes,
thus enabling us to find many cognates that would otherwise have been obscured behind the
prefixes.
</p>
<p>
	Once that was done, editor A. Wesley Jones discovered that the roots sometimes
occurred as doublets, distinguished by one form with an additional consonant at the
beginning or at the end, while a second form with a similar meaning would occur without
that extra consonant. <a href="jones-1990">Jones’s (1990)</a> paper describing this phenomenon
    can be downloaded
below in the References section.  One of his examples, from Lakota, is pa-túza ‘bend over’
compared with pa-ptúza ‘bend over’. He termed the “extra” consonant (the p- at the
beginning of the second root, after the prefix) a “root extension” and speculated that
these root extensions were the remains of a pre-Proto-Siouan layer of morphology.  This
proposal was not accepted by all the editors, but an analysis of many words into roots
and root extensions is presented in the dictionary on the “languages” page under the
“proto-Siouan” heading.  A word like *sku(he) ‘peel’ will be analyzed   as †ku s.h,
meaning that the root was **ku, but in this form it has a pre-posed root extension “*s”
and a post-posed root extension  “*h”. Users of the dictionary should feel free to make
use of this proposal if they wish.
</p>

<h4 style="clear: both">References</h4>
<ul class="unstyled">
    <li id="jones-1990">
        <blockquote>
            Jones, A. Wesley.  1990.  The case for root extensions in Proto-Siouan.  In Ingemann, Frances, ed. 1990 Mid-America Linguistics Conference Papers, 505-517.  Lawrence, Ks.: University of Kansas Department of Linguistics.
            <a href="${request.static_url('csd:static/Jones_root_extensions.pdf')}">[PDF]</a>
        </blockquote>
    </li>
    <li id="rankin-1998">
        <blockquote>
            Rankin, Robert L., Richard T. Carter and A. Wesley Jones. 1998.
            Proto-Siouan Phonology and Grammar.
            In Xingzhong Li, Luis Lopez and Tom Stroik, eds.,
            Papers from the 1997 Mid-America Linguistics Conference, 366-375.
            Columbia:  University of Missouri-Columbia.
            <a href="${request.static_url('csd:static/Rankin_Carter_Jones_Proto-Siouan_Phonology.pdf')}">[PDF]</a>
        </blockquote>
    </li>
    <li id="rood-2002">
        <blockquote>
            Rood, David S. and John E. Koontz.  2002. “The Comparative Siouan Dictionary Project”.
            In Frawley, William, Kenneth C. Hill and Pamela Monroe, eds.
            Making Dictionaries: Preserving Indigenous Languages of the Americas, 259-281.
            Berkeley: Univ. of Calif. Press.
            <a href="${request.static_url('csd:static/Rood_Koontz_2002_CSD.pdf')}">[PDF]</a>
        </blockquote>
    </li>
</ul>


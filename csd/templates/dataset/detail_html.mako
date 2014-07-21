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

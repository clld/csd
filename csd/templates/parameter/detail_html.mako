<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">${_('Parameter')} ${ctx.name}</%block>

<ul class="pull-right nav nav-pills">
    <li><a href="#map-container"><span class="icon-globe"> </span> Map</a></li>
    <li><a href="#words"><span class="icon-list"> </span> Words</a></li>
    <li style="padding-top: 3px; padding-right: 3px;">
        ${h.cite_button(request, ctx.contribution)}
    </li>
    <li style="padding-top: 3px; padding-right: 3px;">
        ${u.comment_button(request, ctx)}
    </li>
    <li style="padding-top: 3px; padding-right: 3px;">
        ${h.alt_representations(request, ctx, doc_position='left')}
    </li>
</ul>

<h2>${ctx.name}</h2>

##<p>${ctx.psi_reconstruction_with_root_extension_code}</p>

<div id="dict-entry" style="margin-left: 2em; margin-right: 2em;">
    ${dict_entry.render(ctx, request)|n}
</div>

% if ctx.description:
<h4>General comment</h4>
<p>${u.insert_links(request, ctx.description)|n}</p>
% endif

% if ctx.othlgs:
    <h4>Other languages</h4>
    <ul class="unstyled">
    % for chunk in ctx.othlgs.split('\n---\n'):
    <li>
        ${u.markup_italic(chunk)|n}
    </li>
    % endfor
    </ul>
% endif

% if request.map:
    ${request.map.render()}
% endif

<div id="words">
${request.get_datatable('values', h.models.Value, parameter=ctx).render()}
</div>
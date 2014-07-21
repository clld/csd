<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">${_('Parameter')} ${ctx.name}</%block>

<h2>${ctx.name}</h2>

<div id="dict-entry" style="margin-left: 2em; margin-right: 2em;">
    ${dict_entry.render(ctx, request)|n}
</div>

% if ctx.description:
<p>${u.insert_language_links(request, ctx.description, languages)|n}</p>
% endif

% if request.map:
    ${request.map.render()}
% endif

${request.get_datatable('values', h.models.Value, parameter=ctx).render()}

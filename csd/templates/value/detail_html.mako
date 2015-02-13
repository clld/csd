<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "values" %>

<%def name="sidebar()">
    <p>
        ${u.comment_button(request, ctx)}
    </p>
    <%util:feed title="Comments" url="${request.blog.feed_url(ctx, request)}">
        No comments have been posted.
    </%util:feed>
</%def>

<h2>${_('Value')} ${ctx.name}</h2>

<dl>
    <dt>Language:</dt>
    <dd>${h.link(request, ctx.valueset.language)}</dd>
    <dt>Parameter:</dt>
    <dd>${h.link(request, ctx.valueset.parameter)}</dd>
    % if ctx.valueset.references:
        <dt>References</dt>
        <dd>${h.linked_references(request, ctx.valueset)|n}</dd>
    % endif
    % for k, v in ctx.datadict().items():
        <dt>${k}</dt>
        <dd>${v}</dd>
    % endfor
</dl>


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

<table class="table table-nonfluid">
    <tbody>
    <tr>
        <th>Language</th>
        <td>${h.link(request, ctx.valueset.language)}</td>
    </tr>
    <tr>
        <th>Entry</th>
        <td>${h.link(request, ctx.valueset.parameter)}</td>
    </tr>
        % if ctx.phonetic:
            <tr>
                <th>Phonetic Siouan</th>
                <td>${ctx.phonetic}</td>
            </tr>
        % endif
    <tr>
        <th>Meaning</th>
        <td>${ctx.description}</td>
    </tr>
        % if ctx.comment:
            <tr>
                <th>Comment</th>
                <td>${ctx.comment}</td>
            </tr>
        % endif
        % if ctx.original_entry:
            <tr>
                <th>Original entry</th>
                <td>${ctx.original_entry}</td>
            </tr>
        % endif
        % if ctx.valueset.references:
            <tr>
                <th>Sources</th>
                <td>${h.linked_references(request, ctx.valueset)|n}</td>
            </tr>
        % endif
    </tbody>
</table>


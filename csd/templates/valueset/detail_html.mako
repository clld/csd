<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>


<h2>Words in ${h.link(request, ctx.language)} for lemma ${h.link(request, ctx.parameter)}</h2>

% for i, value in enumerate(ctx.values):
    <h4>
        ${value.__unicode__()}
    </h4>
    <table class="table table-nonfluid">
        <tbody>
            % if value.alt_reconstruction:
                <tr>
                    <th>Alternative reconstruction</th>
                    <td>${value.alt_reconstruction}</td>
                </tr>
            % endif
            % if value.phonetic:
            <tr>
                <th>Phonetic Siouan</th>
                <td>${value.phonetic}</td>
            </tr>
            % endif
            <tr>
                <th>Meaning</th>
                <td>${value.description}</td>
            </tr>
            % if value.comment:
                <tr>
                    <th>Comment</th>
                    <td>${value.comment}</td>
                </tr>
            % endif
            % if value.original_entry:
            <tr>
                <th>Original entry</th>
                <td>${value.original_entry}</td>
            </tr>
            % endif
            % if value.references:
            <tr>
                <th>Sources</th>
                <td>${h.linked_references(request, value)|n}</td>
            </tr>
            % endif
        </tbody>
    </table>
% endfor

<%def name="sidebar()">
<div class="well well-small">
    <p>
        ${h.cite_button(request, request.dataset)}
    </p>
<dl>
    <dt class="language">${_('Language')}:</dt>
    <dd class="language">${h.link(request, ctx.language)}</dd>
    <dt class="parameter">${_('Parameter')}:</dt>
    <dd class="parameter">${h.link(request, ctx.parameter)}</dd>
    % if ctx.references or ctx.source:
    <dt class="source">${_('Source')}:</dt>
        % if ctx.source:
        <dd>${ctx.source}</dd>
        % endif
        % if ctx.references:
        <dd class="source">${h.linked_references(request, ctx)|n}</dd>
        % endif
    % endif
    ${util.data(ctx, with_dl=False)}
</dl>
</div>
</%def>
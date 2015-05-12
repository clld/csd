<% langs, valuesets = u.tree(ctx.valuesets) %>
<p class='entry'>
    ##<b style="font-size: larger">${ctx.name}</b><br/>
    % if ctx.ps:
        <i>${ctx.ps}</i>
    % endif
    % if ctx.sd:
        <span style="font-variant: small-caps">${ctx.sd}</span>
    % endif
    <br/>
    % for lang in langs:
        ${'&nbsp;' * 2 * lang.level|n}
        <span style="font-variant: small-caps; padding-left: 2px; padding-right: 2px; border: 2px solid #${lang.color};">${lang.name}</span>
        % for vs in valuesets[lang.id]:
            % for value in vs.values:
                ${u.markup_form(value.name)}
                % if value.phonetic:
                    <span>“${u.markup_form(value.phonetic)}”</span>
                % endif
                % if value.description:
                <span>‘${value.description}’</span>
                % endif
                % if value.comment:
                <span style="font-size: smaller">[${u.markup_italic(value.comment)}]</span>
                % endif
                % if value.references:
                <span style="color: gray;">
                    % for ref in value.references:
                    ${ref.source.name}${':' + ref.description if ref.description else ''},
                    % endfor
                </span>
                % endif
            % endfor
        % endfor
        <br/>
    % endfor
</p>
<% langs, valuesets = u.tree(ctx.valuesets) %>
<div class='entry'>
    ##<b style="font-size: larger">${ctx.name}</b><br/>
    <p>
    % if ctx.ps:
        <i>${ctx.ps}</i>
    % endif
    % if ctx.sd:
        <span style="font-variant: small-caps">${ctx.sd}</span>
    % endif
    </p>
    % for lang in langs:
        ##${'&nbsp;' * 2 * lang.level|n}
            <p style="margin-bottom: 2px; margin-left: ${lang.level}em">
        <span style="font-variant: small-caps; padding-left: 2px; padding-right: 2px; border: 2px solid #${lang.color};">${lang.name}</span>
        % for vs in valuesets[lang.id]:
            % for value in vs.values:
                ${'' if loop.first else ','}
                % if not value.phonetic or value.name[1:-1] != value.phonetic:
                    ${u.markup_form(value.name)}
                % endif
                % if value.phonetic:
                    ##<span>“${u.markup_form(value.phonetic)}”</span>
                    ${', ' if value.name[1:-1] != value.phonetic else ''}${u.markup_form(value.phonetic)}
                % endif
                % if value.description and value.description[1:-1] != ctx.name:
                <span>‘${value.description}’</span>
                % endif
                % if value.comment:
                <span style="font-size: smaller">[${u.markup_italic(value.comment)}]</span>
                % endif
                % if value.references:
                <span style="color: gray;">
                    % for ref in value.references:
                    ${ref.source.name}${':' + ref.description if ref.description else ''}${'' if loop.last else ','}
                    % endfor
                </span>
                % endif
            % endfor
        % endfor
        </p>
    % endfor
</div>
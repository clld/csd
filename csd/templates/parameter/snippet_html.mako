<p class='entry'>
    <b style="font-size: larger">${ctx.name}</b><br/>
    % if ctx.ps:
        <i>${ctx.ps}</i>
    % endif
    % if ctx.sd:
        <span style="font-variant: small-caps">${ctx.sd}</span>
    % endif
    <br/>
    % for vs in sorted(ctx.valuesets, key=lambda _vs: _vs.language.ord):
        % if vs.language.proto:
        <br/>
        % endif
        <span style="font-variant: small-caps; color: ${'blue' if vs.language.proto else 'green'}">${vs.language.name}</span>
        % for value in vs.values:
            <i>${value.name}</i>
            % if value.altform:
                <span>“${value.altform}”</span>
            % endif
            % if value.description:
            <span>‘${value.description}’</span>
            % endif
            % if value.comment:
            <span style="font-size: smaller">[${value.comment}]</span>
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
</p>
<%inherit file="app.mako"/>


<%block name="brand">
    <a class="brand" href="${request.route_url('dataset')}">CSD</a>
</%block>

${next.body()}

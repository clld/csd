<%inherit file="app.mako"/>

##
## define app-level blocks:
##
<%block name="head">
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
        google.load("feeds", "1");
    </script>
</%block>

<%block name="brand">
    <a class="brand" href="${request.route_url('dataset')}">CSD</a>
</%block>

${next.body()}

Make Grafana Dashboard visible to public
========================================

Exporting a Grafana dashboard is a bit pain, especially if you want to refresh the data. The easiest way is direct link to an image of specific panel.

You could do that from Grafana Dashboard->Panel->Share->Direct image rendered image

**Requirements**

Grafana Image Renderer plugin - this plugin has a lot of system dependencies. Switch on the Grafana debuging and check the log in order to resolve this. Personaly I didn't found a complete documentation describing which libraries a required.

**URL format**

$URL/render/d-solo/000000001/solar?orgId=1&refresh=30s&from="$STARTEPOCH"000&to="$EPOCH"000&panelId=4&width=430&height=200&tz=Europe%2FSofia"

Pay attention to '000000001' this is the dashboard id. Ensure 'panelId' has proper value as well- this is the actual panel you are rendering

Scripts
-------

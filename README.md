# Smartetailing Package
This package provides a simple, thin wrapper around the 3 major smartetailing endpoints. It also provides a Pythonic
object representation of the order xml export. `v2.00` is the XML version currently required. 
## Examples
* Basically, just instantiate `SmartetailingConnection()` object and call the public methods.
  ````
  from smartetailing import connection, objects
  
  connect_website = connection.SmartetailingConnection(base_url='www.example.com/webservices/xml/feeds.cfc', merchant_id=01234, urlkey='SECRET')
  orders = list(connect_website.export_orders())  # List[WebOrder]
  connect_website.confirm_order_receipts([o.id for o in orders])
  connect_website.update_order_status(orders[0].id, 'Completed')
  ````
* TODO - Doc comments need to be better
## Notes
* Currently only supports smart etailing order export v2. Support for v1 could be added if requested.
* Setup instructions from here: https://realpython.com/pypi-publish-python-package/
{
    "name": "Real Estate Nacho",
    "version": "1.0",
    "summary": "Real estate management module",
    "description": "Module to manage real estate properties, agents, and clients.",
    "author": "Nacho",
    "category": "Real Estate",
    "depends": ["base"],
    "data": [
        "security/real_estate_security.xml",
        "security/ir.model.access.csv",
        "views/realestate_property_views.xml", 
        "views/realestate_visit_views.xml",
        "views/realestate_menuitems.xml"],
    "installable": True,
    "application": True,
}
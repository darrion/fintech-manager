from flask import current_app as app, jsonify, request 
import controllers
from errors import ApiError
import typing as t

from models.psql import Client

@app.route("/signup/client", methods=["POST"])
def signup_client():

    """Return access token, refresh token, and level of auth for client."""

    return jsonify({})

@app.route("/signup/advisor", methods=["POST"])
def signup_advisor():

    """Return access token, refresh token, and level of auth for advisor."""

    return jsonify({})

@app.route("/poll", methods=["GET"])
def poll():

    """Poll redis queue for database initialization status."""

    return jsonify({})

@app.route("/init", methods=["POST"])
def init_db():

    """Accept JSON to initialize database."""


    ### TODO: Remove in production.
    ### For Demonstration Only 
    app.db.drop_all() # Clean up the database.
    app.db.create_all() # Reinitialize with empty tables.

    data = request.get_json()

    clients = data["clients"]
    financial_advisors = data["financial_advisors"]

    added_clients = []
    added_advisors = []

    for client in clients: 

        kwargs = {
            "first_name": client["first_name"],
            "last_name": client["last_name"]
        }

        client_id = controllers.client.add(**kwargs)
        added_client = controllers.client.get(client_id)
        added_client = added_client.json()
        added_clients.append(added_client)

        accounts = client["accounts"]
        for account in accounts:
            controllers.account.create(**{
                "type": account["type"], 
                "value": account["value"],
                "client_id": client_id,
            })

    for advisor in financial_advisors:
        
        first_name, last_name = advisor["name"].split(" ")
        focus_areas = advisor["focus_areas"]

        kwargs = {
            "first_name": first_name,
            "last_name": last_name
        }
        
        advisor_id = controllers.advisor.add(**kwargs)
        added_advisor = controllers.advisor.get(advisor_id)
        added_advisor = added_advisor.json()
        added_advisors.append(added_advisor)

        for spec in focus_areas:
            kwargs = {
                'focus': spec, 
                'advisor_id': advisor_id
            }
            controllers.advisor.specialization.add(**kwargs)

    return jsonify({
        "success": {
            "clients": added_clients, 
            "advisors": added_advisors,
        }
    })

@app.route("/advisors", methods=["GET"])
def get_advisors():

    """Get all advisors"""

    page = request.args.get("page")
    limit = request.args.get("limit")

    page = int(page)
    limit = int(limit)
    
    total, advisors = controllers.advisor.get_available_advisors(page=page, limit=limit)
    
    return jsonify({
        "success": {
            "message": advisors, 
            "total": total
        }
    })

@app.route("/advisor/assign", methods=["PATCH"])
def assign_advisor():

    """Set client's foreign key for advisor."""

    advisor_id = request.args.get("advisorId")
    client_id = request.args.get("clientId")

    try: 
        if not advisor_id or not client_id:
            raise ApiError("Request params `advisorId` and `clientId` are required.")
        controllers.advisor.assign(advisor_id, client_id)
        advisor = controllers.advisor.get(advisor_id=advisor_id)
        client = controllers.client.get(client_id=client_id)
        if not advisor:
            raise ApiError(f"Advisor with id {advisor_id} does not exist.")
        if not client:
            raise ApiError(f"Client with id {client_id} does not exist.")
    except Exception as error:
        return jsonify({
            "error": {
                "message": str(error)
            }
        }), 400
    return jsonify({
        "success": {
            "message": f"Assigned advisor {advisor.first_name} {advisor.last_name} to client {client.first_name} {client.last_name}."
        }
    }), 200

@app.route("/advisor/clients", methods=["GET"])
def get_assigned_clients():

    """Get all clients of an advisor."""

    clients = []
    page = request.args.get("page")
    limit = request.args.get("limit")
    advisor_id = request.args.get("advisorId")
    
    clients = None 
    total = 0

    try:
        
        if not advisor_id or not page or not limit:
            raise ApiError("Request params `advisorId`, `page`, and `limit` are required.")
        
        advisor = controllers.advisor.get(advisor_id=advisor_id)

        if not advisor:
            raise ApiError(f"Advisor with id {advisor_id} does not exist.")
        
        page = int(page) 
        limit = int(limit)
        
        total, clients = controllers.advisor.get_assigned_clients(
            advisor_id=advisor_id,
            page=page,
            limit=limit
            )
        
    except Exception as error: 
        return jsonify({
            "error": {
                "message": str(error)
            }
        }), 400
    return jsonify({
        "success": {
            "clients": clients,
            "total": total,
        }
    }), 200
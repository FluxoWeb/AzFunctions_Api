import azure.functions as func
import requests
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

def get_api_data(api_url, headers):
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json().get('value', [])
        return data
    else:
        return None

@app.route(route="omnichannel")
def omnichannel(req: func.HttpRequest) -> func.HttpResponse:

    headers = {"Authorization": "ZHqz9oRPKQ0r6tBrp088jq82xVmJtTCOVKaG2BjyR5pRevn"}
    api_url = "https://zoytest.neo.com.py/Odata/ContratosOData?$select=Id,Status,ClienteId,PlanoId,DiaBase&$filter=Status eq 11 or Status eq 10&$expand=Cliente($select=Nome,Documento_j,Documento_f,TelCelular),Plano($select=plano),Cidade($select=cidade)&$top=2000"

    try:
        api_data = get_api_data(api_url, headers)
        if api_data is not None:
            remapped_data = []

            for item in api_data:
                remapped_item = {
                    "ClienteId": item.get("ClienteId"),
                    "NombreCliente": item.get("Cliente", {}).get("Nome"),
                    "RUC": item.get("Cliente", {}).get("Documento_j"),
                    "CI": item.get("Cliente", {}).get("Documento_f"),
                    "NumeroTelefono": item.get("Cliente", {}).get("TelCelular"),
                    "ContratoId": item.get("Id"),
                    "FechaVencimiento": item.get("DiaBase"),
                    "NombreContrato": item.get("Plano", {}).get("plano"),
                    "Localidad": item.get("Cidade", {}).get("cidade")
                }

                remapped_data.append(remapped_item)

            json_response = json.dumps(remapped_data, indent=2)
            return func.HttpResponse(json_response, mimetype="application/json", status_code=200)
        else:
            return func.HttpResponse("Error al obtener datos de la API.", status_code=500)
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

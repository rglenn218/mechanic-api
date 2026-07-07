from application.extensions import ma
from application.models import Service

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service
        load_instance = False
        include_fk = True
        
service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
from django.contrib import admin
from client.models import *

# Register your models here.
class ClientAdmin(admin.ModelAdmin):
	list_display = [ 'fname', 'lname', 'phone']
	class Meta:
		model = t_client
admin.site.register(t_client, ClientAdmin)

class CareGiverAdmin(admin.ModelAdmin):
	list_display = [ 'client', 'care_attendant', 'timestamp']
	class Meta:
		model = t_care_giver
admin.site.register(t_care_giver, CareGiverAdmin)

class BillAdmin(admin.ModelAdmin):
	list_display = [ 'billing_date', 'batch_id']
	class Meta:
		model = t_bill
admin.site.register(t_bill, BillAdmin)

class BatchAdmin(admin.ModelAdmin):
	list_display = [ 'rootid', 'billing_date', 'payment_date', 'status', 'timestamp']
	class Meta:
		model = t_batch
admin.site.register(t_batch, BatchAdmin)

class BillingTrackerAdmin(admin.ModelAdmin):
	list_display = [ 'rootid', 'service_date_from', 'service_date_to', 'client_number','payment_status']
	class Meta:
		model = t_billing_tracker
admin.site.register(t_billing_tracker, BillingTrackerAdmin)
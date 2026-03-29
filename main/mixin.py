from django.db.models import ProtectedError

class AuditMixin:
    audit_action = None

    def create_audit_log(self, obj):
        from .models import AuditLog

        if not self.audit_action:
            raise ValueError("Action type must be set in views.")
        
        user = self.request.user if self.request.user.is_authenticated else None

        AuditLog.objects.create(
            user=user,
            action_type=self.audit_action,
            model_name=obj.__class__.__name__,
            object_id=obj.id,
            description=self.get_audit_description(obj)
        )

    def get_audit_description(self, obj):
        return f"{self.request.user} performed {self.audit_action} on {obj}"

    def form_valid(self, form):
        response = super().form_valid(form)

        if hasattr(self, 'object') and self.object:
            self.create_audit_log(self.object)

        return response

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        self.create_audit_log(obj)
        return super().delete(request, *args, **kwargs)